import unittest
from project.authentification.models import User


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
        self.assertEqual(new_user.__repr__(), f"<User: Bob Dupont>")

if __name__ == "__main__":
    unittest.main()
