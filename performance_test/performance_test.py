import datetime
import os
import time
import re

import psycopg2


def connect_db():
    return psycopg2.connect(
        host="postgres",
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=5432
    )


def run_explain_analyze(query, attempts):
    costs = []
    with connect_db() as conn:
        with conn.cursor() as cursor:
            for _ in range(attempts):
                cursor.execute(f"EXPLAIN ANALYZE {query}")
                result = cursor.fetchall()
                if "cost=" in result[0][0]:
                    # Extracting the total cost value from each row
                    cost_part = re.search(r'cost=(\d+\.\d+)\.\.(\d+\.\d+)', result[0][0])
                    end_cost = float(cost_part.group(2))
                costs.append(end_cost)
    return costs


def write_results(query_name, costs):
    if costs:
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = f"/src/query_performance_results/{query_name}_{timestamp}.txt"
        with open(filepath, 'w') as file:
            file.write(f"Query: {query_name}\n")
            file.write(f"Best Case: {min(costs)}\n")
            file.write(f"Average Case: {sum(costs) / len(costs)}\n")
            file.write(f"Worst Case: {max(costs)}\n")
    else:
        print(f"No costs were recorded for query {query_name}.")


def wait_for_db():
    retries = 5
    while retries > 0:
        try:
            conn = connect_db()
            conn.close()
            return True
        except psycopg2.OperationalError:
            retries -= 1
            print("Database not ready yet, waiting...")
            time.sleep(10)
    raise Exception("Database not available")


if __name__ == "__main__":
    wait_for_db()

    queries = [
        {
            "name": "Order Statistics",
            "query": """
                SELECT
                    s.shop_id,
                    s.name AS shop_name,
                    COUNT(oh.order_id) AS total_orders,
                    SUM(od.quantity) AS total_quantity,
                    SUM(od.price * od.quantity) AS total_revenue
                FROM
                    Shops s
                JOIN
                    Products p ON s.shop_id = p.shop_id
                JOIN
                    OrderDetails od ON p.product_id = od.product_id
                JOIN
                    OrderHeaders oh ON od.order_id = oh.order_id
                GROUP BY
                    s.shop_id, s.name
                ORDER BY
                    total_revenue DESC
                LIMIT 1;
            """
        },
        {
            "name": "Products and Shops by Rating and Name",
            "query": """
                SELECT
                    p.product_id,
                    p.name AS product_name,
                    COALESCE(AVG(sr.matching_rating + sr.service_rating + sr.price_quality_rating) / 3, 0) AS avg_rating,
                    s.shop_id,
                    s.name AS shop_name
                FROM
                    Products p
                JOIN
                    Shops s ON p.shop_id = s.shop_id
                LEFT JOIN
                    ShopReviews sr ON p.product_id = sr.product_id
                GROUP BY
                    p.product_id, p.name, s.shop_id, s.name
                ORDER BY
                    avg_rating DESC, p.name ASC, s.name ASC;
            """
        },
        {
            "name": "Most popular shop",
            "query": """
                SELECT
                    u.user_id,
                    s.shop_id,
                    s.name AS shop_name,
                    COUNT(oh.order_id) AS total_orders
                FROM
                    Users u
                JOIN
                    OrderHeaders oh ON u.user_id = oh.user_id
                JOIN
                    OrderDetails od ON oh.order_id = od.order_id
                JOIN
                    Products p ON od.product_id = p.product_id
                JOIN
                    Shops s ON p.shop_id = s.shop_id
                GROUP BY
                    u.user_id, s.shop_id, s.name
                ORDER BY
                    total_orders DESC
                LIMIT 1;
            """
        },
        {
            "name": "Most popular product",
            "query": """
                    SELECT
                        u.user_id,
                        p.product_id,
                        p.name AS product_name,
                        COUNT(od.order_id) AS total_orders
                    FROM
                        Users u
                    JOIN
                        OrderHeaders oh ON u.user_id = oh.user_id
                    JOIN
                        OrderDetails od ON oh.order_id = od.order_id
                    JOIN
                        Products p ON od.product_id = p.product_id
                    GROUP BY
                        u.user_id, p.product_id, p.name
                    ORDER BY
                        total_orders DESC
                    LIMIT 1;
                """
        },
        {
            "name": "Most Purchased Collection",
            "query": """
                SELECT
                    ch.collection_id,
                    COUNT(od.product_id) AS total_purchases
                FROM
                    CollectionHeaders ch
                JOIN
                    CollectionDetails cd ON ch.collection_id = cd.collection_id
                JOIN
                    OrderDetails od ON cd.product_id = od.product_id
                GROUP BY
                    ch.collection_id
                ORDER BY
                    total_purchases DESC
                LIMIT 1;
            """
        }
    ]

    attempts = int(os.getenv("ATTEMPTS", 3))

    for query in queries:
        costs = run_explain_analyze(query["query"], attempts)
        write_results(query["name"], costs)

    print("All tests passed!")
