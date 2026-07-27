from datetime import datetime

from extensions import db


class ChatBlock(db.Model):

    __tablename__ = "chat_blocks"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    blocked_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    reason = db.Column(
        db.String(255),
        nullable=True
    )

    blocked_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        foreign_keys=[user_id],
        backref=db.backref(
            "chat_block",
            uselist=False,
            cascade="all, delete-orphan"
        )
    )

    administrator = db.relationship(
        "User",
        foreign_keys=[blocked_by]
    )