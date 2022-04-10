from . import cryptocurrency_blueprint as crypto
from flask import render_template, request, flash, url_for, redirect
from .utils import (
    get_user_current_total_valorization,
)
from flask_login import login_required, current_user
from .forms import PurchaseForm,QuickPurchaseForm
from project import db
from .models import Cryptocurrency,Purchase,QuoteCurrency
from sqlalchemy.sql import desc

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
@login_required
def manage():
    purchase_historic = Purchase.query.filter(
        Purchase.user_id == current_user.id
    ).all()
    return render_template(
        "cryptocurrency/manage.html",
        purchases=purchase_historic,
        current_page="admin",
    )


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

@crypto.route("/quick-add", methods=["GET", "POST"])
@login_required
def quick_add():
    form = QuickPurchaseForm(request.form)
    form.cryptocurrency.choices = [
        (item.id, f"{item.symbol} ({item.name})")
        for item in Cryptocurrency.query.all()
    ]
    if request.method == "POST" and form.validate():
        last_quote = (
            QuoteCurrency.query.filter(
                QuoteCurrency.cryptocurrency_id == form.cryptocurrency.data
            )
            .order_by(desc(QuoteCurrency.date))
            .first()
        )
        new_purchase = Purchase(
            user_id=current_user.id,
            cryptocurrency_id=form.cryptocurrency.data,
            price=(last_quote.price * float(form.quantity.data)),
            quantity=form.quantity.data,
        )
        db.session.add(new_purchase)
        db.session.commit()
        flash("Votre achats a bien été ajouté.", "success")
    return render_template(
        "cryptocurrency/add_edit.html", form=form, current_page="quick_add"
    )


@crypto.route("/edit/<int:pk>", methods=["GET", "POST"])
@login_required
def edit(pk):
    purchase = Purchase.query.get_or_404(pk)
    # if the current user is not the purchase user
    # redirect to the manage page
    if purchase.user_id != current_user.id:
        return redirect(url_for("cryptocurrency.manage"))
    if request.method == "POST":
        form = PurchaseForm(request.form)
        purchase.cryptocurrency_id = form.cryptocurrency.data
        purchase.quantity = form.quantity.data
        purchase.price = form.price.data
        db.session.commit()
        flash(
            "Votre achats a bien été mise à jour.",
            "success",
        )
    else:
        form = PurchaseForm()
        form.cryptocurrency.choices = [
            (item.id, f"{item.symbol} ({item.name})")
            for item in Cryptocurrency.query.all()
        ]
        form.cryptocurrency.data = purchase.cryptocurrency.id
        form.price.data = purchase.price
        form.quantity.data = purchase.quantity
    return render_template(
        "cryptocurrency/add_edit.html",
        form=form,
        purchase=purchase,
        edit=True,
        back_link=True,
    )

@crypto.route("/delete/")
def delete():
    pass


@crypto.route("/chart")
def chart():
    pass