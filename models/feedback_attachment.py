from datetime import datetime
from extensions import db


class FeedbackAttachment(db.Model):
    __tablename__ = "feedback_attachments"

    id = db.Column(db.Integer, primary_key=True)

    feedback_id = db.Column(
        db.Integer,
        db.ForeignKey("feedback.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    filename = db.Column(
        db.String(255),
        nullable=False
    )

    original_name = db.Column(
        db.String(255),
        nullable=False
    )

    uploaded_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    feedback = db.relationship(
        "Feedback",
        back_populates="attachments"
    )

    def __repr__(self):
        return f"<Attachment {self.original_name}>"