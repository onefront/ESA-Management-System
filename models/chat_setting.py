from datetime import datetime

from extensions import db


class ChatSetting(db.Model):
    __tablename__ = "chat_settings"

    id = db.Column(db.Integer, primary_key=True)

    chat_enabled = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    maintenance_mode = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    member_to_member = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    member_to_admin = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    allow_attachments = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    max_upload_mb = db.Column(
        db.Integer,
        default=10,
        nullable=False
    )

    max_message_length = db.Column(
        db.Integer,
        default=5000,
        nullable=False
    )

    allow_edit = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    allow_delete = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    welcome_message = db.Column(
        db.Text,
        default="Welcome to ESA VIBES.",
        nullable=True
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