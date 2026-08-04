from extensions import db
from datetime import datetime


class Library(db.Model):
    __tablename__ = "library"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    programme_id = db.Column(
        db.Integer,
        db.ForeignKey("programmes.id"),
        nullable=False
    )

    level = db.Column(db.String(20), nullable=False)

    course_code = db.Column(db.String(30), nullable=False)

    course_title = db.Column(db.String(200), nullable=False)

    academic_year = db.Column(db.String(30))

    semester = db.Column(db.String(50))

    exam_type = db.Column(db.String(50))

    description = db.Column(db.Text)

    file_name = db.Column(db.String(255))

    file_path = db.Column(db.String(255))

    file_size = db.Column(db.Integer)

    downloads = db.Column(db.Integer, default=0)

    uploaded_by = db.Column(db.Integer)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    category = db.Column(
        db.String(100),
        default="Past Questions"
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

