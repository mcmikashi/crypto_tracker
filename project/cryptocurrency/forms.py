from wtforms import (
    Form,
    SelectField,
    DecimalField,
    validators,
)


class PurchaseForm(Form):
    cryptocurrency = SelectField(
        "Crypto monaie",
        coerce=int,
    )
    price = DecimalField(
        "Prix", [validators.DataRequired()], render_kw={"placeholder": "Prix"}
    )
    quantity = DecimalField(
        "Quantité",
        [validators.DataRequired()],
        render_kw={"placeholder": "Quantité"},
    )

class QuickPurchaseForm(Form):
    cryptocurrency = SelectField(
        "Crypto monaie",
        coerce=int,
    )
    quantity = DecimalField(
        "Quantité",
        [validators.DataRequired()],
        render_kw={"placeholder": "Quantité"},
    )
