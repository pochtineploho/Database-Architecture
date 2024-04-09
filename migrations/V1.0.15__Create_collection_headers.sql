CREATE TABLE IF NOT EXISTS CollectionHeaders
(
    collection_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id       uuid NOT NULL REFERENCES Users (user_id),
    description   TEXT,
    public        BOOLEAN
);
