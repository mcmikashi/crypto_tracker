from wtforms import (
    Form,
    StringField,
    EmailField,
    PasswordField,
    validators,
    BooleanField,
)


class SignupForm(Form):

    first_name = StringField(
        "Prenom",
        [
            validators.DataRequired(),
            validators.Length(2, 75),
            validators.Regexp(
                "^[a-zA-Z-]+$",
                message="Ce prénom contient des caractères non autorisés.",
            ),
        ],
        description="fa-solid fa-user",
        render_kw={"placeholder": "Prenom"},
    )
    last_name = StringField(
        "Nom",
        [
            validators.DataRequired(),
            validators.Length(2, 75),
            validators.Regexp(
                "^[a-zA-Z-]+$",
                message="Ce nom contient des caractères non autorisés.",
            ),
        ],
        description="fa-solid fa-user",
        render_kw={"placeholder": "Nom"},
    )
    email = EmailField(
        "E-mail",
        [validators.DataRequired(), validators.Email()],
        description="fa-solid fa-at",
        render_kw={"placeholder": "E-mail"},
    )
    password_new = PasswordField(
        "Mot de passe",
        [
            validators.DataRequired(),
            validators.EqualTo(
                "confirm", message="Les mots de passe doivent correspondre."
            ),
            validators.Regexp(
                "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&+-;])"
                "[A-Za-z\d@$!%*#?&+-;]{8,24}$",
                message="Le mot de passe doit avoir une longueur comprise "
                "entre 8 et 24 caractères et doit contenir une"
                "majuscule une minuscule et l'un des symboles suivants"
                ": @$!%*#?&+-;",
            ),
        ],
        description="fa-solid fa-lock",
        render_kw={"placeholder": "Mot de passe"},
    )
    confirm = PasswordField(
        "Répeter le Mot de passe",
        description="fa-solid fa-lock",
        render_kw={"placeholder": "Répeter le Mot de passe"},
    )


class LoginForm(Form):
    email = EmailField(
        "E-mail",
        [validators.DataRequired(), validators.Email()],
        description="fa-solid fa-at",
        render_kw={"placeholder": "E-mail"},
    )
    password = PasswordField(
        "Mot de passe",
        [validators.DataRequired(), validators.Length(1, 150)],
        description="fa-solid fa-lock",
        render_kw={"placeholder": "Mot de passe"},
    )
    remember = BooleanField("Se souvenir de moi")


class ForgotPasswordForm(Form):
    email = EmailField(
        "E-mail",
        [validators.DataRequired(), validators.Email()],
        description="fa-solid fa-at",
        render_kw={"placeholder": "E-mail"},
    )


class ResetPasswordFrorm(Form):
    password_new = PasswordField(
        "Mot de passe",
        [
            validators.DataRequired(),
            validators.EqualTo(
                "confirm", message="Les mots de passe doivent correspondre."
            ),
            validators.Regexp(
                "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&+-;])"
                "[A-Za-z\d@$!%*#?&+-;]{8,24}$",
                message="Le mot de passe doit avoir une longueur comprise "
                "entre 8 et 24 caractères et doit contenir une"
                "majuscule une minuscule et l'un des symboles suivants"
                ": @$!%*#?&+-;",
            ),
        ],
        description="fa-solid fa-lock",
        render_kw={"placeholder": "Mot de passe"},
    )
    confirm = PasswordField(
        "Répeter le Mot de passe",
        description="fa-solid fa-lock",
        render_kw={"placeholder": "Répeter le Mot de passe"},
    )
