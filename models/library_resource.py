from datetime import datetime

from extensions import db


class LibraryResource(db.Model):
    __tablename__ = "library_resources"

    id = db.Column(db.Integer, primary_key=True)

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("library_categories.id"),
        nullable=False
    )

    programme_id = db.Column(
        db.Integer,
        db.ForeignKey("programmes.id"),
        nullable=False
    )

    level = db.Column(
        db.String(20),
        nullable=False
    )

    course_code = db.Column(
        db.String(30),
        nullable=False
    )

    course_title = db.Column(
        db.String(200),
        nullable=False
    )

    academic_year = db.Column(
        db.String(20)
    )

    semester = db.Column(
        db.String(50)
    )

    exam_type = db.Column(
        db.String(50)
    )

    title = db.Column(
        db.String(255),
        nullable=False
    )

    description = db.Column(db.Text)

    file_name = db.Column(
        db.String(255),
        nullable=False
    )

    file_path = db.Column(
        db.String(255),
        nullable=False
    )

    file_size = db.Column(db.Integer)

    downloads = db.Column(
        db.Integer,
        default=0
    )

    uploaded_by = db.Column(db.Integer)

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    category = db.relationship(
        "LibraryCategory",
        back_populates="resources"
    )

    programme = db.relationship(
        "Programme",
        backref="library_resources"
    )

    def __repr__(self):
        return f"<LibraryResource {self.title}>"