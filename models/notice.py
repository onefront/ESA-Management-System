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

    # Optional flyer/image
    image = db.Column(
        db.String(255),
        nullable=True
    )

    # Optional document attachment
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