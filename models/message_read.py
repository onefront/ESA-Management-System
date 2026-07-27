from datetime import datetime

from extensions import db


class MessageRead(db.Model):

    __tablename__ = "message_reads"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    message_id = db.Column(
        db.Integer,
        db.ForeignKey("messages.id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    read_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    message = db.relationship(
        "Message",
        backref=db.backref(
            "read_receipts",
            cascade="all, delete-orphan"
        )
    )

    user = db.relationship(
        "User",
        backref="message_reads"
    )