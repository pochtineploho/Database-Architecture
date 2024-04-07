CREATE TABLE IF NOT EXISTS Subcategories
(
    subcategory_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name           VARCHAR NOT NULL,
    category_id    uuid REFERENCES Categories (category_id)
);