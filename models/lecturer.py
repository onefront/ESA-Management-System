from datetime import datetime

from extensions import db


class Lecturer(db.Model):

    __tablename__ = "lecturers"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    lecturer_name = db.Column(
        db.String(150),
        nullable=False
    )

    phone_number = db.Column(
        db.String(20),
        nullable=False
    )

    department = db.Column(
        db.String(100),
        nullable=True
    )

    created_at = db.Column(
        db.TIMESTAMP,
        nullable=True,
        server_default=db.text("CURRENT_TIMESTAMP")
    )

    def __repr__(self):
        return f"<Lecturer {self.lecturer_name}>"