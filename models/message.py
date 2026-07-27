from datetime import datetime

from extensions import db


class Message(db.Model):

    __tablename__ = "messages"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    conversation_id = db.Column(
        db.Integer,
        db.ForeignKey("conversations.id"),
        nullable=False
    )

    sender_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=False
    )
    reply_to_id = db.Column(
        db.Integer,
        db.ForeignKey("messages.id"),
        nullable=True
    )

    edited = db.Column(
        db.Boolean,
        default=False
    )

    edited_at = db.Column(
        db.DateTime,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    conversation = db.relationship(
        "Conversation",
        backref=db.backref(
            "messages",
            cascade="all, delete-orphan",
            order_by="Message.created_at"
        )
    )

    sender = db.relationship(
        "User",
        backref="sent_messages"
    )

    reply_to = db.relationship(
        "Message",
        remote_side=[id],
        backref="replies"
    )