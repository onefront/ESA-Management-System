from datetime import datetime
from extensions import db
from datetime import datetime
from models.executive import Executive

class Feedback(db.Model):
    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)

    ticket_no = db.Column(db.String(20), unique=True, nullable=False)

    member_id = db.Column(
        db.Integer,
        db.ForeignKey("members.id"),
        nullable=False
    )

    feedback_type = db.Column(
        db.String(30),
        nullable=False
    )

    subject = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    priority = db.Column(
        db.String(20),
        default="Medium"
    )

    status = db.Column(
        db.String(30),
        default="New"
    )

    anonymous = db.Column(
        db.Boolean,
        default=False
    )

    assigned_to = db.Column(
        db.Integer,
        db.ForeignKey("executives.id"),
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

    member = db.relationship(
        "Member",
        backref=db.backref(
            "feedbacks",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )

    assigned_executive = db.relationship(
        "Executive",
        foreign_keys=[assigned_to]
    )

    replies = db.relationship(
        "FeedbackReply",
        back_populates="feedback",
        cascade="all, delete-orphan",
        lazy=True,
        order_by="FeedbackReply.created_at"
    )

    attachments = db.relationship(
        "FeedbackAttachment",
        back_populates="feedback",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f"<Feedback {self.ticket_no}>"
