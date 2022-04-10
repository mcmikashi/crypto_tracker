from . import authentification_blueprint as authentification
from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from project import db
from .models import User
from .forms import SignupForm, LoginForm
from flask_login import login_user, current_user,login_required ,logout_user


@authentification.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    email = request.form.get("email")
    password = request.form.get("password")
    remember = request.form.get("remember")
    if current_user.is_authenticated:
        return redirect(url_for("cryptocurrency.home"))
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash("Identifiant ou mot de passe incorrect.","danger")
            return redirect(url_for("authentification.login"))
        else:
            login_user(user, remember=remember)
            return redirect(url_for("cryptocurrency.home"))
    return render_template(
        "authentification/login.html", form=form, current_page="login"
    )


@authentification.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm(request.form)
    if request.method == "POST" and form.validate():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        # if a user is found, we want to redirect back 
        # to the login page so user can login.
        if user : 
            flash("Un compte a déjà été créé avec cette adresse mail.",
                  "warning")
            return redirect(url_for("authentification.login"))
        # create a new user with the form data. 
        # Hash the password so the plaintext version isn't saved.
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=generate_password_hash(password, method="sha256"),
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Votre compte a bien été enregistré.","success")
        return redirect(url_for("authentification.login"))
    return render_template(
        "authentification/signup.html", form=form, current_page="signup"
    )


@authentification.route("/logout")
@login_required
def logout():
    logout_user()
    flash("A bientot","success")
    return redirect(url_for("authentification.login"))
