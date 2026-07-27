from datetime import datetime
from extensions import db


class ClassNotice(db.Model):
    __tablename__ = "class_notices"

    id = db.Column(db.Integer, primary_key=True)

    class_group_id = db.Column(
        db.Integer,
        db.ForeignKey("class_groups.id"),
        nullable=False
    )

    created_by_user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    message = db.Column(
        db.Text,
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

    status = db.Column(
        db.String(20),
        default="Active"
    )

    class_group = db.relationship(
        "ClassGroup",
        backref="class_notices"
    )

    created_by = db.relationship(
        "User",
        backref="class_notices"
    )