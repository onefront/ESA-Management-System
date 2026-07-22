from extensions import db
from datetime import datetime
from dateutil.relativedelta import relativedelta
from models.faculty import Faculty


class Member(db.Model):

    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id",
            ondelete="SET NULL"
        ),
        unique=True,
        nullable=True
    )

    user = db.relationship(
        "User",
        foreign_keys=[user_id],
        backref=db.backref(
            "member_profile",
            uselist=False
        )
    )

    course_rep = db.relationship(
        "CourseRep",
        back_populates="member",
        uselist=False
    )
    # Personal Information
    student_id = db.Column(db.String(30), unique=True, nullable=False)
    esa_id = db.Column(db.String(20), unique=True)

    first_name = db.Column(db.String(100), nullable=False)

    last_name = db.Column(db.String(100), nullable=False)

    gender = db.Column(db.String(20))
    date_of_birth = db.Column(
        db.Date,
        nullable=True
    )

    address = db.Column(
        db.String(250),
        nullable=True
    )

    guardian_name = db.Column(
        db.String(150),
        nullable=True
    )

    guardian_phone = db.Column(
        db.String(20),
        nullable=True
    )

    relationship = db.Column(
        db.String(100),
        nullable=True
    )


    phone = db.Column(db.String(20))
    email = db.Column(
        db.String(120),
        nullable=True
    )





    passport = db.Column(db.String(255))

    # Academic Information
    faculty_id = db.Column(
        db.Integer,
        db.ForeignKey("faculties.id")
    )
    faculty = db.relationship(
        "Faculty",
        backref="members"
    )
    programme = db.Column(db.String(150))

    department = db.Column(db.String(150))

    level = db.Column(db.String(20))

    session = db.Column(db.String(20))

    academic_year = db.Column(db.String(20))

    class_group_id = db.Column(
        db.Integer,
        db.ForeignKey("class_groups.id"),
        nullable=True
    )

    class_group = db.relationship(
        "ClassGroup",
        foreign_keys=[class_group_id]
    )


    # Membership
    status = db.Column(db.String(20), default="Active")
    # Registration Approval
    registration_status = db.Column(
        db.String(20),
        default="Pending"
    )

    approved_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )
    reviewer = db.relationship(
        "User",
        foreign_keys=[approved_by]
    )

    approved_at = db.Column(
        db.DateTime,
        nullable=True
    )

    date_registered = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    expiry_date = db.Column(
        db.DateTime,
        nullable=True
    )
    has_voted = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    def __repr__(self):
        return f"<Member {self.first_name} {self.last_name}>"

    def set_expiry_date(self):
        if self.date_registered and not self.expiry_date:
            self.expiry_date = self.date_registered + relativedelta(years=2)
