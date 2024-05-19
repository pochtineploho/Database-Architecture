import os
import psycopg2
import datetime


def connect_db():
    return psycopg2.connect(
        host="postgres",
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=os.getenv("POSTGRES_PORT")
    )


def run_explain_analyze(query, attempts):
    costs = []
    with connect_db() as conn:
        with conn.cursor() as cursor:
            for _ in range(attempts):
                cursor.execute(f"EXPLAIN ANALYZE {query}")
                result = cursor.fetchall()
                for row in result:
                    if "Total Cost" in row[0]:
                        cost = float(row[0].split('=')[-1].split(' ')[0])
                        costs.append(cost)
    return costs


def write_results(query_name, costs):
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filepath = f"/src/query_performance_results/{query_name}_{timestamp}.txt"
    with open(filepath, 'w') as file:
        file.write(f"Query: {query_name}\n")
        file.write(f"Best Case: {min(costs)}\n")
        file.write(f"Average Case: {sum(costs) / len(costs)}\n")
        file.write(f"Worst Case: {max(costs)}\n")


if __name__ == "__main__":
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
                    s.name AS shop_name,
                    p.name AS product_name
                FROM
                    Shops s
                JOIN
                    Products p ON s.shop_id = p.shop_id
                ORDER BY
                    p.name, s.name;
            """
        },
        {
            "name": "Customer Statistics",
            "query": """
                SELECT
                    u.user_id,
                    u.name AS user_name,
                    s.name AS most_frequent_shop,
                    p.name AS most_frequent_product
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
                    u.user_id, u.name, s.name, p.name
                ORDER BY
                    COUNT(oh.order_id) DESC
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
