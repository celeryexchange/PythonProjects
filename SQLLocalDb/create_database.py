import sqlite3
import random
from faker import Faker

# Initialize Faker object
fake = Faker()
Faker.seed(11)

with sqlite3.connect('example.db') as conn:
    cursor = conn.cursor()

    with open('sql/create_table_customers.sql') as f:
        query = f.read()

    # Create customers table
    cursor.execute(query)
    conn.commit()
    print("Customers table created successfully.")

    # Insert customer records
    num_records = 10
    for _ in range(num_records):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        phone = fake.phone_number()
        num_orders = random.randint(0, 100)

        sql = "INSERT INTO customers (first_name, last_name, email, phone, num_orders)" \
              "VALUES (:first_name, :last_name, :email, :phone, :num_orders)"
        cursor.execute(sql, {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'num_orders': num_orders})

    conn.commit()

    print(f"{num_records} customer records inserted successfully.")
    cursor.close()
