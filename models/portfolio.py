from extensions import db


class Portfolio(db.Model):

    __tablename__ = "portfolios"

    id = db.Column(db.Integer, primary_key=True)

    portfolio_name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    description = db.Column(db.Text)

    display_order = db.Column(
        db.Integer,
        default=1
    )

    status = db.Column(
        db.String(20),
        default="Active"
    )


    def __repr__(self):
        return f"<Portfolio {self.portfolio_name}>"