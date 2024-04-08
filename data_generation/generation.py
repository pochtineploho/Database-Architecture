import os
import sys
import random
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
        description = fake.text()
        legal_details = fake.text()
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
    shop = shop_generator.generate_shop()
    cur.execute("""
    INSERT INTO Shops (name, photo, address, description, legal_details, password)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, (shop["name"], shop["photo"], shop["address"], shop["description"], shop["legal_details"], shop["password"]))
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
        subcategory = fake.word()

        cur.execute("""
               INSERT INTO Subcategories (name, category_id)
               VALUES (%s, %s)
               """, (subcategory, category_id))
print("Subcategories generated")

cur.close()
connection.commit()
connection.close()
