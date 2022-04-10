import unittest
from flask_testing import TestCase
from project import create_app, db
from project.authentification.models import User
from werkzeug.security import generate_password_hash
from flask import url_for

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
                "password": "new-password",
                "confirm": "new-password",
            },
        )
        self.assert_message_flashed(
            "Votre compte a bien été enregistré.",
            "success",
        )
        self.assertEqual(response.request.path, url_for("authentification.login"))

    def test_post_on_signup_email_already_on_database(self):
        response = self.client.post(
            url_for("authentification.signup"),
            follow_redirects=True,
            data={
                "first_name": "bob",
                "last_name": "dupont",
                "email": "bobdupont@test.com",
                "password": "new-password",
                "confirm": "new-password",
            },
        )
        self.assert_message_flashed(
            "Un compte a déjà été créé avec cette adresse mail.",
            "warning",
        )
        self.assertEqual(response.request.path, url_for("authentification.login"))

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
            data={"email": "bobdupont@test.com", "password": "bobdu1234"},
        )
        self.assertRedirects(response, url_for("cryptocurrency.home"))

    def test_login_post_bad_password(self):
        response = self.client.post(
            url_for("authentification.login"),
            data={"email": "bobdupont@test.com", "password": "bad-password"},
        )
        self.assert_message_flashed(
            "Identifiant ou mot de passe incorrect.","danger"
        )
        self.assertEqual(response.request.path, url_for("authentification.login"))

    def test_logout_page_status_code(self):
        url = url_for("authentification.logout")
        response_0 = self.client.get(url)
        self.assertEqual(response_0.status_code, 302)
        # testing with a logged user
        self.logged_user()
        response_1 = self.client.get(url)
        self.assertEqual(response_1.status_code, 302)
        self.assert_message_flashed("A bientot", "success")
