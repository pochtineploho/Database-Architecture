CREATE TABLE IF NOT EXISTS CollectionDetails
(
    collection_id uuid REFERENCES CollectionHeaders (collection_id),
    product_id    uuid REFERENCES Products (product_id),
    PRIMARY KEY (collection_id, product_id)
);