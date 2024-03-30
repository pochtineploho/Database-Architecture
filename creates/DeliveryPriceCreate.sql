CREATE TABLE DeliveryPrice
(
    shop_id   uuid REFERENCES Shops (shop_id),
    max_limit DECIMAL,
    price     DECIMAL,
    PRIMARY KEY (shop_id, max_limit)
)