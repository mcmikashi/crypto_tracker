import unittest
from flask_testing import LiveServerTestCase
from project import create_app, db
from werkzeug.security import generate_password_hash
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from project.cryptocurrency.models import Cryptocurrency, QuoteCurrency
from project.authentification.models import User


class TestStatusCode(LiveServerTestCase, unittest.TestCase):
    def create_app(self):
        app = create_app("config.TestConfig")
        return app

    def setUp(self):
        db.create_all()
        self.new_user = User(
            first_name="Bob",
            last_name="Dupont",
            email="bob.dupont@test.com",
            password=generate_password_hash("bobdupont1234"),
        )
        self.cryptocurrency_1 = Cryptocurrency(
            name="Coin",
            symbol="C",
            coinmarketcap_id=1,
            coinmarketcap_icon="https://example.com/icon/1",
        )
        self.cryptocurrency_2 = Cryptocurrency(
            name="Coin1",
            symbol="C1",
            coinmarketcap_id=2,
            coinmarketcap_icon="https://example.com/icon/2",
        )
        data_list = [
            self.new_user,
            self.cryptocurrency_1,
            self.cryptocurrency_2,
        ]
        db.session.add_all(data_list)
        db.session.commit()
        options = Options()
        mobile_emulation = {"deviceName": "iPhone X"}
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        self.browser = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        self.browser.implicitly_wait(5)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.browser.quit()

    def add_quote_currency(self):
        self.new_quote1 = QuoteCurrency(
            cryptocurrency_id=self.cryptocurrency_1.id, price=110
        )
        self.new_quote2 = QuoteCurrency(
            cryptocurrency_id=self.cryptocurrency_2.id, price=120
        )
        data_list = [
            self.new_quote1,
            self.new_quote2,
        ]
        db.session.add_all(data_list)
        db.session.commit()

    def test_a_signup_and_login(self):
        # the index page will redirect us to the login page
        self.browser.get(self.get_server_url())
        self.assertEqual(
            self.browser.current_url, f"{self.get_server_url()}/login?next=%2F"
        )
        # go to the sign up page
        self.browser.find_element(By.LINK_TEXT, "Créer un compte").click()
        # fill the inscription form
        self.browser.find_element(By.NAME, "first_name").send_keys("Bob")
        self.browser.find_element(By.NAME, "last_name").send_keys("Dupont")
        self.browser.find_element(By.NAME, "email").send_keys(
            "bobdupont@test.fr"
        )
        self.browser.find_element(By.NAME, "password_new").send_keys(
            "Dubo1234+nbt"
        )
        self.browser.find_element(By.NAME, "confirm").send_keys("Dubo1234+nbt")
        self.browser.find_element(By.NAME, "submit_form").click()
        # redirect to the login page
        self.assertEqual(
            self.browser.current_url, f"{self.get_server_url()}/login"
        )
        self.browser.find_element(By.NAME, "email").send_keys(
            "bobdupont@test.fr"
        )
        self.browser.find_element(By.NAME, "password").send_keys(
            "Dubo1234+nbt"
        )
        self.browser.find_element(By.NAME, "submit_form").click()
        # we are logged and get redirect to the index
        self.assertEqual(self.browser.current_url, f"{self.get_server_url()}/")
        # we disconnect the user he will be redirect to login page
        self.browser.find_element(
            By.CSS_SELECTOR, ".fa-arrow-right-from-bracket"
        ).click()
        self.assertEqual(
            self.browser.current_url, f"{self.get_server_url()}/login"
        )

    def test_b_add_delete_edit_purchase(self):
        # the index page will redirect us to the login page
        self.browser.get(self.get_server_url())
        self.assertEqual(
            self.browser.current_url,
            f"{self.get_server_url()}/login?next=%2F",
        )
        # log with the default user
        self.browser.find_element(By.NAME, "email").send_keys(
            "bob.dupont@test.com"
        )
        self.browser.find_element(By.NAME, "password").send_keys(
            "bobdupont1234"
        )
        self.browser.find_element(By.NAME, "submit_form").click()
        # add a purchase
        self.browser.find_element(By.CSS_SELECTOR, ".fa-circle-plus").click()
        Select(
            self.browser.find_element(By.NAME, "cryptocurrency")
        ).select_by_value("2")

        field_price = self.browser.find_element(By.NAME, "price")
        field_price.clear()
        field_price.send_keys(100)
        field_quantity = self.browser.find_element(By.NAME, "quantity")
        field_quantity.clear()
        field_quantity.send_keys(10)
        self.browser.find_element(By.NAME, "submit_form").click()
        # edit a purchase
        self.browser.find_element(By.CSS_SELECTOR, ".fa-pen-to-square").click()
        table_row = self.browser.find_element(
            By.CSS_SELECTOR, "table tbody tr:first-child"
        ).get_attribute("innerHTML")
        self.assertNotEqual(
            table_row.strip(), '<td colspan="2" class="text-center">Aucun</td>'
        )
        self.browser.find_element(
            By.CSS_SELECTOR,
            "table tbody tr:first-child td:last-child a.btn-outline-warning",
        ).click()
        field_price = self.browser.find_element(By.NAME, "price")
        field_price.clear()
        field_price.send_keys(500)
        field_quantity = self.browser.find_element(By.NAME, "quantity")
        field_quantity.clear()
        field_quantity.send_keys(25)
        self.browser.find_element(By.NAME, "submit_form").click()
        # delete purchase
        self.browser.find_element(By.CSS_SELECTOR, ".fa-pen-to-square").click()
        self.browser.find_element(
            By.CSS_SELECTOR,
            "table tbody tr:first-child td:last-child a.btn-outline-danger",
        ).click()
        self.browser.find_element(By.NAME, "submit_form").click()
        self.browser.find_element(By.CSS_SELECTOR, ".fa-pen-to-square").click()
        table_row = self.browser.find_element(
            By.CSS_SELECTOR, "table tbody tr:first-child"
        ).get_attribute("innerHTML")
        self.assertEqual(
            table_row.strip(), '<td colspan="2" class="text-center">Aucun</td>'
        )
        self.browser.find_element(
            By.CSS_SELECTOR, ".fa-arrow-right-from-bracket"
        ).click()

    def test_d_quick_add_home(self):
        self.add_quote_currency()
        self.browser.get(self.get_server_url())
        self.assertEqual(
            self.browser.current_url,
            f"{self.get_server_url()}/login?next=%2F",
        )
        # log with the default user
        self.browser.find_element(By.NAME, "email").send_keys(
            "bob.dupont@test.com"
        )
        self.browser.find_element(By.NAME, "password").send_keys(
            "bobdupont1234"
        )
        self.browser.find_element(By.NAME, "submit_form").click()
        # add a quick purchase
        self.browser.find_element(By.CSS_SELECTOR, ".fa-plus").click()
        Select(
            self.browser.find_element(By.NAME, "cryptocurrency")
        ).select_by_value("1")
        field_quantity = self.browser.find_element(By.NAME, "quantity")
        field_quantity.clear()
        field_quantity.send_keys(10)
        # check the current valorization on home page
        self.browser.find_element(By.LINK_TEXT, "Crypto Tracker").click()
        link_valorization = self.browser.find_element(
            By.CSS_SELECTOR, "#id_valorization"
        ).get_attribute("innerHTML")
        self.assertIn("+0", link_valorization)


if __name__ == "__main__":
    unittest.main()
