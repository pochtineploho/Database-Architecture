-- Сортировка товаров и магазинов по рейтингу и названию
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