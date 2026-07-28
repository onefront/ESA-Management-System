from datetime import datetime

from extensions import db


class ConversationMember(db.Model):

    __tablename__ = "conversation_members"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    conversation_id = db.Column(
        db.Integer,
        db.ForeignKey("conversations.id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    joined_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    is_admin = db.Column(
        db.Boolean,
        default=False
    )

    is_muted = db.Column(
        db.Boolean,
        default=False
    )

    conversation = db.relationship(
        "Conversation",
        backref=db.backref(
            "members",
            cascade="all, delete-orphan"
        )
    )

    user = db.relationship(
        "User",
        backref=db.backref(
            "conversation_memberships",
            passive_deletes=True
        ),
        passive_deletes=True
    )