CREATE TABLE IF NOT EXISTS UserReviews
(
    user_id     uuid REFERENCES Users (user_id),
    shop_id     uuid REFERENCES Shops (shop_id),
    description TEXT,
    rating      SMALLINT,
    PRIMARY KEY (user_id, shop_id)
);