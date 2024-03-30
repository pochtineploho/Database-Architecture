CREATE TABLE Subcategories
(
    subcategory_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name           VARCHAR,
    category_id    uuid REFERENCES Categories (category_id)
)