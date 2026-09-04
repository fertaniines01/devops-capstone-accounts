"""
Tests unitaires pour le modèle Account.
"""
import unittest
from service.models import Account, DataValidationError


class TestAccountModel(unittest.TestCase):
    """Tests pour la classe Account."""

    def test_create_account(self):
        """Vérifie qu'un compte peut être créé."""
        account = Account(name="John Doe", email="john@example.com")
        account.create()
        self.assertIsNotNone(account.id)

    def test_create_without_name_fails(self):
        """Vérifie qu'un compte sans nom lève une erreur."""
        account = Account()
        with self.assertRaises(DataValidationError):
            account.create()

    def test_to_dict(self):
        """Vérifie la conversion en dictionnaire."""
        account = Account(name="Jane Doe", email="jane@example.com")
        data = account.to_dict()
        self.assertEqual(data["name"], "Jane Doe")


if __name__ == "__main__":
    unittest.main()
