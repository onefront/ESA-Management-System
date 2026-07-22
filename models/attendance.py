from extensions import db


class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True)

    attendance_code = db.Column(db.String(20), unique=True)

    member_id = db.Column(
        db.Integer,
        db.ForeignKey("members.id"),
        nullable=False
    )

    event_id = db.Column(
        db.Integer,
        db.ForeignKey("events.id"),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Present"
    )

    attendance_date = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    member = db.relationship(
        "Member",
        backref=db.backref(
            "attendance",
            cascade="all, delete-orphan"
        )
    )

    event = db.relationship("Event", backref="attendance")