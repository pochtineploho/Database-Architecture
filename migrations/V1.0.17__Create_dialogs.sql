CREATE TABLE IF NOT EXISTS Dialogs
(
    dialog_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id   uuid REFERENCES Users (user_id),
    shop_id   uuid REFERENCES Shops (shop_id)
);