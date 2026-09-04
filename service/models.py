"""
Modèle Account pour le microservice.
Implémentation en mémoire (liste Python) pour rester simple à déployer.
"""


class DataValidationError(Exception):
    """Levée quand les données fournies pour un compte sont invalides."""


class Account:
    """Représente un compte client."""

    _next_id = 1
    _storage = {}  # {id: Account}

    def __init__(self, name=None, email=None, address=None, phone_number=None):
        self.id = None
        self.name = name
        self.email = email
        self.address = address
        self.phone_number = phone_number

    def create(self):
        """Crée un nouveau compte et l'enregistre."""
        if not self.name:
            raise DataValidationError("Le champ 'name' est obligatoire")
        self.id = Account._next_id
        Account._next_id += 1
        Account._storage[self.id] = self
        return self

    def update(self):
        """Met à jour un compte existant."""
        if self.id not in Account._storage:
            raise DataValidationError(f"Compte {self.id} introuvable")
        Account._storage[self.id] = self

    def delete(self):
        """Supprime un compte."""
        if self.id in Account._storage:
            del Account._storage[self.id]

    def to_dict(self):
        """Convertit le compte en dictionnaire."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "phone_number": self.phone_number,
        }

    def deserialize(self, data):
        """Remplit le compte à partir d'un dictionnaire."""
        try:
            self.name = data["name"]
            self.email = data.get("email")
            self.address = data.get("address")
            self.phone_number = data.get("phone_number")
        except KeyError as error:
            raise DataValidationError(f"Champ manquant : {error}") from error
        return self

    @classmethod
    def find(cls, account_id):
        """Retourne un compte par son id, ou None."""
        return cls._storage.get(account_id)

    @classmethod
    def all(cls):
        """Retourne tous les comptes."""
        return list(cls._storage.values())
