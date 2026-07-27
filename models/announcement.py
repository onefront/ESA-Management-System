from extensions import db
from datetime import datetime


class Announcement(db.Model):

    __tablename__ = "announcements"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=False
    )

    # Image (optional)
    image = db.Column(
        db.String(255),
        nullable=True
    )

    # Document (optional)
    attachment = db.Column(
        db.String(255),
        nullable=True
    )

    attachment_name = db.Column(
        db.String(255),
        nullable=True
    )

    attachment_type = db.Column(
        db.String(100),
        nullable=True
    )

    is_pinned = db.Column(
        db.Boolean,
        default=False
    )

    status = db.Column(
        db.String(20),
        default="Published"
    )

    expiry_date = db.Column(
        db.Date,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )