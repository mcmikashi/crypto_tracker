from wtforms import (
    Form,
    SelectField,
    DecimalField,
    validators,
    HiddenField
)


class PurchaseForm(Form):
    cryptocurrency = SelectField(
        "Crypto monnaie",
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
        "Crypto monnaie",
        coerce=int,
    )
    quantity = DecimalField(
        "Quantité",
        [validators.DataRequired()],
        render_kw={"placeholder": "Quantité"},
    )


class DeletePurchaseForm(Form):
    id_purchase = HiddenField()