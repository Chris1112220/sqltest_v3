import sqlite3


# connecting to database
conn = sqlite3.connect("sales_data.db")
cursor = conn.cursor()


# creating table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    sale_date TEXT NOT NULL
);
""")
# Creating new Tranactions table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_date TEXT NOT NULL,
    amount REAL NOT NULL
);
""")


# inserting sample data
sample_data = [
    ("Laptop", 3, 1200.00, "2025-03-01"),
    ("Mouse", 10, 25.50, "2025-03-02"),
    ("Keyboard", 5, 75.99, "2025-03-03"),
    ("Monitor", 2, 300.00, "2025-03-04"),
    ("Headphones", 7, 50.00, "2025-03-05")
]


# Inserting sample data into Transactions table
sample_transactions = [
    ("2025-03-01", 1500.00),
    ("2025-03-02", 250.50),
    ("2025-03-02", 600.00),
    ("2025-03-03", 75.99),
    ("2025-03-05", 300.00)
]
cursor.executemany(
    "INSERT INTO Transactions (transaction_date, amount) VALUES (?, ?)", sample_transactions)


cursor.executemany(
    "INSERT INTO Sales (product_name, quantity, price, sale_date) VALUES (?, ?, ?, ?)", sample_data)
conn.commit()

# printing all data
print("All Sales Data:")
cursor.execute("SELECT * FROM Sales")
for row in cursor.fetchall():
    print(row)

print("\nAll Transactions:")
cursor.execute("SELECT * FROM Transactions")
for row in cursor.fetchall():
    print(row)

print("\nSales with price > $100:")
cursor.execute("SELECT * FROM Sales WHERE price > 100")
for row in cursor.fetchall():
    print(row)

print("\nSales sorted by sale_date:")
cursor.execute("SELECT * FROM Sales ORDER BY sale_date DESC")
for row in cursor.fetchall():
    print(row)
