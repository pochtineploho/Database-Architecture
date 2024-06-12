import decimal
import os
import random
import sys
import uuid
from bisect import bisect_left, bisect_right
from datetime import datetime, timedelta

import psycopg2
from faker import Faker

errs = 0
num_records = int(os.getenv('NUM_RECORDS'))
time_to_connect = 60

time = datetime.now()
success = False
while not success:
    try:
        connection = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host="postgres",
            port=5432,
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

def generate_phone_number():
    r_phone_number = "+7"
    for _ in range(10):
        r_phone_number += str(random.randint(0, 9))
    return r_phone_number


def generate_photo():
    photo_bytes = bytes([random.randint(0, 255) for _ in range(100)])
    return photo_bytes


def generate_rating():
    return random.randint(1, 5)


category_names = ["Flowers and Gifts", "Confectionery and Bakeries", "Live Plants", "Cosmetics and Perfumes",
                  "Tea and Coffee", "Jewelry", "Food and Drinks", "Decor", "Tableware", "Accessories",
                  "Clothing", "Children's Clothing", "Handmade and Hobbies", "Party Supplies", "Books", "Paintings",
                  "Pet Supplies", "Gift Certificates", "Home Goods", "Stationery Supplies", "Other"]

cur = connection.cursor()

cur.execute("SELECT user_id FROM Users")
users_t = cur.fetchall()
users = [tup[0] for tup in users_t]

cur.execute("SELECT product_id, shop_id FROM Products")
products_t = cur.fetchall()
products = [(product_id, shop_id) for product_id, shop_id in products_t]
products.sort(key=lambda x: x[1])

cur.execute("SELECT shop_id FROM Shops")
shops_t = cur.fetchall()
shops = [tup[0] for tup in shops_t]

ur = {}
for _ in range(2 * num_records // 3):
    random_user = random.choice(users)
    random_shop = random.choice(shops)

    if fake.pybool() and not (random_user in ur and random_shop in ur[random_user]):
        if random_user in ur:
            ur[random_user].append(random_shop)
        else:
            ur[random_user] = [random_shop]
        description = fake.sentence()
        rating = generate_rating()
        try:
            cur.execute("""
                                INSERT INTO userreviews (user_id, shop_id, description, rating)
                                VALUES (%s, %s, %s, %s)
                            """, (random_user, random_shop, description, rating))

        except psycopg2.Error as e:
            errs = errs + 1
print("Reviews generated")

cur.close()
connection.commit()
connection.close()
