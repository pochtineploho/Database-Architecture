CREATE TABLE IF NOT EXISTS OrderHeaders
(
    order_id    uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     uuid NOT NULL REFERENCES Users (user_id),
    status      order_status,
    time        TIMESTAMP,
    card_number VARCHAR(19)
);