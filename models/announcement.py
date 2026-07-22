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