from . import cryptocurrency_blueprint as crypto
from flask import render_template
from .utils import (
    get_user_current_total_valorization,
)
from flask_login import login_required, current_user

@crypto.route("/")
@login_required
def home():
    cryptocurrencys,total_valorization = \
        get_user_current_total_valorization(current_user.id)
    return render_template(
        "cryptocurrency/home.html",
        cryptocurrencys=cryptocurrencys,
        total_valorization=f"{total_valorization:+}",
    )

@crypto.route("/manage")
def manage():
    pass


@crypto.route("/add")
def add():
    pass

@crypto.route("/quick-add")
def quick_add():
    pass


@crypto.route("/edit/")
def edit():
    pass

@crypto.route("/delete/")
def delete():
    pass


@crypto.route("/chart")
def chart():
    pass