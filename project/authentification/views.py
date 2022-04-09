from . import authentification_blueprint as authentification


@authentification.route("/login")
def login():
    pass


@authentification.route("/signup")
def signup():
    pass


@authentification.route("/logout")
def logout():
    pass
