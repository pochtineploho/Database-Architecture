CREATE TABLE IF NOT EXISTS Messages
(
    message_id      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    dialog_id       uuid NOT NULL REFERENCES Dialogs (dialog_id),
    message         TEXT NOT NULL,
    time            TIMESTAMP,
    sender_is_user  BOOLEAN,
    message_is_read BOOLEAN
);