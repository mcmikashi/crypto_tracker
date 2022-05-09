from . import cryptocurrency_blueprint as crypto
from flask import render_template, request, flash, url_for, redirect
from .utils import get_user_current_total_valorization
from flask_login import login_required, current_user
from .forms import PurchaseForm, QuickPurchaseForm, DeletePurchaseForm
from project import db
from .models import Cryptocurrency, Purchase, QuoteCurrency, Profit
from sqlalchemy.sql import desc
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from datetime import date, timedelta


@crypto.route("/")
@login_required
def home():
    cryptocurrencys, total_valorization = get_user_current_total_valorization(
        current_user.id
    )
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


@crypto.route("/delete/<int:pk>", methods=["GET", "POST"])
@login_required
def delete(pk):
    purchase = Purchase.query.get_or_404(pk)
    # if the current user is not the purchase user
    # redirect to the manage page
    if purchase.user_id != current_user.id:
        return redirect(url_for("cryptocurrency.manage"))
    form = DeletePurchaseForm(request.form)
    form.id_purchase.data = purchase.id
    if request.method == "POST" and form.validate():
        # if the id of the purchase is not the same
        # as the id purchase of the form we redirect
        # to the manage page this SHOULD NEVER HAPPEN
        if purchase.id == form.id_purchase.data:
            db.session.delete(purchase)
            db.session.commit()
            flash(
                "Votre achats a bien été suprimmé.",
                "success",
            )
            return redirect(url_for("cryptocurrency.manage"))
    return render_template(
        "cryptocurrency/delete.html", form=form, purchase=purchase
    )


@crypto.route("/chart")
@login_required
def chart():
    profit_dict = dict()
    profit_list = Profit.query.filter(
        Profit.user_id == current_user.id
    ).order_by(desc(Profit.date)).limit(30)
    for item in profit_list[::-1]:
        # Get the datetime and turn it into string date
        the_date = item.date.date().strftime("%d/%m/%Y")
        profit_dict.update({the_date: item.profit_and_loss})

    # If the user doesn't have profit histori
    # we show him yesterday date with 0 profit
    if profit_dict == dict():
        yesterday = date.today() - timedelta(days=1)
        new_key = yesterday.strftime("%d/%m/%Y")
        profit_dict[new_key] = 0
    # Create a new key with today is date
    new_key = date.today().strftime("%d/%m/%Y")
    profit_dict[new_key] = get_user_current_total_valorization(
        current_user.id, True
    )
    # color
    primary_black = "#100f0f0f"
    primary_grey = "#efefef"
    primary_green = "#1fc36c"
    # Data for plotting
    fig, ax = plt.subplots(facecolor=primary_black)
    ax.plot(profit_dict.keys(), profit_dict.values(), color=primary_green)
    ax.set(xlabel="Date", ylabel="Gain ou Perte (€)", facecolor=primary_black)
    # Change color of the spines
    ax.spines["bottom"].set_color(primary_grey)
    ax.spines["left"].set_color(primary_grey)
    # Change color of the label
    ax.yaxis.label.set_color(primary_grey)
    ax.xaxis.label.set_color(primary_grey)
    # Rotates and right-aligns the x labels so they don't crowd each other.
    for label in ax.get_xticklabels(which="major"):
        label.set(rotation=30, horizontalalignment="right",size=8)
    ax.tick_params(axis="both", colors=primary_grey)
    # Remove top and rigth spines
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    buf = BytesIO()
    # Change the size of the image
    fig.set_size_inches((8, 8))
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    graph = base64.b64encode(buf.getbuffer()).decode("ascii")
    return render_template(
        "cryptocurrency/chart.html", graph=graph, current_page="graphique"
        
    )
