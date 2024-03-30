CREATE TABLE Shops
(
    shop_id       uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name          VARCHAR(256),
    photo         bytea,
    address       VARCHAR(300),
    description   TEXT,
    legal_details TEXT,
    password      VARCHAR
)