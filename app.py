import os
import sqlite3
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import datetime

app = Flask(__name__)
CORS(app)
DATABASE = 'cafe.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE, timeout=10, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def generate_pdf_bill(order_id, customer_name, order_items, total_amount):
    filename = f"bill_order_{order_id}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    margin = 20 * mm

    # Title - HOTEL AMEOBUS uppercase, bold, big and underlined
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height - margin, "HOTEL AMEOBUS")
    c.setLineWidth(2)
    c.line(margin, height - margin - 10, width - margin, height - margin - 10)

    # Current date string
    current_date = datetime.now().strftime("%d-%m-%Y")

    # Header info
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin, height - margin - 40, f"Customer Name: {customer_name}")
    c.drawRightString(width - margin, height - margin - 40, f"No: {order_id}")
    c.drawRightString(width - margin, height - margin - 55, f"Date: {current_date}")

    # Prepare table data
    data = [["S.No", "Particulars", "Qty", "Rate", "Amount"]]
    for idx, item in enumerate(order_items, 1):
        amount = item['quantity'] * item['price']
        data.append([
            str(idx),
            item['name'],
            str(item['quantity']),
            f"Rs. {item['price']:.2f}",
            f"Rs. {amount:.2f}"
        ])

    # Create Table
    table_width = width - 2 * margin
    col_widths = [40, 250, 60, 70, 70]  # Adjusted widths
    t = Table(data, colWidths=col_widths, hAlign='CENTER')

    # Table style - navy blue header background, white text, thick borders for outer & header row
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#001f4d")),  # Navy blue header
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),           # White header text
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('INNERGRID', (0, 1), (-1, -1), 1, colors.HexColor("#001f4d")),  # Navy blue grid
        ('BOX', (0, 0), (-1, -1), 3, colors.HexColor("#001f4d")),         # Thick outer border navy
        ('LINEABOVE', (0, 0), (-1, 0), 3, colors.HexColor("#001f4d")),    # Thick line above header
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Increased padding top header row
        ('TOPPADDING', (0, 1), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
    ])
    t.setStyle(style)

    # Calculate table position
    table_height = t.wrap(table_width, height)[1]
    table_y = height - margin - 80 - table_height

    # Draw table on canvas
    t.wrapOn(c, table_width, height)
    t.drawOn(c, margin, table_y)

    # Gap after table before total
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(width - margin, table_y - 25, f"Total: Rs. {total_amount:.2f}")

    # Footer
    c.setFont("Helvetica", 8)
    c.drawString(margin, 50, "E. & O.E")
    c.drawRightString(width - margin, 50, "For Hotel Ameobus")
    c.drawString(margin, 35, "THANK YOU")
    c.drawString(margin, 20, "Goods Once Sold Will not Be Taken Back.")
    c.drawRightString(width - margin, 20, "Proprietor")

    c.showPage()
    c.save()

    return filename

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    u = request.json.get('username')
    p = request.json.get('password')
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE username=? AND password=?',
        (u, p)
    ).fetchone()
    conn.close()
    if user:
        return jsonify(success=True, username=u)
    return jsonify(success=False, message="Wrong username or password"), 401

@app.route('/menu')
def menu():
    conn = get_db_connection()
    items = conn.execute('SELECT id, name, price FROM menu').fetchall()
    conn.close()
    return jsonify([dict(i) for i in items])

@app.route('/orders', methods=['POST'])
def orders():
    data = request.json
    cn = data.get('customer_name')
    items = data.get('items') or []
    if not cn or not items:
        return jsonify(success=False, message="Customer & items required"), 400

    conn = get_db_connection()
    cur = conn.cursor()

    # Find or create customer
    c = conn.execute('SELECT id FROM customers WHERE name=?', (cn,)).fetchone()
    if c:
        cid = c['id']
    else:
        cur.execute('INSERT INTO customers(name) VALUES(?)', (cn,))
        cid = cur.lastrowid
        conn.commit()

    # New order
    cur.execute('INSERT INTO orders(customer_name) VALUES(?)', (cn,))
    oid = cur.lastrowid

    total = 0
    details = []
    for it in items:
        mid, qty = it['item_id'], it['quantity']
        if qty <= 0:
            continue
        m = conn.execute('SELECT name, price FROM menu WHERE id=?', (mid,)).fetchone()
        name, price = m['name'], m['price']
        total += price * qty
        cur.execute(
            'INSERT INTO order_items(order_id, item_id, quantity) VALUES(?,?,?)',
            (oid, mid, qty)
        )
        details.append({'name': name, 'quantity': qty, 'price': price})

    cur.execute('UPDATE orders SET total_amount=? WHERE id=?', (total, oid))
    conn.commit()
    conn.close()

    pdf = generate_pdf_bill(oid, cn, details, total)
    return jsonify(success=True, order_id=oid, bill_pdf=pdf), 201

@app.route('/bill/<int:order_id>')
def bill(order_id):
    fn = f"bill_order_{order_id}.pdf"
    if os.path.exists(fn):
        return send_file(fn, as_attachment=True)
    return jsonify(success=False, message="Bill not found"), 404

@app.route('/sales_report')
def sales_report():
    conn = get_db_connection()
    rows = conn.execute(
        'SELECT id AS order_id, customer_name, order_time, total_amount FROM orders ORDER BY order_time DESC'
    ).fetchall()
    conn.close()
    total_orders = len(rows)
    total_sales = sum(r['total_amount'] for r in rows)
    avg = total_sales / total_orders if total_orders else 0
    return jsonify(
        total_orders=total_orders,
        total_sales=total_sales,
        average_order_amount=avg,
        orders=[dict(r) for r in rows]
    )

if __name__ == '__main__':
    app.run(debug=True)
