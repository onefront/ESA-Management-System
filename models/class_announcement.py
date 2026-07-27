from datetime import datetime, date, time

from extensions import db


class ClassAnnouncement(db.Model):
    __tablename__ = "class_announcements"

    id = db.Column(db.Integer, primary_key=True)

    class_group_id = db.Column(
        db.Integer,
        db.ForeignKey("class_groups.id"),
        nullable=False
    )

    created_by = db.Column(
        db.Integer,
        db.ForeignKey("members.id"),
        nullable=False
    )

    title = db.Column(db.String(200), nullable=False)

    message = db.Column(db.Text, nullable=False)

    # Optional attachment
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

    event_date = db.Column(
        db.Date,
        nullable=True
    )

    event_time = db.Column(
        db.Time,
        nullable=True
    )

    venue = db.Column(
        db.String(200),
        nullable=True
    )

    is_pinned = db.Column(
        db.Boolean,
        default=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    class_group = db.relationship(
        "ClassGroup",
        backref="announcements"
    )
    author = db.relationship(
        "Member",
        backref="class_announcements",
        foreign_keys=[created_by]
    )


