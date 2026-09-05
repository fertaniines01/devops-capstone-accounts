"""
Tests unitaires pour les routes REST du microservice Accounts,
y compris les en-têtes de sécurité (Talisman) et la politique CORS.
"""
import unittest
from service import app


class TestAccountRoutes(unittest.TestCase):
    """Tests pour les endpoints CRUD et la sécurité."""

    def setUp(self):
        self.client = app.test_client()
        self.headers = {"Content-Type": "application/json"}

    # ---- Health ----
    def test_health(self):
        """It should return 200 on health check"""
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)

    # ---- CREATE ----
    def test_create_account(self):
        """It should create a new account"""
        resp = self.client.post(
            "/accounts",
            json={"name": "Alice", "email": "alice@example.com"},
        )
        self.assertEqual(resp.status_code, 201)

    def test_create_account_returns_location_header(self):
        """It should return a Location header on create"""
        resp = self.client.post(
            "/accounts", json={"name": "Carol", "email": "carol@example.com"}
        )
        self.assertIsNotNone(resp.headers.get("Location"))

    def test_create_account_missing_name_fails(self):
        """It should not create an account without a name"""
        resp = self.client.post("/accounts", json={"email": "no-name@example.com"})
        self.assertEqual(resp.status_code, 400)

    # ---- LIST ----
    def test_list_accounts(self):
        """It should list all accounts"""
        resp = self.client.get("/accounts")
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.get_json(), list)

    # ---- READ ----
    def test_read_account_not_found(self):
        """It should return 404 for a missing account"""
        resp = self.client.get("/accounts/999999")
        self.assertEqual(resp.status_code, 404)

    def test_read_account_found(self):
        """It should read an existing account"""
        created = self.client.post(
            "/accounts", json={"name": "Dan", "email": "dan@example.com"}
        )
        account_id = created.get_json()["id"]
        resp = self.client.get(f"/accounts/{account_id}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["name"], "Dan")

    # ---- UPDATE ----
    def test_update_account(self):
        """It should update an existing account"""
        created = self.client.post(
            "/accounts", json={"name": "Eve", "email": "eve@example.com"}
        )
        account_id = created.get_json()["id"]
        resp = self.client.put(
            f"/accounts/{account_id}",
            json={"name": "Eve Updated", "email": "eve2@example.com"},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["name"], "Eve Updated")

    def test_update_account_not_found(self):
        """It should return 404 when updating a missing account"""
        resp = self.client.put(
            "/accounts/999999", json={"name": "Ghost", "email": "ghost@example.com"}
        )
        self.assertEqual(resp.status_code, 404)

    # ---- DELETE ----
    def test_delete_account(self):
        """It should delete an existing account"""
        created = self.client.post(
            "/accounts", json={"name": "Frank", "email": "frank@example.com"}
        )
        account_id = created.get_json()["id"]
        resp = self.client.delete(f"/accounts/{account_id}")
        self.assertEqual(resp.status_code, 204)

    def test_delete_missing_account_still_succeeds(self):
        """It should return 204 even if the account does not exist"""
        resp = self.client.delete("/accounts/999999")
        self.assertEqual(resp.status_code, 204)

    # ---- Full CRUD cycle ----
    def test_create_read_update_delete_flow(self):
        """It should support the full create-read-update-delete cycle"""
        resp = self.client.post(
            "/accounts", json={"name": "Bob", "email": "bob@example.com"}
        )
        account_id = resp.get_json()["id"]

        resp = self.client.get(f"/accounts/{account_id}")
        self.assertEqual(resp.status_code, 200)

        resp = self.client.put(
            f"/accounts/{account_id}",
            json={"name": "Bob Updated", "email": "bob2@example.com"},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["name"], "Bob Updated")

        resp = self.client.delete(f"/accounts/{account_id}")
        self.assertEqual(resp.status_code, 204)

    # ---- Security headers (Talisman) ----
    def test_security_headers(self):
        """It should return security headers"""
        resp = self.client.get("/health")
        expected_headers = {
            "X-Frame-Options": "SAMEORIGIN",
            "X-Content-Type-Options": "nosniff",
            "Content-Security-Policy": "default-src 'self'; object-src 'none'",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }
        for key in expected_headers:
            self.assertIn(key, resp.headers)

    # ---- CORS ----
    def test_cors_security(self):
        """It should return a CORS header"""
        resp = self.client.get("/health", environ_overrides={"HTTP_ORIGIN": "http://localhost"})
        self.assertIn("Access-Control-Allow-Origin", resp.headers)


if __name__ == "__main__":
    unittest.main()
