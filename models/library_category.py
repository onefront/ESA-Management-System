from extensions import db


class LibraryCategory(db.Model):
    __tablename__ = "library_categories"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    description = db.Column(db.Text)

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    resources = db.relationship(
        "LibraryResource",
        back_populates="category",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<LibraryCategory {self.name}>"