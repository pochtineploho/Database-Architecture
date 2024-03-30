CREATE TABLE CollectionHeaders
(
    collection_id uuid PRIMARY KEY,
    user_id       uuid REFERENCES Users (user_id),
    description   TEXT,
    public        BOOLEAN
)