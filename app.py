from flask import Flask, request, render_template, redirect, url_for
from database import init_db, db_session
from models import Product, User
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash

app = Flask(__name__)
init_db()

@app.route("/")
def index():
    products = db_session.query(Product).all()
    return render_template("index.html", products=products)

@app.route("/add", methods=["POST"])
def add_product():
    name = request.form["name"]
    price = float(request.form["price"])
    stock = int(request.form["stock"])
    product = Product(name=name, price=price, stock=stock)
    try:
        db_session.add(product)
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User(username=username)
        user.set_password(password)
        try:
            db_session.add(user)
            db_session.commit()
            return redirect(url_for("login"))
        except IntegrityError:
            db_session.rollback()
            error = "使用者名稱已存在"
            return render_template("register.html", error=error)
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = db_session.query(User).filter_by(username=username).first()
        if user and user.check_password(password):
            return redirect(url_for("list_users"))
        else:
            error = "帳號或密碼錯誤"
    return render_template("login.html", error=error)


@app.route("/users")
def list_users():
    users = db_session.query(User).all()
    return render_template("users.html", users=users)

if __name__ == "__main__":
    app.run(debug=True)
