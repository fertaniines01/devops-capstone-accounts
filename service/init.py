"""
Package d'initialisation du microservice Accounts.
Crée l'application Flask et enregistre les routes.
"""
from flask import Flask

app = Flask(__name__)

from service import routes  # noqa: E402, F401
