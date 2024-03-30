CREATE TABLE Messages
(
    message_id      uuid PRIMARY KEY,
    dialog_id       uuid REFERENCES Dialogs (dialog_id),
    message         TEXT,
    time            TIMESTAMP,
    sender_is_user  BOOLEAN,
    message_is_read BOOLEAN
)