from . import authentification_blueprint as authentification
from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from project import db, mail
from .models import User
from .forms import (
    SignupForm,
    LoginForm,
    ForgotPasswordForm,
    ResetPasswordFrorm,
)
from flask_login import login_user, current_user, login_required, logout_user
from flask_mail import Message
from itsdangerous.url_safe import URLSafeTimedSerializer
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


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
            flash("Identifiant ou mot de passe incorrect.", "danger")
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
        password = form.password_new.data
        user = User.query.filter_by(email=email).first()
        # if a user is found, we want to redirect back
        # to the login page so user can login.
        if user:
            flash(
                "Un compte a déjà été créé avec cette adresse mail.", "warning"
            )
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
        flash("Votre compte a bien été enregistré.", "success")
        return redirect(url_for("authentification.login"))
    return render_template(
        "authentification/signup.html", form=form, current_page="signup"
    )


@authentification.route("/logout")
@login_required
def logout():
    logout_user()
    flash("A bientot", "success")
    return redirect(url_for("authentification.login"))


@authentification.route("/forgot-password", methods=["GET", "POST"])
def forgot():
    form = ForgotPasswordForm(request.form)
    if request.method == "POST" and form.validate():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            password_reset_serializer = URLSafeTimedSerializer(
                environ.get("SECRET_KEY")
            )
            password_reset_url = url_for(
                "authentification.reset",
                token=password_reset_serializer.dumps(
                    email, salt=environ.get("PASSWORD_SALT")
                ),
                _external=True,
            )

            html = render_template(
                "authentification/password_reset_email.html",
                password_reset_url=password_reset_url,
            )
            msg = Message(
                "Réinitialisation du mot de passe Crypto Tracker",
                recipients=[email],
                html=html,
            )
            mail.send(msg)
            flash(
                "Vous allez recevoir un mail pour réinitialiser votre "
                "mot de passe.(vérifier aussi dans la catégorie spam)",
                "success",
            )
        else:
            flash(
                "Cette adresse e-mail n'est reliée à aucun compte.", "warning"
            )
    return render_template("authentification/forgot.html", form=form)


@authentification.route("/reset-password/<token>", methods=["GET", "POST"])
def reset(token):
    try:
        password_reset_serializer = URLSafeTimedSerializer(
            environ.get("SECRET_KEY")
        )
        email = password_reset_serializer.loads(
            token, salt=environ.get("PASSWORD_SALT"), max_age=900
        )
    except:
        flash("Le lien est invalide ou a expiré.", "danger")
        return redirect(url_for("authentification.login"))
    form = ResetPasswordFrorm(request.form)
    if request.method == "POST" and form.validate():
        password = form.password_new.data
        user = User.query.filter_by(email=email).first_or_404()
        user.password = generate_password_hash(password, method="sha256")
        db.session.add(user)
        db.session.commit()
        flash("Votre mot de passe a été mise à jour.", "success")
        return redirect(url_for("authentification.login"))
    return render_template("authentification/forgot.html", form=form)
