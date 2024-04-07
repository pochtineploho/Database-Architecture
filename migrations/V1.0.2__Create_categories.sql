CREATE TABLE IF NOT EXISTS Categories
(
    category_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name        VARCHAR NOT NULL
);