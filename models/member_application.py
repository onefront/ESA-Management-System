from datetime import datetime

from extensions import db


class MemberApplication(db.Model):

    __tablename__ = "member_applications"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    first_name = db.Column(
        db.String(100),
        nullable=False
    )

    last_name = db.Column(
        db.String(100),
        nullable=False
    )

    gender = db.Column(
        db.String(20)
    )

    phone = db.Column(
        db.String(20)
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    faculty_id = db.Column(
        db.Integer,
        db.ForeignKey("faculties.id")
    )

    programme = db.Column(
        db.String(150)
    )

    department = db.Column(
        db.String(150)
    )

    level = db.Column(
        db.String(20)
    )

    session = db.Column(
        db.String(20)
    )

    academic_year = db.Column(
        db.String(20)
    )
    class_group_id = db.Column(
        db.Integer,
        db.ForeignKey("class_groups.id"),
        nullable=True
    )
    passport = db.Column(
        db.String(255)
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Pending"
    )

    reviewed_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    reviewed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    rejection_reason = db.Column(
        db.Text,
        nullable=True
    )

    date_applied = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    faculty = db.relationship(
        "Faculty"
    )
    class_group = db.relationship(
        "ClassGroup"
    )

    reviewer = db.relationship(
        "User",
        foreign_keys=[reviewed_by]
    )
    def __repr__(self):
        return f"<Application {self.student_id}>"