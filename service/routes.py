"""
Routes REST pour le microservice Accounts : Create, Read, List, Update, Delete.
"""
from flask import jsonify, request, url_for
from service import app
from service.models import Account, DataValidationError

STATUS_OK = 200
STATUS_CREATED = 201
STATUS_NOT_FOUND = 404
STATUS_BAD_REQUEST = 400


@app.route("/health", methods=["GET"])
def health():
    """Vérifie que le service tourne."""
    return jsonify(status="OK"), STATUS_OK


@app.route("/accounts", methods=["POST"])
def create_accounts():
    """CREATE : crée un nouveau compte."""
    try:
        account = Account()
        account.deserialize(request.get_json())
        account.create()
    except DataValidationError as error:
        return jsonify(error=str(error)), STATUS_BAD_REQUEST

    location_url = url_for("read_accounts", account_id=account.id, _external=True)
    return (
        jsonify(account.to_dict()),
        STATUS_CREATED,
        {"Location": location_url},
    )


@app.route("/accounts/<int:account_id>", methods=["GET"])
def read_accounts(account_id):
    """READ : retourne un compte précis."""
    account = Account.find(account_id)
    if not account:
        return jsonify(error=f"Compte {account_id} introuvable"), STATUS_NOT_FOUND
    return jsonify(account.to_dict()), STATUS_OK


@app.route("/accounts", methods=["GET"])
def list_accounts():
    """LIST : retourne tous les comptes."""
    accounts = [account.to_dict() for account in Account.all()]
    return jsonify(accounts), STATUS_OK


@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_accounts(account_id):
    """UPDATE : met à jour un compte existant."""
    account = Account.find(account_id)
    if not account:
        return jsonify(error=f"Compte {account_id} introuvable"), STATUS_NOT_FOUND

    try:
        account.deserialize(request.get_json())
        account.id = account_id
        account.update()
    except DataValidationError as error:
        return jsonify(error=str(error)), STATUS_BAD_REQUEST

    return jsonify(account.to_dict()), STATUS_OK


@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_accounts(account_id):
    """DELETE : supprime un compte."""
    account = Account.find(account_id)
    if account:
        account.delete()
    return "", 204
