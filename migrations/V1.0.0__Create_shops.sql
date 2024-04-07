CREATE TABLE IF NOT EXISTS Shops
(
    shop_id       uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name          VARCHAR(256) NOT NULL,
    photo         bytea,
    address       VARCHAR(300),
    description   TEXT,
    legal_details TEXT,
    password      VARCHAR
);