from project import db
from datetime import datetime


class Cryptocurrency(db.Model):
    __tablename__ = "cryptocurrency"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    symbol = db.Column(db.String(100), nullable=False)
    coinmarketcap_id = db.Column(db.Integer, nullable=False)
    coinmarketcap_icon = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Cryptocurrency {self.name}>"


class Purchase(db.Model):
    __tablename__ = "purchase"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    cryptocurrency_id = db.Column(
        db.Integer, db.ForeignKey("cryptocurrency.id"), nullable=False
    )
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship("User", backref=db.backref("purchases", lazy=True))
    cryptocurrency = db.relationship(
        "Cryptocurrency", backref=db.backref("purchases", lazy=True)
    )

    def __repr__(self):
        return (f"<Purchase : <C:{self.cryptocurrency_id.symbol}> "
                f"<D:{self.date}> >")


class QuoteCurrency(db.Model):
    __tablename__ = "quote_currency"
    id = db.Column(db.Integer, primary_key=True)
    cryptocurrency_id = db.Column(
        db.Integer, db.ForeignKey("cryptocurrency.id"), nullable=False
    )
    price = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cryptocurrency = db.relationship(
        "Cryptocurrency", backref=db.backref("valorizations", lazy=True)
    )

    def __repr__(self):
        return (f"<QuoteCurrency : <C:{self.cryptocurrency_id.name}> "
                f"<D:{self.date}> >")


class Profit(db.Model):
    __tablename__ = "profit"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    profit_and_loss = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship("User", backref=db.backref("profits", lazy=True))

    def __repr__(self):
        return (f"<Profit : <U:{self.user_id.first_name} "
                f"{self.user_id.last_name}> <D:{self.date}> >")
