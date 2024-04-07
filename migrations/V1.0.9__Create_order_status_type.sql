DO
$$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'order_status') THEN
            CREATE TYPE order_status AS ENUM ('CREATED', 'IN_PROGRESS', 'CANCELED', 'DELIVERED');
        end if;
    END
$$;