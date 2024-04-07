CREATE TABLE IF NOT EXISTS Products
(
    product_id     uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name           VARCHAR(256) NOT NULL,
    subcategory_id uuid REFERENCES Subcategories (subcategory_id),
    photo          bytea,
    description    TEXT,
    shop_id        uuid REFERENCES Shops (shop_id),
    width          INTEGER,
    height         INTEGER
);