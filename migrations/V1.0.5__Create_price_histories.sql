CREATE TABLE IF NOT EXISTS PriceHistories
(
    product_id uuid REFERENCES Products (product_id),
    time       TIMESTAMP NOT NULL,
    price      DECIMAL,
    PRIMARY KEY (product_id, time)
);