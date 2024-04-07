CREATE TABLE IF NOT EXISTS ShoppingCarts
(
    user_id    uuid REFERENCES Users (user_id),
    product_id uuid REFERENCES Products (product_id),
    quantity   INTEGER,
    PRIMARY KEY (user_id, product_id)
);