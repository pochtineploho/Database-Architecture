CREATE TABLE Users
(
    user_id       uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name          VARCHAR(256),
    phone_number  VARCHAR(15),
    email_address VARCHAR(320),
    photo         bytea,
    password      VARCHAR
)