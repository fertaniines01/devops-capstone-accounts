"""
Tests unitaires pour les routes REST du microservice Accounts.
"""
import unittest
from service import app


class TestAccountRoutes(unittest.TestCase):
    """Tests pour les endpoints CRUD."""

    def setUp(self):
        self.client = app.test_client()

    def test_health(self):
        """Vérifie l'endpoint /health."""
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)

    def test_create_account(self):
        """Vérifie la création d'un compte."""
        resp = self.client.post(
            "/accounts",
            json={"name": "Alice", "email": "alice@example.com"},
        )
        self.assertEqual(resp.status_code, 201)

    def test_list_accounts(self):
        """Vérifie que la liste des comptes fonctionne."""
        resp = self.client.get("/accounts")
        self.assertEqual(resp.status_code, 200)

    def test_read_account_not_found(self):
        """Vérifie qu'un compte inexistant retourne 404."""
        resp = self.client.get("/accounts/999999")
        self.assertEqual(resp.status_code, 404)

    def test_create_read_update_delete_flow(self):
        """Teste le cycle complet CRUD."""
        # Create
        resp = self.client.post(
            "/accounts", json={"name": "Bob", "email": "bob@example.com"}
        )
        account_id = resp.get_json()["id"]

        # Read
        resp = self.client.get(f"/accounts/{account_id}")
        self.assertEqual(resp.status_code, 200)

        # Update
        resp = self.client.put(
            f"/accounts/{account_id}",
            json={"name": "Bob Updated", "email": "bob2@example.com"},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["name"], "Bob Updated")

        # Delete
        resp = self.client.delete(f"/accounts/{account_id}")
        self.assertEqual(resp.status_code, 204)


if __name__ == "__main__":
    unittest.main()
