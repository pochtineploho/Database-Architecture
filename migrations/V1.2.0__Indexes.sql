CREATE INDEX IF NOT EXISTS idx_shops_id ON Shops (shop_id);
CREATE INDEX IF NOT EXISTS idx_products_shop_id ON Products (shop_id);
CREATE INDEX IF NOT EXISTS idx_order_details_order_id ON OrderDetails (order_id);
CREATE INDEX IF NOT EXISTS idx_shop_reviews_product_id ON ShopReviews (product_id);
CREATE INDEX IF NOT EXISTS idx_user_reviews_product_id ON UserReviews (shop_id);
CREATE INDEX IF NOT EXISTS idx_order_headers_user_id ON OrderHeaders (user_id);
CREATE INDEX IF NOT EXISTS idx_order_details_product_id ON OrderDetails (product_id);
CREATE INDEX IF NOT EXISTS idx_collection_details_collection_id ON CollectionDetails (collection_id);