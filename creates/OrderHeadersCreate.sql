CREATE TYPE order_status AS ENUM ('CREATED', 'IN_PROGRESS', 'CANCELED', 'DELIVERED');

CREATE TABLE OrderHeaders
(
    order_id    uuid PRIMARY KEY,
    user_id     uuid REFERENCES Users (user_id),
    status      order_status,
    time        TIMESTAMP,
    card_number VARCHAR(19)
)
