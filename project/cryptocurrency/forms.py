from wtforms import Form, SelectField, DecimalField, validators, HiddenField


class PurchaseForm(Form):
    cryptocurrency = SelectField(
        "Crypto monnaie",
        coerce=int,
        description="fa-solid fa-magnifying-glass-dollar",
    )
    quantity = DecimalField(
        "Quantité",
        [validators.DataRequired()],
        render_kw={"placeholder": "Quantité"},
        description="fa-solid fa-coins",

    )
    price = DecimalField(
        "Prix", [validators.DataRequired()],
        render_kw={"placeholder": "Prix"},
        description="fa-solid fa-euro-sign",
    )


class QuickPurchaseForm(Form):
    cryptocurrency = SelectField(
        "Crypto monnaie",
        coerce=int,
        description="fa-solid fa-magnifying-glass-dollar",
    )
    quantity = DecimalField(
        "Quantité",
        [validators.DataRequired()],
        render_kw={"placeholder": "Quantité"},
        description="fa-solid fa-coins",
    )


class DeletePurchaseForm(Form):
    id_purchase = HiddenField()
