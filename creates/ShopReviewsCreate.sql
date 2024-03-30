CREATE TABLE ShopReviews
(
    user_id              uuid REFERENCES Users (user_id),
    product_id           uuid REFERENCES Products (product_id),
    description          TEXT,
    photo                bytea,
    matching_rating      SMALLINT,
    service_rating       SMALLINT,
    price_quality_rating SMALLINT,
    PRIMARY KEY (user_id, product_id)
)