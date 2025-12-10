# generate_data.py
import csv
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
random.seed(42)
Faker.seed(42)

NUM_CUSTOMERS = 200
NUM_PRODUCTS = 80
NUM_ORDERS = 500
MAX_ITEMS_PER_ORDER = 5

# 1) customers.csv
customers = []
for i in range(1, NUM_CUSTOMERS + 1):
    customers.append({
        "customer_id": i,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "join_date": fake.date_between(start_date='-2y', end_date='today').isoformat()
    })

# 2) products.csv
products = []
categories = ["electronics", "home", "books", "toys", "beauty", "sports"]
for i in range(1, NUM_PRODUCTS + 1):
    products.append({
        "product_id": i,
        "name": f"{fake.word().capitalize()} {random.choice(['Pro','Plus','X','Mini','Max'])}",
        "category": random.choice(categories),
        "price": round(random.uniform(5, 500), 2),
        "in_stock": random.randint(0, 200)
    })

# 3) orders.csv and order_items.csv
orders = []
order_items = []
order_id = 1
for _ in range(NUM_ORDERS):
    cust = random.choice(customers)
    order_date = fake.date_time_between(start_date='-365d', end_date='now')
    num_items = random.randint(1, MAX_ITEMS_PER_ORDER)
    orders.append({
        "order_id": order_id,
        "customer_id": cust["customer_id"],
        "order_date": order_date.isoformat(),
        "status": random.choice(["completed", "cancelled", "refunded"])
    })
    for _ in range(num_items):
        prod = random.choice(products)
        qty = random.randint(1, 4)
        unit_price = prod["price"]
        order_items.append({
            "order_item_id": len(order_items) + 1,
            "order_id": order_id,
            "product_id": prod["product_id"],
            "quantity": qty,
            "unit_price": unit_price
        })
    order_id += 1

# 4) reviews.csv
reviews = []
for i in range(1, 300):
    reviews.append({
        "review_id": i,
        "product_id": random.choice(products)["product_id"],
        "customer_id": random.choice(customers)["customer_id"],
        "rating": random.randint(1,5),
        "review_text": fake.sentence(nb_words=12),
        "review_date": fake.date_time_between(start_date='-365d', end_date='now').isoformat()
    })

# Write CSV helper
def write_csv(filename, rows, fieldnames):
    with open(filename, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

write_csv("customers.csv", customers, ["customer_id","first_name","last_name","email","join_date"])
write_csv("products.csv", products, ["product_id","name","category","price","in_stock"])
write_csv("orders.csv", orders, ["order_id","customer_id","order_date","status"])
write_csv("order_items.csv", order_items, ["order_item_id","order_id","product_id","quantity","unit_price"])
write_csv("reviews.csv", reviews, ["review_id","product_id","customer_id","rating","review_text","review_date"])

print("Generated CSV files: customers.csv, products.csv, orders.csv, order_items.csv, reviews.csv")
