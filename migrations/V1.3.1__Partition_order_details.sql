DROP TABLE OrderDetails;
CREATE TABLE IF NOT EXISTS OrderDetails
(
    order_id   UUID,
    product_id UUID,
    quantity   INT,
    price      DECIMAL,
    PRIMARY KEY (order_id, product_id)
) PARTITION BY RANGE (order_id);

-- Creating partitions for different UUID ranges
CREATE TABLE IF NOT EXISTS OrderDetails_p1 PARTITION OF OrderDetails
    FOR VALUES FROM ('00000000-0000-0000-0000-000000000000') TO ('40000000-0000-0000-0000-000000000000');

CREATE TABLE IF NOT EXISTS OrderDetails_p2 PARTITION OF OrderDetails
    FOR VALUES FROM ('40000000-0000-0000-0000-000000000000') TO ('80000000-0000-0000-0000-000000000000');

CREATE TABLE IF NOT EXISTS OrderDetails_p3 PARTITION OF OrderDetails
    FOR VALUES FROM ('80000000-0000-0000-0000-000000000000') TO ('c0000000-0000-0000-0000-000000000000');

CREATE TABLE IF NOT EXISTS OrderDetails_p4 PARTITION OF OrderDetails
    FOR VALUES FROM ('c0000000-0000-0000-0000-000000000000') TO ('ffffffff-ffff-ffff-ffff-ffffffffffff');

CREATE TABLE IF NOT EXISTS OrderDetails_p1 (
    order_id   UUID,
    product_id UUID,
    quantity   INT,
    price      DECIMAL,
    PRIMARY KEY (order_id, product_id)
);

CREATE TABLE IF NOT EXISTS OrderDetails_p2 (
    order_id   UUID,
    product_id UUID,
    quantity   INT,
    price      DECIMAL,
    PRIMARY KEY (order_id, product_id)
);

CREATE TABLE IF NOT EXISTS OrderDetails_p3 (
    order_id   UUID,
    product_id UUID,
    quantity   INT,
    price      DECIMAL,
    PRIMARY KEY (order_id, product_id)
);

CREATE TABLE IF NOT EXISTS OrderDetails_p4 (
    order_id   UUID,
    product_id UUID,
    quantity   INT,
    price      DECIMAL,
    PRIMARY KEY (order_id, product_id)
);

-- ALTER TABLE OrderDetails
--     ATTACH PARTITION OrderDetails_p1 FOR VALUES FROM ('00000000-0000-0000-0000-000000000000') TO ('40000000-0000-0000-0000-000000000000');
--
-- ALTER TABLE OrderDetails
--     ATTACH PARTITION OrderDetails_p2 FOR VALUES FROM ('40000000-0000-0000-0000-000000000000') TO ('80000000-0000-0000-0000-000000000000');
--
-- ALTER TABLE OrderDetails
--     ATTACH PARTITION OrderDetails_p3 FOR VALUES FROM ('80000000-0000-0000-0000-000000000000') TO ('c0000000-0000-0000-0000-000000000000');
--
-- ALTER TABLE OrderDetails
--     ATTACH PARTITION OrderDetails_p4 FOR VALUES FROM ('c0000000-0000-0000-0000-000000000000') TO ('ffffffff-ffff-ffff-ffff-ffffffffffff');