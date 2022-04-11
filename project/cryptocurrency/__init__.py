"""
The cryptocurrency Blueprint handles the cryptocurrency data management.
The user can see is current valorization, add a purchase, add quickly
a purchase (with the last quote currency of the cryptocurrency), manage
the purchase.
"""
from flask import Blueprint

cryptocurrency_blueprint = Blueprint(
    "cryptocurrency", __name__, template_folder="templates"
)

from . import views
