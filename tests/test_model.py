import unittest
from project.authentification.models import User
from project.cryptocurrency.models import (
    Cryptocurrency,
    Purchase,
    QuoteCurrency,
    Profit,
)
from datetime import datetime, timezone


class TestAuthentification(unittest.TestCase):
    def test_new_user(self):
        new_user = User(
            first_name="Bob",
            last_name="Dupont",
            email="bob.dupont@test.com",
            password="bobdupont1234",
        )
        self.assertEqual(new_user.first_name, "Bob")
        self.assertEqual(new_user.last_name, "Dupont")
        self.assertEqual(new_user.email, "bob.dupont@test.com")
        self.assertEqual(new_user.password, "bobdupont1234")
        self.assertEqual(new_user.__repr__(), "<User: Bob Dupont>")


class TestCrypto(unittest.TestCase):
    def test_new_cryptocurrency(self):
        new_cryptocurrency = Cryptocurrency(
            name="Bitcon",
            symbol="BTC",
            coinmarketcap_id=4,
            coinmarketcap_icon="https://example.com/icon/4",
        )
        self.assertEqual(new_cryptocurrency.name, "Bitcon")
        self.assertEqual(new_cryptocurrency.symbol, "BTC")
        self.assertEqual(new_cryptocurrency.coinmarketcap_id, 4)
        self.assertEqual(
            new_cryptocurrency.coinmarketcap_icon, "https://example.com/icon/4"
        )
        self.assertEqual(
            new_cryptocurrency.__repr__(), "<Cryptocurrency Bitcon>"
        )

    def test_new_quote_currency(self):
        new_cryptocurrency = Cryptocurrency(
            name="Bitcon",
            symbol="BTC",
            coinmarketcap_id=4,
            coinmarketcap_icon="https://example.com/icon/4",
        )
        new_date = datetime.now(timezone.utc)
        new_quote_currency = QuoteCurrency(
            cryptocurrency_id=new_cryptocurrency, price=32000, date=new_date
        )
        self.assertEqual(
            new_quote_currency.cryptocurrency_id, new_cryptocurrency
        )
        self.assertEqual(new_quote_currency.price, 32000)
        self.assertEqual(new_quote_currency.date, new_date)
        self.assertEqual(
            new_quote_currency.__repr__(),
            f"<QuoteCurrency : <C:Bitcon> <D:{new_date}> >",
        )

    def test_new_purchase(self):
        new_user = User(
            first_name="Bob",
            last_name="Dupont",
            email="bob.dupont@test.com",
            password="bobdupont1234",
        )
        new_cryptocurrency = Cryptocurrency(
            name="Bitcon",
            symbol="BTC",
            coinmarketcap_id=4,
            coinmarketcap_icon="https://example.com/icon/4",
        )
        new_date = datetime.now(timezone.utc)
        new_purchase = Purchase(
            user_id=new_user,
            cryptocurrency_id=new_cryptocurrency,
            price=50000,
            quantity=4,
            date=new_date,
        )
        self.assertEqual(new_purchase.user_id, new_user)
        self.assertEqual(new_purchase.cryptocurrency_id, new_cryptocurrency)
        self.assertEqual(new_purchase.price, 50000)
        self.assertEqual(new_purchase.quantity, 4)
        self.assertEqual(new_purchase.date, new_date)
        self.assertEqual(
            new_purchase.__repr__(), f"<Purchase : <C:BTC> <D:{new_date}> >"
        )

    def test_new_profit(self):
        new_user = User(
            first_name="Bob",
            last_name="Dupont",
            email="bob.dupont@test.com",
            password="bobdupont1234",
        )
        new_date = datetime.now(timezone.utc)
        new_profit = Profit(
            user_id=new_user,
            profit_and_loss=65000,
            date=new_date,
        )
        self.assertEqual(new_profit.user_id, new_user)
        self.assertEqual(new_profit.profit_and_loss, 65000)
        self.assertEqual(new_profit.date, new_date)
        self.assertEqual(
            new_profit.__repr__(), f"<Profit : <U:Bob Dupont> <D:{new_date}> >"
        )


if __name__ == "__main__":
    unittest.main()
