DROP TABLE PriceHistories;
CREATE TABLE IF NOT EXISTS PriceHistories
(
    product_id uuid REFERENCES Products (product_id),
    time       TIMESTAMP NOT NULL,
    price      DECIMAL,
    PRIMARY KEY (product_id, time)
) PARTITION BY RANGE (time);

CREATE TABLE IF NOT EXISTS PriceHistories_2019 PARTITION OF PriceHistories
    FOR VALUES FROM ('2019-01-01') TO ('2020-01-01');

CREATE TABLE IF NOT EXISTS PriceHistories_2020 PARTITION OF PriceHistories
    FOR VALUES FROM ('2020-01-01') TO ('2021-01-01');

CREATE TABLE IF NOT EXISTS PriceHistories_2021 PARTITION OF PriceHistories
    FOR VALUES FROM ('2021-01-01') TO ('2022-01-01');

CREATE TABLE IF NOT EXISTS PriceHistories_2022 PARTITION OF PriceHistories
    FOR VALUES FROM ('2022-01-01') TO ('2023-01-01');

CREATE TABLE IF NOT EXISTS PriceHistories_2023 PARTITION OF PriceHistories
    FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');

CREATE TABLE IF NOT EXISTS PriceHistories_2024 PARTITION OF PriceHistories
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');


-- CREATE TABLE IF NOT EXISTS PriceHistories_2024 (
--     product_id uuid REFERENCES Products (product_id),
--     time       TIMESTAMP NOT NULL,
--     price      DECIMAL,
--     PRIMARY KEY (product_id, time)
-- );
--
-- ALTER TABLE PriceHistories
--     ATTACH PARTITION PriceHistories_2024 FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
--
-- -- Повторяем для других партиций, если нужно
-- CREATE TABLE IF NOT EXISTS PriceHistories_2023 (
--     product_id uuid REFERENCES Products (product_id),
--     time       TIMESTAMP NOT NULL,
--     price      DECIMAL,
--     PRIMARY KEY (product_id, time)
-- );
--
-- ALTER TABLE PriceHistories
--     ATTACH PARTITION PriceHistories_2023 FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');
--
-- CREATE TABLE IF NOT EXISTS PriceHistories_2022 (
--     product_id uuid REFERENCES Products (product_id),
--     time       TIMESTAMP NOT NULL,
--     price      DECIMAL,
--     PRIMARY KEY (product_id, time)
-- );
--
-- ALTER TABLE PriceHistories
--     ATTACH PARTITION PriceHistories_2022 FOR VALUES FROM ('2022-01-01') TO ('2023-01-01');
--
-- CREATE TABLE IF NOT EXISTS PriceHistories_2021 (
--     product_id uuid REFERENCES Products (product_id),
--     time       TIMESTAMP NOT NULL,
--     price      DECIMAL,
--     PRIMARY KEY (product_id, time)
-- );
--
-- ALTER TABLE PriceHistories
--     ATTACH PARTITION PriceHistories_2021 FOR VALUES FROM ('2021-01-01') TO ('2022-01-01');
--
-- CREATE TABLE IF NOT EXISTS PriceHistories_2020 (
--     product_id uuid REFERENCES Products (product_id),
--     time       TIMESTAMP NOT NULL,
--     price      DECIMAL,
--     PRIMARY KEY (product_id, time)
-- );
--
-- ALTER TABLE PriceHistories
--     ATTACH PARTITION PriceHistories_2020 FOR VALUES FROM ('2020-01-01') TO ('2021-01-01');
--
-- CREATE TABLE IF NOT EXISTS PriceHistories_2019 (
--     product_id uuid REFERENCES Products (product_id),
--     time       TIMESTAMP NOT NULL,
--     price      DECIMAL,
--     PRIMARY KEY (product_id, time)
-- );
--
-- ALTER TABLE PriceHistories
--     ATTACH PARTITION PriceHistories_2019 FOR VALUES FROM ('2019-01-01') TO ('2020-01-01');
