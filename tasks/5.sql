-- Самая продаваемая коллекция
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