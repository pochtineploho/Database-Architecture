CREATE TABLE OrderDetails
(
    order_id   uuid REFERENCES OrderHeaders (order_id),
    product_id uuid REFERENCES Products (product_id),
    quantity   INTEGER,
    price      DECIMAL,
    PRIMARY KEY (order_id, product_id)
)