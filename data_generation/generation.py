import os
import sys
import random
from datetime import datetime
import numpy as np

from faker import Faker
import psycopg2

num_records = int(os.getenv('NUM_RECORDS'))
time_to_connect = 10

time = datetime.now()
success = False
while not success:
    try:
        connection = psycopg2.connect(
            host="postgres",
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=os.getenv("POSTGRES_PORT"),

        )
        success = True
    except:
        success = False
    if datetime.now() - time > time_to_connect:
        sys.exit("Connection timed out")
print("Connected successfully")


class DataGenerator:
    def __init__(self):
        self.fake = Faker()

    def generate_photo(self):
        photo_bytes = bytes([random.randint(0, 255) for _ in range(100)])
        return photo_bytes

    def generate_rating(self):
        return random.randint(1, 5)



class UserGenerator(DataGenerator):
    def generate_user(self):
        user_name = self.fake.name()
        phone_number = self.fake.phone_number()
        email_address = self.fake.email()
        photo = self.generate_photo()
        password = self.fake.password()

        user = {
            "name": user_name,
            "phone_number": phone_number,
            "email_address": email_address,
            "photo": photo,
            "password": password
        }
        return user


class ShopGenerator(DataGenerator):
    def generate_shop(self):
        shop_name = self.fake.company()
        photo = self.generate_photo()
        address = self.fake.address()
        description = self.fake.text()
        legal_details = self.fake.text()
        password = self.fake.password()

        shop = {
            "name": shop_name,
            "photo": photo,
            "address": address,
            "description": description,
            "legal_details": legal_details,
            "password": password
        }
        return shop


class ReviewGenerator(DataGenerator):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn

    def get_random_uuid_from_table(self):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT uuid FROM ")
        rows = cursor.fetchall()
        uuids = [row[0] for row in rows]
        cursor.close()
        return random.choice(uuids)

    def generate_user_review(self):
        user_id = self.get_random_uuid_from_table('users')
        shop_id = self.get_random_uuid_from_table('shops')
        description = self.fake.text()
        rating = self.generate_rating()

        user_review = {
            "user_id": user_id,
            "shop_id": shop_id,
            "description": description,
            "rating": rating
        }
        return user_review

    def generate_shop_review(self):
        user_id = self.get_random_uuid_from_table('users')
        shop_id = self.get_random_uuid_from_table('shops')
        description = self.fake.text()
        matching_rating = self.generate_rating()
        service_rating = self.generate_rating()
        price_quality_rating = self.generate_rating()

        shop_review = {
            "user_id": user_id,
            "shop_id": shop_id,
            "description": description,
            "matching_rating": matching_rating,
            "service_rating": service_rating,
            "price_quality_rating": price_quality_rating
        }
        return shop_review


cursor = connection.cursor()

connection.commit()
connection.close()
