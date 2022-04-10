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
        [validators.DataRequired(), validators.Length(2, 75)],
        description="fa-solid fa-user",
        render_kw={"placeholder": "Prenom"},
    )
    last_name = StringField(
        "Nom",
        [validators.DataRequired(), validators.Length(2, 75)],
        description="fa-solid fa-user",
        render_kw={"placeholder": "Nom"},
    )
    email = EmailField(
        "E-mail",
        [validators.DataRequired(), validators.Email()],
        description="fa-solid fa-at",
        render_kw={"placeholder": "E-mail"},
    )
    password = PasswordField(
        "Mot de passe",
        [
            validators.DataRequired(),
            validators.EqualTo(
                "confirm", message="les mots de passe doivent correspondre"
            ),
            validators.Length(6, 150),
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
