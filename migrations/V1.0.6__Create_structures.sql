CREATE TABLE IF NOT EXISTS Structures
(
    product_id uuid REFERENCES Products (product_id),
    element    VARCHAR NOT NULL,
    quantity   INTEGER,
    PRIMARY KEY (product_id, element)
);