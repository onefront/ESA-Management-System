from extensions import db


class SystemSettings(db.Model):
    __tablename__ = "system_settings"

    id = db.Column(db.Integer, primary_key=True)

    # General
    system_name = db.Column(db.String(200), default="Executive Student Association")
    short_name = db.Column(db.String(50), default="ESA")
    slogan = db.Column(db.String(200), default="Together We Build")

    # University
    university_name = db.Column(
        db.String(255),
        default="University of Skills Training and Entrepreneurial Development"
    )

    campus = db.Column(
        db.String(100),
        default="Kumasi Campus"
    )

    # Membership
    membership_validity = db.Column(
        db.Integer,
        default=2
    )

    # Branding
    logo = db.Column(
        db.String(255),
        default="logo.png"

    )

    ceo_signature = db.Column(
        db.String(255),
        default="ceo_signature.png"
    )

    # Contact
    phone = db.Column(db.String(30))
    email = db.Column(db.String(120))
    website = db.Column(db.String(200))