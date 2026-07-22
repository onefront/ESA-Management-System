from extensions import db
from datetime import datetime


class Notice(db.Model):

    __tablename__ = "notices"

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

    category = db.Column(
        db.String(50),
        default="General"
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