import decimal
import os
import sys
import random
import uuid
from datetime import datetime, timedelta
from time import sleep

import numpy as np
from faker import Faker
import psycopg2
from faker.providers import BaseProvider

num_records = int(os.getenv('NUM_RECORDS'))
time_to_connect = 30

sleep(10)
time = datetime.now()
success = False
while not success:
    try:
        connection = psycopg2.connect(
            host="postgres",
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=5432
        )
        success = True

    except:
        success = False
    if datetime.now() - time > timedelta(seconds=time_to_connect):
        sys.exit("Connection timed out")

print("Connected successfully")

fake = Faker(locale='ru_RU')
max_decimal_value = decimal.Decimal('Infinity')
max_elements_selected = 1000


class CustomProvider(BaseProvider):
    def custom_phone_number(self):
        phone_number = "+7"
        for _ in range(10):
            phone_number += str(random.randint(0, 9))
        return phone_number

    def generate_photo(self):
        photo_bytes = bytes([random.randint(0, 255) for _ in range(100)])
        return photo_bytes

    def generate_rating(self):
        return random.randint(1, 5)


class UserGenerator:
    def generate_user(self):
        user_name = fake.name()
        phone_number = fake.custom_phone_number()
        email_address = fake.email()
        photo = fake.generate_photo()
        password = fake.password()

        user = {
            "name": user_name,
            "phone_number": phone_number,
            "email_address": email_address,
            "photo": photo,
            "password": password
        }
        return user


class ShopGenerator:
    def generate_shop(self):
        shop_name = fake.company()
        photo = fake.generate_photo()
        address = fake.address()
        description = fake.sentence()
        legal_details = fake.sentence()
        password = fake.password()

        shop = {
            "name": shop_name,
            "photo": photo,
            "address": address,
            "description": description,
            "legal_details": legal_details,
            "password": password
        }
        return shop


category_names = ["Цветы и подарки", "Кондитерские и пекарни", "Живые растения", "Косметика и парфюмерия", "Чай и кофе",
                  "Украшения", "Продукты и напитки", "Декор", "Посуда", "Аксессуары",
                  "Одежда", "Одежда для детей", "Хендмейд и хобби", "Товары для праздника", "Книги", "Картины",
                  "Зоотовары", "Подарочные сертификаты", "Для дома", "Канцелярские товары", "Другое"]

cur = connection.cursor()
user_generator = UserGenerator()
shop_generator = ShopGenerator()

for _ in range(num_records):
    user = user_generator.generate_user()
    cur.execute("""
    INSERT INTO Users (name, phone_number, email_address, photo, password)
    VALUES (%s, %s, %s, %s, %s)
    """, (user["name"], user["phone_number"], user["email_address"], user["photo"], user["password"]))
print("Users generated")

for _ in range(num_records):
    product = shop_generator.generate_shop()
    cur.execute("""
    INSERT INTO Shops (name, photo, address, description, legal_details, password)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, (product["name"], product["photo"], product["address"], product["description"], product["legal_details"],
          product["password"]))
print("Shops generated")

for category in category_names:
    cur.execute("""
       INSERT INTO Categories (name)
       VALUES (%s)
       """, category)
print("Categories generated")

for category in category_names:
    cur.execute("""
                   SELECT category_id FROM Categories 
                    WHERE name = %s
                   """, category)
    category_id = cur.fetchone()[0]

    for _ in range(10):
        subcategory = fake.noun()

        cur.execute("""
               INSERT INTO Subcategories (name, category_id)
               VALUES (%s, %s)
               """, (subcategory, category_id))
print("Subcategories generated")

cur.execute("SELECT subcategory_id FROM Subcategories")
subcategories = cur.fetchall()

available_max_limits = list(range(1000, 10001, 1000))
cur.execute("SELECT shop_id FROM Shops")
while True:
    batch = cur.fetchmany(max_elements_selected)  # Получаем порции данных по 1000 записей за раз
    if not batch:
        break
    for product in batch:
        shop_id = product[0]
        num_products = random.randint(0, 2)  # Случайное количество лимитов для магазина
        max_limits = available_max_limits[:]
        max_limit_exists = False

        # Вставка данных в таблицу deliveryPrices
        for _ in range(num_products):
            price = random.randint(0, 10) * 100  # Генерация случайной цены для доставки
            if not max_limit_exists:
                max_limit_exists = True
                max_limit = max_decimal_value
            else:
                max_limit = random.choice(max_limits)  # Генерация случайного максимального лимита
                max_limits.remove(max_limit)
            cur.execute("""
                INSERT INTO DeliveryPrices (shop_id, price, max_limit)
                VALUES (%s, %s, %s)
            """, (shop_id, price, max_limit))
print("Delivery prices generated")

cur.execute("SELECT shop_id FROM Shops")
while True:
    batch = cur.fetchmany(max_elements_selected)  # Получаем порции данных по 1000 записей за раз
    if not batch:
        break
    for product in batch:
        shop_id = product[0]
        num_products = random.randint(5, 10)  # Случайное количество продуктов для магазина

        # Вставка данных в таблицу deliveryPrices
        for _ in range(num_products):
            name = fake.noun()
            subcategory_id = random.choice(subcategories)
            photo = fake.generate_photo()
            description = fake.sentence()
            width = random.randint(100, 300)
            height = random.randint(100, 300)
            cur.execute("""
                INSERT INTO Products (name, subcategory_id, photo, description, shop_id, width, height)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (name, subcategory_id, photo, description, shop_id, width, height))
print("Products generated")

cur.execute("SELECT product_id FROM Products")
while True:
    batch = cur.fetchmany(max_elements_selected)  # Получаем порции данных по 1000 записей за раз
    if not batch:
        break
    for product in batch:
        product_id = product[0]
        num_history = random.randint(1, 3)
        price = random.randint(100, 10000)
        rnd_start_date = datetime.now() - timedelta(days=4 * 365)
        rnd_end_date = datetime.now() - timedelta(days=400)
        time = fake.date_time_between(start_date=rnd_start_date, end_date=rnd_end_date)
        for _ in range(num_history):
            cur.execute("""
                            INSERT INTO PriceHistories (product_id, time, price)
                            VALUES (%s, %s, %s)
                        """, (product_id, time, price))

        num_structure = random.randint(1, 3)
        for _ in range(num_structure):
            element = fake.noun()
            quantity = random.randint(1, 10)
            cur.execute("""
                            INSERT INTO Structures (product_id, element, quantity)
                            VALUES (%s, %s, %s)
                        """, (product_id, element, quantity))
print("Structures and price histories generated")

cur.execute("SELECT user_id FROM Users")
users = cur.fetchall()
cur.execute("SELECT shop_id FROM Shops")
shops = cur.fetchall()
cur.execute("SELECT product_id FROM products")
all_products = cur.fetchall()

for _ in range(num_records // 10):
    random_user = random.choice(users)
    for shop in range(random.randint(1, 5)):
        random_shop = random.choice(shops)
        cur.execute("""
                            INSERT INTO favoritelists (user_id, shop_id)
                            VALUES (%s, %s)
                        """, (random_user, random_shop))
print("Favorite lists generated")

statuses = ['CREATED', 'IN_PROGRESS', 'CANCELED', 'DELIVERED']
for _ in range(num_records):
    random_user = random.choice(users)
    order_id = uuid.uuid4()
    status = random.choice(statuses)
    rnd_start_date = datetime.now() - timedelta(days=365)
    rnd_end_date = datetime.now()
    time = fake.date_time_between(start_date=rnd_start_date, end_date=rnd_end_date)
    card_number = fake.credit_card_number()
    cur.execute("""
                                INSERT INTO orderheaders (order_id, user_id, status, time, card_number)
                                VALUES (%s, %s, %s, %s, %s)
                            """, (order_id, random_user, status, time, card_number))

    random_shop = random.choice(shops)
    cur.execute("SELECT product_id FROM Products WHERE shop_id = %s", random_shop)
    products = cur.fetchall()
    products_for_rating = []
    for order_details in range(random.randint(1, 5)):
        quantity = random.randint(1, 10)
        product_id = random.choice(products)
        products_for_rating.append(product_id)
        products.remove(product_id)
        cur.execute("""
                                    SELECT price 
                                    FROM pricehistories 
                                    WHERE product_id = %s
                                    AND time <= %s
                                    ORDER BY time DESC 
                                    LIMIT 1;
                                """, (product_id, time))
        price = cur.fetchone()
        cur.execute("""
                            INSERT INTO orderdetails (order_id, product_id, quantity, price)
                            VALUES (%s, %s, %s, %s)
                            """, (order_id, product_id, quantity, price))

    if fake.pybool():
        description = fake.sentence()
        rating = random.randint(1, 5)
        cur.execute("""
                            INSERT INTO userreviews (user_id, shop_id, description, rating)
                            VALUES (%s, %s, %s, %s)
                        """, (random_user, random_shop, description, rating))

    if fake.pybool():
        description = fake.sentence()
        product_id = random.choice(products_for_rating)
        rating_1 = random.randint(1, 5)
        rating_2 = random.randint(1, 5)
        rating_3 = random.randint(1, 5)
        photo = fake.generate_photo()
        cur.execute("""
                            INSERT INTO shopreviews (user_id, product_id, description, photo, matching_rating, service_rating, price_quality_rating)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            """,
                    (random_user, product_id, description, photo, rating_1, rating_2, rating_3))

print("Orders generated")
print("Reviews generated")

for _ in range(num_records // 10):
    collection_id = uuid.uuid4()
    user_id = random.choice(users)
    description = fake.sentence()
    public = fake.pybool()
    cur.execute("""
                            INSERT INTO collectionheaders (collection_id, user_id, description, public)
                            VALUES (%s, %s, %s, %s)
                            """, (collection_id, user_id, description, public))
    for i in range(random.randint(1, 10)):
        product_id = random.choice(all_products)
        cur.execute("""
                            INSERT INTO collectiondetails (collection_id, product_id)
                            VALUES (%s, %s)
                            """, (collection_id, product_id))

print("Collections generated")

for _ in range(num_records // 10):
    dialog_id = uuid.uuid4()
    random_user = random.choice(users)
    random_shop = random.choice(shops)
    cur.execute("""
                        INSERT INTO dialogs (dialog_id, user_id, shop_id)
                        VALUES (%s, %s, %s)
                        """, (dialog_id, random_user, random_shop))

    for i in range(random.randint(1, 10)):
        message = fake.sentence()
        sender_is_user = fake.pybool()
        message_is_read = 0
        time = fake.date_this_year()
        cur.execute("""
                            INSERT INTO messages (dialog_id, message, time, sender_is_user, message_is_read)
                            VALUES (%s, %s, %s, %s, %s)
                            """, (dialog_id, message, sender_is_user, message_is_read, time))


cur.close()
connection.commit()
connection.close()
