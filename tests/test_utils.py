import unittest
from flask_testing import TestCase
from project.cryptocurrency.utils import (
    get_user_current_total_valorization,
    get_user_total_valorization_of_the_day,
    add_cryptocurrency,
    update_quote,
    daily_update_user_last_valorization,
)
from project import create_app, db
from project.authentification.models import User
from project.cryptocurrency.models import (
    Cryptocurrency,
    Purchase,
    QuoteCurrency,
    Profit,
)
from werkzeug.security import generate_password_hash
from datetime import date, datetime, timedelta


class TestUtilsFunction(TestCase, unittest.TestCase):
    def create_app(self):
        app = create_app("config.TestConfig")
        return app

    def setUp(self):
        db.create_all()
        self.yesterday = date.today() - timedelta(days=1)
        self.yesterday_start = datetime.combine(
            self.yesterday, datetime.min.time()
        )
        self.yesterday_end = self.yesterday_start.replace(
            hour=23, minute=59, second=59
        )

    def set_user_and_cryptocurrency(self):
        self.new_user = User(
            first_name="Bob",
            last_name="Dupont",
            email="bobdupont@test.com",
            password=generate_password_hash("bobdu1234"),
        )
        self.new_user_1 = User(
            first_name="Robert",
            last_name="Dupont",
            email="robertdupont@test.com",
            password=generate_password_hash("robertdu856"),
        )
        db.session.add(self.new_user)
        db.session.add(self.new_user_1)
        self.new_cryptocurrency = Cryptocurrency(
            name="Bitcon",
            symbol="BTC",
            coinmarketcap_id=4,
            coinmarketcap_icon="https://example.com/icon/4",
        )
        db.session.add(self.new_cryptocurrency)
        db.session.commit()

    def set_purchse_and_quote(self):
        self.new_quote_currency = QuoteCurrency(
            cryptocurrency_id=self.new_cryptocurrency.id, price=110,
            date=date.today()
        )
        db.session.add(self.new_quote_currency)
        self.new_purchase = Purchase(
            user_id=self.new_user.id,
            cryptocurrency_id=self.new_cryptocurrency.id,
            price=1000,
            quantity=10,
            date=self.yesterday_start,
        )
        self.new_purchase_1 = Purchase(
            user_id=self.new_user_1.id,
            cryptocurrency_id=self.new_cryptocurrency.id,
            price=200,
            quantity=1,
            date=self.yesterday_start,
        )
        db.session.add(self.new_purchase)
        db.session.add(self.new_purchase_1)
        db.session.commit()

    def yesterday_last_quote_of_the_day(self):
        self.new_quote_currency_yesterday_0 = QuoteCurrency(
            cryptocurrency_id=self.new_cryptocurrency.id,
            price=120,
            date=self.yesterday_start,
        )
        db.session.add(self.new_quote_currency_yesterday_0)
        self.new_quote_currency_yeseday_1 = QuoteCurrency(
            cryptocurrency_id=self.new_cryptocurrency.id,
            price=150,
            date=self.yesterday_end,
        )
        db.session.add(self.new_quote_currency_yeseday_1)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_current_valorisation(self):
        self.set_user_and_cryptocurrency()
        self.set_purchse_and_quote()
        self.yesterday_last_quote_of_the_day()
        item_list, totale = get_user_current_total_valorization(1)
        self.assertEqual(totale, 100)
        self.assertEqual(item_list[0].name, self.new_cryptocurrency.name)
        self.assertEqual(item_list[0].symbol, self.new_cryptocurrency.symbol)
        self.assertEqual(
            item_list[0].icon, self.new_cryptocurrency.coinmarketcap_icon
        )
        self.assertEqual(item_list[0].valorization, 100)

    def test_yesterday_last_valorisation(self):
        self.set_user_and_cryptocurrency()
        self.set_purchse_and_quote()
        self.yesterday_last_quote_of_the_day()
        (
            yesterday_last_quote,
            yesterday_end,
        ) = get_user_total_valorization_of_the_day(1)
        self.assertEqual(yesterday_last_quote, 500)
        self.assertEqual(yesterday_end, self.yesterday_end)

    def test_add_cryptocurrency(self):
        cryptocurrencys = Cryptocurrency.query.all()
        self.assertEqual(cryptocurrencys, [])
        add_cryptocurrency()
        cryptocurrencys_1 = Cryptocurrency.query.all()
        self.assertNotEqual(cryptocurrencys_1, [])

    def test_update_quote_cryptocurrency(self):
        add_cryptocurrency()
        quote_currency = QuoteCurrency.query.all()
        self.assertEqual(quote_currency, [])
        update_quote()
        quote_currency_1 = QuoteCurrency.query.all()
        self.assertNotEqual(quote_currency_1, [])

    def test_daily_update_user_last_valorization(self):
        self.set_user_and_cryptocurrency()
        self.set_purchse_and_quote()
        self.yesterday_last_quote_of_the_day()
        profit = Profit.query.all()
        self.assertEqual(profit, [])
        daily_update_user_last_valorization()
        profit_1 = Profit.query.all()
        self.assertNotEqual(profit_1, [])
        profit_user = Profit.query.filter(
            Profit.user_id == self.new_user.id
        ).first()
        self.assertEqual(profit_user.profit_and_loss, 500)
        self.assertEqual(profit_user.date, self.yesterday_end)
        profit_user_1 = Profit.query.filter(
            Profit.user_id == self.new_user_1.id
        ).first()
        self.assertEqual(profit_user_1.profit_and_loss, -50)
        self.assertEqual(profit_user_1.date, self.yesterday_end)
