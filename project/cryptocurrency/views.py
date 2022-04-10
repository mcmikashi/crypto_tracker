from . import cryptocurrency_blueprint as crypto

@crypto.route("/")
def home():
    pass


@crypto.route("/manage")
def manage():
    pass


@crypto.route("/add")
def add():
    pass

@crypto.route("/quick-add")
def quick_add():
    pass


@crypto.route("/edit/")
def edit():
    pass

@crypto.route("/delete/")
def delete():
    pass


@crypto.route("/chart")
def chart():
    pass