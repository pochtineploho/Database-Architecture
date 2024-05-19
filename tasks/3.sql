-- Магазин, в котором чаще всего заказывают
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
