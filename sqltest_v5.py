import sqlite3

# Connecting to the database
conn = sqlite3.connect("sales_data.db")
cursor = conn.cursor()

# Enabling foreign key constraints
cursor.execute("PRAGMA foreign_keys = ON;")

# Dropping existing tables to prevent duplication issues
cursor.execute("DROP TABLE IF EXISTS Transactions;")
cursor.execute("DROP TABLE IF EXISTS Customers;")
cursor.execute("DROP TABLE IF EXISTS Sales;")

# Creating Customers table
cursor.execute("""
CREATE TABLE Customers (
    Customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    signup_date TEXT NOT NULL
);
""")

# Creating Sales table (NOW WITH customer_id AS FOREIGN KEY)
cursor.execute("""
CREATE TABLE Sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    sale_date TEXT NOT NULL,
    customer_id INTEGER,
    FOREIGN KEY (customer_id) REFERENCES Customers(Customer_id)
);
""")

# Creating Transactions table (with customer_id as a foreign key)
cursor.execute("""
CREATE TABLE Transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_date TEXT NOT NULL,
    amount REAL NOT NULL,
    customer_id INTEGER,
    FOREIGN KEY (customer_id) REFERENCES Customers(Customer_id)
);
""")

# Inserting sample Customers
sample_customers = [
    ("Alice Johnson", "alice@email.com", "2025-01-10"),
    ("Bob Smith", "bob@email.com", "2025-01-12"),
    ("Charlie Brown", "charlie@email.com", "2025-01-15"),
    ("Diana Prince", "diana@email.com", "2025-01-20"),
    ("Evan Wright", "evan@email.com", "2025-01-22")
]

cursor.executemany(
    "INSERT INTO Customers (name, email, signup_date) VALUES (?, ?, ?)", sample_customers
)
conn.commit()

# Debugging: Check inserted Customers
cursor.execute("SELECT * FROM Customers")
print("\nExisting Customers:")
for row in cursor.fetchall():
    print(row)

# Inserting sample Sales data WITH customer_id
sample_sales = [
    ("Laptop", 3, 1200.00, "2025-03-01", 1),   # Alice
    ("Mouse", 10, 25.50, "2025-03-02", 2),    # Bob
    ("Keyboard", 5, 75.99, "2025-03-03", 3),  # Charlie
    ("Monitor", 2, 300.00, "2025-03-04", 4),  # Diana
    ("Headphones", 7, 50.00, "2025-03-05", 5)  # Evan
]

cursor.executemany(
    "INSERT INTO Sales (product_name, quantity, price, sale_date, customer_id) VALUES (?, ?, ?, ?, ?)", sample_sales
)

# Insert Transactions AFTER Customers exist
sample_transactions = [
    ("2025-03-01", 1500.00, 1),  # Alice
    ("2025-03-02", 250.50, 2),   # Bob
    ("2025-03-02", 600.00, 2),   # Bob
    ("2025-03-03", 75.99, 3),    # Charlie
    ("2025-03-05", 300.00, 4)    # Diana
]

cursor.executemany(
    "INSERT INTO Transactions (transaction_date, amount, customer_id) VALUES (?, ?, ?)", sample_transactions
)
conn.commit()

# Printing all Sales data
print("\nAll Sales Data:")
cursor.execute("SELECT * FROM Sales")
for row in cursor.fetchall():
    print(row)

# Printing all Transactions data
print("\nAll Transactions:")
cursor.execute("SELECT * FROM Transactions")
for row in cursor.fetchall():
    print(row)

# Printing all Customers data
print("\nAll Customers:")
cursor.execute("SELECT * FROM Customers")
for row in cursor.fetchall():
    print(row)

# Query 1: Retrieve all transactions for a specific customer
customer_name = "Alice Johnson"
print(f"\nTransactions for {customer_name}:")
cursor.execute("""
SELECT Transactions.id, Transactions.transaction_date, Transactions.amount 
FROM Transactions
JOIN Customers ON Transactions.customer_id = Customers.Customer_id
WHERE Customers.name = ?;
""", (customer_name,))
for row in cursor.fetchall():
    print(row)

# Query 2: Find the total transaction amount per customer
print("\nTotal transaction amount per customer:")
cursor.execute("""
SELECT Customers.name, SUM(Transactions.amount) AS total_spent
FROM Transactions
JOIN Customers ON Transactions.customer_id = Customers.Customer_id
GROUP BY Customers.name;
""")
for row in cursor.fetchall():
    print(row)

# Query 3: Get the most recent transaction date for each customer
print("\nMost recent transaction date for each customer:")
cursor.execute("""
SELECT Customers.name, MAX(Transactions.transaction_date) AS last_transaction
FROM Transactions
JOIN Customers ON Transactions.customer_id = Customers.Customer_id
GROUP BY Customers.name;
""")
for row in cursor.fetchall():
    print(row)

# Query 4: Get total **sales** amount per customer
print("\nTotal sales amount per customer:")
cursor.execute("""
SELECT Customers.name, SUM(Sales.price * Sales.quantity) AS total_sales
FROM Sales
JOIN Customers ON Sales.customer_id = Customers.Customer_id
GROUP BY Customers.name;
""")
for row in cursor.fetchall():
    print(row)

# Close the connection
conn.close()
