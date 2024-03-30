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

CREATE TABLE IF NOT EXISTS DeliveryPrice
(
    shop_id   uuid REFERENCES Shops (shop_id),
    max_limit DECIMAL,
    price     DECIMAL,
    PRIMARY KEY (shop_id, max_limit)
);

CREATE TABLE IF NOT EXISTS Categories
(
    category_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name        VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS Subcategories
(
    subcategory_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name           VARCHAR NOT NULL,
    category_id    uuid REFERENCES Categories (category_id)
);

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

CREATE TABLE IF NOT EXISTS PriceHistory
(
    product_id uuid REFERENCES Products (product_id),
    time       TIMESTAMP NOT NULL,
    price      DECIMAL,
    PRIMARY KEY (product_id, time)
);

CREATE TABLE IF NOT EXISTS Structures
(
    product_id uuid REFERENCES Products (product_id),
    element    VARCHAR NOT NULL,
    quantity   INTEGER,
    PRIMARY KEY (product_id, element)
);

CREATE TABLE IF NOT EXISTS Users
(
    user_id       uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name          VARCHAR(256) NOT NULL,
    phone_number  VARCHAR(15) NOT NULL,
    email_address VARCHAR(320),
    photo         bytea,
    password      VARCHAR
);

CREATE TABLE IF NOT EXISTS ShoppingCarts
(
    user_id    uuid REFERENCES Users (user_id),
    product_id uuid REFERENCES Products (product_id),
    quantity   INTEGER,
    PRIMARY KEY (user_id, product_id)
);

DROP TYPE IF EXISTS order_status;
CREATE TYPE order_status AS ENUM ('CREATED', 'IN_PROGRESS', 'CANCELED', 'DELIVERED');

CREATE TABLE IF NOT EXISTS OrderHeaders
(
    order_id    uuid PRIMARY KEY,
    user_id     uuid NOT NULL REFERENCES Users (user_id),
    status      order_status,
    time        TIMESTAMP,
    card_number VARCHAR(19)
);

CREATE TABLE IF NOT EXISTS OrderDetails
(
    order_id   uuid REFERENCES OrderHeaders (order_id),
    product_id uuid REFERENCES Products (product_id),
    quantity   INTEGER,
    price      DECIMAL,
    PRIMARY KEY (order_id, product_id)
);

CREATE TABLE IF NOT EXISTS ShopReviews
(
    user_id              uuid REFERENCES Users (user_id),
    product_id           uuid REFERENCES Products (product_id),
    description          TEXT,
    photo                bytea,
    matching_rating      SMALLINT,
    service_rating       SMALLINT,
    price_quality_rating SMALLINT,
    PRIMARY KEY (user_id, product_id)
);

CREATE TABLE IF NOT EXISTS UserReviews
(
    user_id     uuid REFERENCES Users (user_id),
    shop_id     uuid REFERENCES Shops (shop_id),
    description TEXT,
    rating      SMALLINT,
    PRIMARY KEY (user_id, shop_id)
);

CREATE TABLE IF NOT EXISTS FavouriteLists
(
    user_id uuid REFERENCES Users (user_id),
    shop_id uuid REFERENCES Shops (shop_id),
    PRIMARY KEY (user_id, shop_id)
);

CREATE TABLE IF NOT EXISTS CollectionHeaders
(
    collection_id uuid PRIMARY KEY,
    user_id       uuid NOT NULL REFERENCES Users (user_id),
    description   TEXT,
    public        BOOLEAN
);

CREATE TABLE IF NOT EXISTS CollectionDetails
(
    collection_id uuid REFERENCES CollectionHeaders (collection_id),
    product_id    uuid REFERENCES Products (product_id),
    PRIMARY KEY (collection_id, product_id)
);

CREATE TABLE IF NOT EXISTS Dialogs
(
    dialog_id uuid PRIMARY KEY,
    user_id   uuid REFERENCES Users (user_id),
    shop_id   uuid REFERENCES Shops (shop_id)
);

CREATE TABLE IF NOT EXISTS Messages
(
    message_id      uuid PRIMARY KEY,
    dialog_id       uuid NOT NULL REFERENCES Dialogs (dialog_id),
    message         TEXT NOT NULL,
    time            TIMESTAMP,
    sender_is_user  BOOLEAN,
    message_is_read BOOLEAN
);