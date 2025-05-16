Cafe Sales Management System

A simple Flask-based cafe order management app with SQLite database and a frontend.
Project Structure

.
├── app.py         # Flask backend application
├── index.html     # Frontend HTML page (served via Flask)
└── schema.sql     # SQLite database schema and sample data

Setup & Run Instructions
1. Clone the repository

git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name

2. (Optional but recommended) Create and activate a virtual environment

python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

3. Install required Python packages

pip install flask reportlab

4. Initialize the database

Make sure SQLite is installed, then run:

sqlite3 cafe_management.db < schema.sql

5. Run the Flask app

python app.py

This will start the app at http://127.0.0.1:5000.
Usage

    Open http://127.0.0.1:5000 in your browser.

    Login with sample credentials (e.g., username: admin, password: admin123).

    Place orders, enter customer name.

    Download the generated PDF bill.

    View sales reports.

Notes

    The app currently uses plain text passwords (for demo purposes only).

    You can customize the database or frontend UI by editing schema.sql and index.html.

    PDF bills are generated dynamically using the reportlab Python library.

If you want me to help create a requirements.txt file or add a .gitignore, just let me know!
