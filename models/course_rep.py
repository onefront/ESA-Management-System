from datetime import datetime

from extensions import db


class CourseRep(db.Model):

    __tablename__ = "course_reps"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    member_id = db.Column(
        db.Integer,
        db.ForeignKey("members.id"),
        unique=True,
        nullable=False
    )
    class_group_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "class_groups.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    class_group = db.relationship(
        "ClassGroup",
        backref="representatives"
    )
    # NEW FIELD
    position = db.Column(
        db.String(30),
        nullable=False,
        default="Course Rep"
    )

    status = db.Column(
        db.String(20),
        default="Active"
    )

    appointed_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    member = db.relationship(
        "Member",
        back_populates="course_rep"
    )