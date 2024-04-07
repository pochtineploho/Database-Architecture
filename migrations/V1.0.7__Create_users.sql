CREATE TABLE IF NOT EXISTS Users
(
    user_id       uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name          VARCHAR(256) NOT NULL,
    phone_number  VARCHAR(15)  NOT NULL,
    email_address VARCHAR(320),
    photo         bytea,
    password      VARCHAR
);