"""
Package d'initialisation du microservice Accounts.
Crée l'application Flask, active les en-têtes de sécurité (Talisman)
et la politique CORS.
"""
from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS

app = Flask(__name__)

# En-têtes de sécurité HTTP (HSTS, X-Frame-Options, CSP, etc.)
# force_https=False car l'environnement de dev/lab n'utilise pas toujours TLS.
talisman = Talisman(app, force_https=False)

# Politique CORS : autorise les appels cross-origin (utile pour un frontend séparé)
CORS(app)

from service import routes  # noqa: E402, F401
