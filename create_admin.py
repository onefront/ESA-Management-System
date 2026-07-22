from app import app
from extensions import db
from models.user import User

with app.app_context():

    user = User.query.filter_by(
        email="admin@usted.edu.gh"
    ).first()

    if not user:

        admin = User(
            full_name="System Administrator",
            email="admin@usted.edu.gh",
            role="Administrator"
        )

        admin.set_password("admin123")

        db.session.add(admin)
        db.session.commit()

        print("Administrator created successfully!")

    else:

        print("Administrator already exists.")