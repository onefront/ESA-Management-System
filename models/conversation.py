from datetime import datetime

from extensions import db

messages = db.relationship(
    "Message",
    backref="conversation",
    order_by="Message.created_at"
)
class Conversation(db.Model):

    __tablename__ = "conversations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    conversation_type = db.Column(
        db.String(20),
        nullable=False,
        default="private"
    )  # private | group | broadcast

    title = db.Column(
        db.String(150),
        nullable=True
    )

    created_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    creator = db.relationship(
        "User",
        back_populates="created_conversations",
        passive_deletes=True
    )


