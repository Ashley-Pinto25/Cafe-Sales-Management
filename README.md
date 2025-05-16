Cafe Sales Management System

A simple Flask based cafe order management application using SQLite as the database and a basic HTML frontend.
This app allows you to place orders, generate PDF bills, and view sales reports.

Project Structure

.
├── app.py # Flask backend application
├── index.html # Frontend HTML page (served via Flask)
└── schema.sql # SQLite database schema and sample data

Setup & Run Instructions

    Clone the repository
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name

    (Optional) Create and activate a virtual environment
    python3 -m venv venv
    source venv/bin/activate # On Windows: venv\Scripts\activate

    Install dependencies
    pip install flask reportlab

    Initialize the SQLite database
    sqlite3 cafe_management.db < schema.sql

    Run the Flask application
    python app.py

Open the app in your browser at http://127.0.0.1:5000

Usage

    Login with sample credentials (e.g., username: admin, password: admin123).

    Place orders by selecting items and entering the customer name.

    Download the generated PDF bill for each order.

    View the sales report with order summaries.

Notes

    Passwords are stored in plain text; not for production use.

    PDF bills are generated dynamically using reportlab.

    Menu items and user data can be changed by editing schema.sql.

    Frontend is customizable via index.html.
