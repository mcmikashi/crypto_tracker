import unittest
from flask_testing import TestCase
from werkzeug.security import generate_password_hash
from flask import url_for
from project import create_app, db
from project.authentification.models import User
from project.cryptocurrency.models import (
    Cryptocurrency,
    Profit,
    Purchase,
    QuoteCurrency,
)
from datetime import datetime, date, timezone, timedelta


class TestAuthentification(TestCase, unittest.TestCase):
    def create_app(self):
        app = create_app("config.TestConfig")
        return app

    def setUp(self):
        db.create_all()
        self.new_user = User(
            first_name="Bob",
            last_name="Dupont",
            email="bobdupont@test.com",
            password=generate_password_hash("bobdu1234"),
        )
        db.session.add(self.new_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def logged_user(self):
        return self.client.post(
            url_for("authentification.login"),
            data=dict(email="bobdupont@test.com", password="bobdu1234"),
        )

    def test_signup_page_status_code(self):
        url = url_for("authentification.signup")
        response_0 = self.client.get(url)
        self.assert200(response_0)
        # testing with a logged user
        self.logged_user()
        response_1 = self.client.get(url)
        self.assert200(response_1)

    def test_post_on_signup(self):
        response = self.client.post(
            url_for("authentification.signup"),
            follow_redirects=True,
            data={
                "first_name": "bernard",
                "last_name": "dupont",
                "email": "bernarddupont@test.com",
                "password_new": "New+pass15",
                "confirm": "New+pass15",
            },
        )
        self.assert_message_flashed(
            "Votre compte a bien été enregistré.",
            "success",
        )
        self.assertEqual(
            response.request.path, url_for("authentification.login")
        )

    def test_post_on_signup_email_already_on_database(self):
        response = self.client.post(
            url_for("authentification.signup"),
            follow_redirects=True,
            data={
                "first_name": "bob",
                "last_name": "dupont",
                "email": "bobdupont@test.com",
                "password_new": "New+pass15",
                "confirm": "New+pass15",
            },
        )
        self.assert_message_flashed(
            "Un compte a déjà été créé avec cette adresse mail.",
            "warning",
        )
        self.assertEqual(
            response.request.path, url_for("authentification.login")
        )

    def test_login_page_status_code(self):
        url = url_for("authentification.login")
        response_0 = self.client.get(url)
        self.assert200(response_0)
        # testing with a logged user
        self.logged_user()
        response_1 = self.client.get(url)
        self.assertEqual(response_1.status_code, 302)

    def test_login_post(self):
        response = self.client.post(
            url_for("authentification.login"),
            follow_redirects=True,
            data={"email": "bobdupont@test.com", "password": "bobdu1234"},
        )
        self.assertEqual(response.request.path, url_for("cryptocurrency.home"))

    def test_login_post_bad_password(self):
        response = self.client.post(
            url_for("authentification.login"),
            data={"email": "bobdupont@test.com", "password": "bad-password"},
        )
        self.assert_message_flashed(
            "Identifiant ou mot de passe incorrect.", "danger"
        )
        self.assertEqual(
            response.request.path, url_for("authentification.login")
        )

    def test_logout_page_status_code(self):
        url = url_for("authentification.logout")
        response_0 = self.client.get(url)
        self.assertEqual(response_0.status_code, 302)
        # testing with a logged user
        self.logged_user()
        response_1 = self.client.get(url)
        self.assertEqual(response_1.status_code, 302)
        self.assert_message_flashed("A bientot", "success")


class TestCryptocurrency(TestCase, unittest.TestCase):
    def create_app(self):
        app = create_app("config.TestConfig")
        return app

    def setUp(self):
        db.create_all()
        self.new_user = User(
            first_name="Bob",
            last_name="Dupont",
            email="bobdupont@test.com",
            password=generate_password_hash("bobdu1234"),
        )
        db.session.add(self.new_user)
        self.new_user_1 = User(
            first_name="Robert",
            last_name="Dupont",
            email="robertdupont@test.com",
            password=generate_password_hash("robertdup1234"),
        )
        db.session.add(self.new_user_1)
        self.new_cryptocurrency = Cryptocurrency(
            name="Bitcon",
            symbol="BTC",
            coinmarketcap_id=1,
            coinmarketcap_icon="https://example.com/icon/1",
        )
        db.session.add(self.new_cryptocurrency)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def auth_user(self):
        return self.client.post(
            url_for("authentification.login"),
            data=dict(email="bobdupont@test.com", password="bobdu1234"),
        )

    def set_purchse_and_quote(self):
        self.new_quote_currency = QuoteCurrency(
            cryptocurrency_id=self.new_cryptocurrency.id, price=110
        )
        db.session.add(self.new_quote_currency)
        self.new_purchase = Purchase(
            user_id=self.new_user.id,
            cryptocurrency_id=self.new_cryptocurrency.id,
            price=1000,
            quantity=10,
            date=datetime.now(timezone.utc),
        )
        db.session.add(self.new_purchase)
        self.new_purchase_1 = Purchase(
            user_id=self.new_user_1.id,
            cryptocurrency_id=self.new_cryptocurrency.id,
            price=200,
            quantity=1,
            date=datetime.now(timezone.utc),
        )
        db.session.add(self.new_purchase_1)
        db.session.commit()

    def set_profit(self):
        self.profit = Profit(
            user_id=self.new_user.id,
            profit_and_loss=300,
            date=date.today() - timedelta(1),
        )
        db.session.add(self.profit)
        db.session.commit()

    def test_home_status_code(self):
        url = url_for("cryptocurrency.home")
        response_0 = self.client.get(url)
        self.assertEqual(response_0.status_code, 302)
        # testing with a logged user
        self.auth_user()
        response_1 = self.client.get(url)
        self.assert_200(response_1)

    def test_add_status_code(self):
        url = url_for("cryptocurrency.add")
        response_0 = self.client.get(url)
        self.assertEqual(response_0.status_code, 302)
        # testing with a logged user
        self.auth_user()
        response_1 = self.client.get(url)
        self.assert200(response_1)

    def test_post_on_add(self):
        self.auth_user()
        response = self.client.post(
            url_for("cryptocurrency.add"),
            data={
                "cryptocurrency": 1,
                "price": 100,
                "quantity": 10,
            },
        )
        self.assert_message_flashed(
            "Votre achats a bien été ajouté.",
            "success",
        )
        self.assert200(response)

    def test_quick_add_status_code(self):
        url = url_for("cryptocurrency.quick_add")
        response_0 = self.client.get(url)
        self.assertEqual(response_0.status_code, 302)
        # testing with a logged user
        self.auth_user()
        response_1 = self.client.get(url)
        self.assert200(response_1)

    def test_post_on_quick_add(self):
        self.auth_user()
        self.set_purchse_and_quote()
        response = self.client.post(
            url_for("cryptocurrency.quick_add"),
            data={
                "cryptocurrency": 1,
                "quantity": 10,
            },
        )
        self.assert_message_flashed(
            "Votre achats a bien été ajouté.",
            "success",
        )
        self.assert200(response)

    def test_admin_status_code(self):
        url = url_for("cryptocurrency.manage")
        response_0 = self.client.get(url)
        self.assertEqual(response_0.status_code, 302)
        # testing with a logged user
        self.auth_user()
        response_1 = self.client.get(url)
        self.assert200(response_1)

    def test_graphique_status_code(self):
        url = url_for("cryptocurrency.chart")
        response_0 = self.client.get(url)
        self.assertEqual(response_0.status_code, 302)
        # testing with a logged user
        self.auth_user()
        response_1 = self.client.get(url)
        self.assert200(response_1)
        # testing with a logged user with profit
        self.set_purchse_and_quote()
        self.set_profit()
        response_1 = self.client.get(url)
        self.assert200(response_1)

    def test_edit_status_code(self):
        self.set_purchse_and_quote()
        url = url_for("cryptocurrency.edit", pk=self.new_purchase.id)
        response_0 = self.client.get(url)
        self.assertEqual(response_0.status_code, 302)
        # testing with a logged user
        self.auth_user()
        response_1 = self.client.get(url)
        self.assert200(response_1)
        # default user tries to access another user's purchase
        url_1 = url_for("cryptocurrency.edit", pk=self.new_purchase_1.id)
        response_2 = self.client.get(url_1, follow_redirects=True)
        self.assertEqual(
            response_2.request.path, url_for("cryptocurrency.manage")
        )

    def test_post_on_edit(self):
        self.auth_user()
        self.set_purchse_and_quote()
        response = self.client.post(
            url_for("cryptocurrency.edit", pk=self.new_purchase.id),
            data={
                "cryptocurrency": 1,
                "price": 200,
                "quantity": 5,
            },
        )
        self.assert_message_flashed(
            "Votre achats a bien été mise à jour.",
            "success",
        )
        self.assert200(response)

    def test_delete_status_code(self):
        self.set_purchse_and_quote()
        url = url_for("cryptocurrency.delete", pk=self.new_purchase.id)
        response_0 = self.client.get(url)
        self.assertEqual(response_0.status_code, 302)
        # testing with a logged user
        self.auth_user()
        response_1 = self.client.get(url)
        self.assert200(response_1)
        # default user tries to access another user's purchase
        url_1 = url_for("cryptocurrency.delete", pk=self.new_purchase_1.id)
        response_2 = self.client.get(url_1, follow_redirects=True)
        self.assertEqual(
            response_2.request.path, url_for("cryptocurrency.manage")
        )

    def test_post_on_delete(self):
        self.auth_user()
        self.set_purchse_and_quote()
        response = self.client.post(
            url_for("cryptocurrency.delete", pk=self.new_purchase.id),
            follow_redirects=True,
        )
        self.assert_message_flashed(
            "Votre achats a bien été suprimmé.",
            "success",
        )
        self.assertEqual(
            response.request.path, url_for("cryptocurrency.manage")
        )
