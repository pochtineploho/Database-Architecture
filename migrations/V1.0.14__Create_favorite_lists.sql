CREATE TABLE IF NOT EXISTS FavoriteLists
(
    user_id uuid REFERENCES Users (user_id),
    shop_id uuid REFERENCES Shops (shop_id),
    PRIMARY KEY (user_id, shop_id)
);