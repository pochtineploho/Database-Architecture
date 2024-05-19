import os
import psycopg2
import statistics
from datetime import datetime


# Настройки базы данных через переменные окружения
def connect_db():
    return psycopg2.connect(
        host="postgres",
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=5432
    )


# Запросы для анализа
QUERIES = [
    """
    -- Получение статистики заказов своего магазина
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
    """,
    """
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
    """,
    """
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
    """,
    """
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
        total_purchases DESC;
    """
]


def explain_analyze_query(cursor, query):
    cursor.execute(f"EXPLAIN ANALYZE {query}")
    return cursor.fetchall()


def parse_cost(result):
    for line in result:
        if 'Total Cost' in line[0]:
            parts = line[0].split()
            return float(parts[parts.index('Total') + 2].replace(',', ''))
    return None


def save_results(filename, results):
    with open(filename, 'w') as f:
        for result in results:
            f.write(f"{result}\n")


def main():
    conn = connect_db()
    cursor = conn.cursor()

    attempts = int(os.getenv('ATTEMPTS', 3))  # Количество попыток к каждому запросу, по умолчанию 3

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_dir = "query_performance_results"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"performance_{timestamp}.txt")

    all_results = []

    for i, query in enumerate(QUERIES):
        print(f"Running query {i + 1}")
        costs = []
        for attempt in range(attempts):
            results = explain_analyze_query(cursor, query)
            cost = parse_cost(results)
            if cost is not None:
                costs.append(cost)

        if costs:
            best_case = min(costs)
            worst_case = max(costs)
            avg_case = statistics.mean(costs)
            all_results.append(
                f"Query {i + 1} results:\nBest Case: {best_case}\nAverage Case: {avg_case}\nWorst Case: {worst_case}\n\n")
        else:
            all_results.append(f"Query {i + 1} results: No valid results\n\n")

    save_results(output_file, all_results)

    cursor.close()
    conn.close()
    print(f"Results saved to {output_file}")


if __name__ == "__main__":
    main()
