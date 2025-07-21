from flask import Flask, request, render_template, redirect
from database import init_db, db_session
from models import Product
from sqlalchemy.exc import IntegrityError

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

if __name__ == "__main__":
    app.run(debug=True)
