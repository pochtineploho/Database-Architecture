CREATE TABLE IF NOT EXISTS CollectionHeaders
(
    collection_id uuid PRIMARY KEY,
    user_id       uuid NOT NULL REFERENCES Users (user_id),
    description   TEXT,
    public        BOOLEAN
);
