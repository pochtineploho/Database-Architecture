CREATE TABLE PriceHistory
(
    product_id uuid REFERENCES Products (product_id),
    time       TIMESTAMP,
    price      DECIMAL,
    PRIMARY KEY (product_id, time)
)