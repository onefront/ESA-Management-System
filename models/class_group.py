from extensions import db
from datetime import datetime


class ClassGroup(db.Model):
    __tablename__ = "class_groups"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)

    programme_id = db.Column(
        db.Integer,
        db.ForeignKey("programmes.id"),
        nullable=False
    )
    session = db.Column(
        db.String(20),
        nullable=False,
        default="Weekend"
    )
    programme = db.relationship(
        "Programme",
        backref="class_groups"
    )

    level = db.Column(
        db.String(20),
        nullable=False
    )

    admission_year = db.Column(db.String(10))

    graduation_year = db.Column(db.String(10))

    status = db.Column(
        db.String(20),
        default="Active"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    course_rep_id = db.Column(
        db.Integer,
        db.ForeignKey("members.id"),
        nullable=True
    )
    assistant_course_rep_id = db.Column(
        db.Integer,
        db.ForeignKey("members.id"),
        nullable=True
    )

    course_rep = db.relationship(
        "Member",
        foreign_keys=[course_rep_id]
    )
    assistant_course_rep = db.relationship(
        "Member",
        foreign_keys=[assistant_course_rep_id]
    )



    def __repr__(self):
        return f"<ClassGroup {self.name}>"