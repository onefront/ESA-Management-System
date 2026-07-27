from datetime import datetime

from extensions import db


class Attachment(db.Model):

    __tablename__ = "attachments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    message_id = db.Column(
        db.Integer,
        db.ForeignKey("messages.id"),
        nullable=False
    )

    filename = db.Column(
        db.String(255),
        nullable=False
    )

    filepath = db.Column(
        db.String(500),
        nullable=False
    )

    filetype = db.Column(
        db.String(255),
        nullable=True
    )

    filesize = db.Column(
        db.Integer,
        nullable=True
    )

    uploaded_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    message = db.relationship(
        "Message",
        backref=db.backref(
            "attachments",
            cascade="all, delete-orphan"
        )
    )

    @property
    def formatted_size(self):
        size = self.filesize or 0

        if size < 1024:
            return f"{size} B"

        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"

        elif size < 1024 * 1024 * 1024:
            return f"{size / (1024 * 1024):.1f} MB"

        return f"{size / (1024 * 1024 * 1024):.1f} GB"