--Получение статистики заказов своего магазина
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
-- WHERE
--     s.shop_id = %shop_id%
GROUP BY
    s.shop_id, s.name
-- Вместо WHERE напишем вот это:
ORDER BY
    total_revenue DESC
LIMIT 1;