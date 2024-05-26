import decimal
import os
import random
import sys
import uuid
from bisect import bisect_left, bisect_right
from datetime import datetime, timedelta

import psycopg2
from faker import Faker

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

# Users = n
# Shops = n/5
# Categories = 21
# Subcategories = 210
# Delivery prices = 2n/5
# Products = n
# PriceHistories = 2n participant
# Structures = 1.5n
# FavoriteLists = n
# OrderHeaders = 2n/3
# OrderDetails = 2n
# UserReviews = n/3
# ShopReviews = n/3
# CollectionHeaders = n/5
# CollectionDetails = n
# Dialogs = n/5
# Messages = n
# Shopping Carts = n


for _ in range(num_records):
    user_name = fake.name()
    phone_number = generate_phone_number()
    email_address = fake.email()
    photo = generate_photo()
    password = fake.password()
    cur.execute("""
    INSERT INTO Users (name, phone_number, email_address, photo, password)
    VALUES (%s, %s, %s, %s, %s)
    """, (user_name, phone_number, email_address, photo, password))
print("Users generated")

cur.execute("SELECT user_id FROM Users")
users_t = cur.fetchall()
users = [tup[0] for tup in users_t]

for _ in range(num_records // 5):
    shop_name = fake.company()
    photo = generate_photo()
    address = fake.address()
    description = fake.sentence()
    legal_details = fake.sentence()
    password = fake.password()
    cur.execute("""
    INSERT INTO Shops (name, photo, address, description, legal_details, password)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, (shop_name, photo, address, description, legal_details, password))
print("Shops generated")

cur.execute("SELECT shop_id FROM Shops")
shops_t = cur.fetchall()
shops = [tup[0] for tup in shops_t]

for category in category_names:
    cur.execute("""
       INSERT INTO Categories (name)
       VALUES (%s)
       """, (category,))
print("Categories generated")

for category in category_names:
    cur.execute("""
                   SELECT category_id FROM Categories 
                    WHERE name = %s
                   """, (category,))
    category_id = cur.fetchone()[0]

    for _ in range(10):
        subcategory = fake.word()
        cur.execute("""
               INSERT INTO Subcategories (name, category_id)
               VALUES (%s, %s)
               """, (subcategory, category_id))
print("Subcategories generated")

cur.execute("SELECT subcategory_id FROM Subcategories")
subcategories_t = cur.fetchall()
subcategories = [tup[0] for tup in subcategories_t]

available_max_limits = list(range(1000, 10001, 1000))
for shop_id in shops:
    num_products = random.randint(0, 2)  # Случайное количество лимитов для магазина
    max_limits = available_max_limits[:]
    max_limit_exists = False

    # Вставка данных в таблицу deliveryPrices
    for _ in range(random.randint(1, 4)):
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

for shop_id in shops:
    num_products = random.randint(3, 7)  # Случайное количество продуктов для магазина
    for _ in range(num_products):
        name = fake.word()
        subcategory_id = random.choice(subcategories)
        photo = generate_photo()
        description = fake.sentence()
        width = random.randint(100, 300)
        height = random.randint(100, 300)
        cur.execute("""
                INSERT INTO Products (name, subcategory_id, photo, description, shop_id, width, height)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (name, subcategory_id, photo, description, shop_id, width, height))
print("Products generated")

cur.execute("SELECT product_id, shop_id FROM Products")
products_t = cur.fetchall()
products = [(product_id, shop_id) for product_id, shop_id in products_t]
products.sort(key=lambda x: x[1])

for product in products:
    num_history = random.randint(1, 3)
    rnd_start_date = datetime.now() - timedelta(days=4 * 365)
    rnd_end_date = datetime.now() - timedelta(days=400)
    for _ in range(num_history):
        price = random.randint(100, 10000)
        time = fake.date_time_between(start_date=rnd_start_date, end_date=rnd_end_date)
        cur.execute("""
                    INSERT INTO PriceHistories (product_id, time, price)
                    VALUES (%s, %s, %s)
                        """, (product[0], time, price))

    num_structure = random.randint(0, 3)

    used_words = []
    for _ in range(num_structure):
        element = fake.word()
        while element in used_words:
            element = fake.word()
        used_words.append(element)
        quantity = random.randint(1, 10)
        cur.execute("""
                        INSERT INTO Structures (product_id, element, quantity)
                         VALUES (%s, %s, %s)
                        """, (product[0], element, quantity))
print("Structures and price histories generated")

for i in range(num_records // 3):
    random_user = users[i * 2]
    used_shops = []
    for shop in range(random.randint(1, 5)):
        random_shop = random.choice(shops)
        while random_shop in used_shops:
            random_shop = random.choice(shops)
        used_shops.append(random_shop)
        cur.execute("""
                        INSERT INTO favoritelists (user_id, shop_id)
                        VALUES (%s, %s)
                        """, (random_user, random_shop))
print("Favorite lists generated")

statuses = ['CREATED', 'IN_PROGRESS', 'CANCELED', 'DELIVERED']
percent = 2 * num_records // 3 // 10
for _ in range(2 * num_records // 3):
    if _ % percent == 0 and _ > 0:
        print(str(_ // percent * 10) + "% of orders")

    random_user = random.choice(users)
    order_id = str(uuid.uuid4())
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
    start = bisect_left(products, random_shop, key=lambda x: x[1])
    end = bisect_right(products, random_shop, key=lambda x: x[1])
    shop_products = products[start:end]
    products_for_rating = []
    used_products = []

    for order_details in range(random.randint(1, len(shop_products))):
        quantity = random.randint(1, 10)
        chosen_product = random.choice(shop_products)[0]
        while chosen_product in used_products:
            chosen_product = random.choice(shop_products)[0]
        used_products.append(chosen_product)

        products_for_rating.append(chosen_product)
        cur.execute("""
                            SELECT price 
                            FROM pricehistories 
                            WHERE product_id = %s
                            AND time <= %s
                            ORDER BY time DESC 
                            LIMIT 1;
                            """, (chosen_product, time))
        price = cur.fetchone()
        cur.execute("""
                            INSERT INTO orderdetails (order_id, product_id, quantity, price)
                            VALUES (%s, %s, %s, %s)
                            """, (order_id, chosen_product, quantity, price))

    if fake.pybool():
        description = fake.sentence()
        rating = generate_rating()
        try:

            cur.execute("""
                                INSERT INTO userreviews (user_id, shop_id, description, rating)
                                VALUES (%s, %s, %s, %s)
                            """, (random_user, random_shop, description, rating))

        except psycopg2.Error as e:
            connection.rollback()

    if fake.pybool():
        product = random.choice(products_for_rating)
        try:
            description = fake.sentence()
            rating_1 = generate_rating()
            rating_2 = generate_rating()
            rating_3 = generate_rating()
            photo = generate_photo()
            cur.execute("""
                                INSERT INTO shopreviews (user_id, product_id, description, photo, matching_rating, service_rating, price_quality_rating)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)
                                """,
                        (random_user, product, description, photo, rating_1, rating_2, rating_3))
        except psycopg2.Error as e:
            connection.rollback()
print("Orders generated")
print("Reviews generated")

for _ in range(num_records // 5):
    collection_id = str(uuid.uuid4())
    user_id = random.choice(users)
    description = fake.sentence()
    public = fake.pybool()
    cur.execute("""
                        INSERT INTO collectionheaders (collection_id, user_id, description, public)
                        VALUES (%s, %s, %s, %s)
                        """, (collection_id, user_id, description, public))
    used_products = []
    for i in range(random.randint(1, 10)):
        product = random.choice(products)[0]
        while product in used_products:
            product = random.choice(products)[0]
        used_products.append(product)
        cur.execute("""
                            INSERT INTO collectiondetails (collection_id, product_id)
                            VALUES (%s, %s)
                            """, (collection_id, product))

print("Collections generated")

for _ in range(num_records // 5):
    dialog_id = str(uuid.uuid4())
    random_user = random.choice(users)
    random_shop = random.choice(shops)
    cur.execute("""
                        INSERT INTO dialogs (dialog_id, user_id, shop_id)
                        VALUES (%s, %s, %s)
                        """, (dialog_id, random_user, random_shop))

    for i in range(random.randint(1, 10)):
        message = fake.sentence()
        sender_is_user = fake.pybool()
        message_is_read = False
        time = fake.date_this_year()
        cur.execute("""
                            INSERT INTO messages (dialog_id, message, time, sender_is_user, message_is_read)
                            VALUES (%s, %s, %s, %s, %s)
                            """, (dialog_id, message, time, sender_is_user, message_is_read))
print("Dialogs and messages generated")

counter = 0
for user in users:
    counter += 1
    if (counter % 5) == 0:
        used_products = []
        for i in range(random.randint(1, 10)):
            product = random.choice(products)[0]
            while product in used_products:
                product = random.choice(products)[0]
            used_products.append(product)
            quantity = random.randint(1, 10)
            cur.execute("""
                                INSERT INTO shoppingcarts (user_id, product_id, quantity)
                                VALUES (%s, %s, %s)
                                """, (user, product, quantity))
print("Shopping carts generated")
print("Done")

cur.close()
connection.commit()
connection.close()
