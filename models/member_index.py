from datetime import datetime

from extensions import db


class MemberIndex(db.Model):
    __tablename__ = "member_indexes"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    used = db.Column(
        db.Boolean,
        default=False
    )

    used_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    used_at = db.Column(
        db.DateTime,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        foreign_keys=[used_by]
    )

    def __repr__(self):
        return f"<MemberIndex {self.student_id}>"