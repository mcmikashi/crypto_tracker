from . import cryptocurrency_blueprint as crypto
from flask import render_template, request, flash
from .utils import (
    get_user_current_total_valorization,
)
from flask_login import login_required, current_user
from .forms import PurchaseForm
from project import db
from .models import Cryptocurrency,Purchase

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


@crypto.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = PurchaseForm(request.form)
    form.cryptocurrency.choices = [
        (item.id, f"{item.symbol} ({item.name})")
        for item in Cryptocurrency.query.all()
    ]
    if request.method == "POST" and form.validate():
        new_purchase = Purchase(
            user_id=current_user.id,
            cryptocurrency_id=form.cryptocurrency.data,
            price=form.price.data,
            quantity=form.quantity.data,
        )
        db.session.add(new_purchase)
        db.session.commit()
        flash("Votre achats a bien été ajouté.", "success")
    return render_template(
        "cryptocurrency/add_edit.html",
        form=form,
        quick=True,
        current_page="add",
    )

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