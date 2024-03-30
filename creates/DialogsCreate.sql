CREATE TABLE Dialogs
(
    dialog_id uuid PRIMARY KEY,
    user_id   uuid REFERENCES Users (user_id),
    shop_id   uuid REFERENCES Shops (shop_id)
)