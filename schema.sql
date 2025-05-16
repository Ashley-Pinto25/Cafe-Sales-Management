DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount REAL DEFAULT 0
);

DROP TABLE IF EXISTS menu;
CREATE TABLE menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL  -- price in Rupees
);

DROP TABLE IF EXISTS order_items;
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(item_id) REFERENCES menu(id)
);

-- Insert sample menu items
INSERT INTO menu (name, price) VALUES ('Coffee', 40.00);
INSERT INTO menu (name, price) VALUES ('Tea', 30.00);
INSERT INTO menu (name, price) VALUES ('Sandwich', 70.00);
INSERT INTO menu (name, price) VALUES ('Cake Slice', 90.00);
INSERT INTO menu (name, price) VALUES ('Burger', 120.00);
INSERT INTO menu (name, price) VALUES ('Fries', 60.00);
INSERT INTO menu (name, price) VALUES ('Soft Drink', 50.00);

-- Insert a sample user
INSERT INTO users (username, password) VALUES ('admin', 'admin123');
