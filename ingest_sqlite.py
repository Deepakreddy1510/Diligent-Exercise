# ingest_sqlite.py
import sqlite3
import csv

DB_NAME = "ecom.db"

def create_tables(conn):
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        join_date TEXT
    )""")
    c.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        name TEXT,
        category TEXT,
        price REAL,
        in_stock INTEGER
    )""")
    c.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        order_date TEXT,
        status TEXT,
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    )""")
    c.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        unit_price REAL,
        FOREIGN KEY(order_id) REFERENCES orders(order_id),
        FOREIGN KEY(product_id) REFERENCES products(product_id)
    )""")
    c.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        review_id INTEGER PRIMARY KEY,
        product_id INTEGER,
        customer_id INTEGER,
        rating INTEGER,
        review_text TEXT,
        review_date TEXT,
        FOREIGN KEY(product_id) REFERENCES products(product_id),
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    )""")
    conn.commit()

def import_csv(conn, csv_file, table_name, columns):
    with open(csv_file, 'r', encoding='utf-8') as f:
        dr = csv.DictReader(f)
        to_db = []
        for row in dr:
            to_db.append(tuple(row[col] for col in columns))
    placeholders = ",".join(["?"] * len(columns))
    conn.executemany(f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})", to_db)
    conn.commit()

def main():
    conn = sqlite3.connect(DB_NAME)
    create_tables(conn)

    import_csv(conn, "customers.csv", "customers", ["customer_id","first_name","last_name","email","join_date"])
    import_csv(conn, "products.csv", "products", ["product_id","name","category","price","in_stock"])
    import_csv(conn, "orders.csv", "orders", ["order_id","customer_id","order_date","status"])
    import_csv(conn, "order_items.csv", "order_items", ["order_item_id","order_id","product_id","quantity","unit_price"])
    import_csv(conn, "reviews.csv", "reviews", ["review_id","product_id","customer_id","rating","review_text","review_date"])

    print(f"Imported CSVs into {DB_NAME}")
    conn.close()

if __name__ == "__main__":
    main()
