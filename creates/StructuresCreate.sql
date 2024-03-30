CREATE TABLE Structures
(
    product_id uuid REFERENCES Products (product_id),
    element    VARCHAR,
    quantity   INTEGER,
    PRIMARY KEY (product_id, element)
)