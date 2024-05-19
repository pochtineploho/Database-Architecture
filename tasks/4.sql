-- Самый часто заказываемый товар
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