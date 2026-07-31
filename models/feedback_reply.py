from datetime import datetime
from extensions import db


class FeedbackReply(db.Model):
    __tablename__ = "feedback_replies"

    id = db.Column(db.Integer, primary_key=True)

    feedback_id = db.Column(
        db.Integer,
        db.ForeignKey("feedback.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    message = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    feedback = db.relationship(
        "Feedback",
        back_populates="replies"
    )

    user = db.relationship(
        "User"
    )

    def __repr__(self):
        return f"<FeedbackReply #{self.id}>"