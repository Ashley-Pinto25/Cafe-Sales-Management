# Cafe Sales Management System

A simple **Flask** based cafe order management application using **SQLite** as the database and a basic HTML frontend.  
This app allows you to place orders, generate PDF bills, and view sales reports.

---

## Project Structure

.
├── app.py # Flask backend application
├── index.html # Frontend HTML page (served via Flask)
└── schema.sql # SQLite database schema and sample data


---

## Setup & Run Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name

2. (Optional) Create and activate a virtual environment

python3 -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate

3. Install dependencies

pip install flask reportlab

4. Initialize the SQLite database

Make sure you have SQLite installed. Then run:

sqlite3 cafe_management.db < schema.sql

5. Run the Flask application

python app.py

The app will start at: http://127.0.0.1:5000
