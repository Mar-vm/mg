from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__, static_folder='static')

# Conexión MongoDB
uri = "laURL"
client = MongoClient(uri)

db = client["restaurants_db"]
collection = db["restaurants"]

# -------------------------
# READ + FILTRO
# -------------------------
@app.route("/")
def index():
    borough = request.args.get("borough")
    cuisine = request.args.get("cuisine")

    query = {}

    if borough:
        query["borough"] = borough
    if cuisine:
        query["cuisine"] = cuisine

    restaurants = list(collection.find(query))
    total = len(restaurants)

    return render_template("index.html", restaurants=restaurants, total=total)


# -------------------------
# CREATE
# -------------------------
@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        new_restaurant = {
            "name": request.form["name"],
            "borough": request.form["borough"],
            "cuisine": request.form["cuisine"],
            "address": {
                "zipcode": request.form["zipcode"]
            }
        }

        collection.insert_one(new_restaurant)
        return redirect("/")

    return render_template("create.html")


# -------------------------
# UPDATE
# -------------------------
@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    restaurant = collection.find_one({"_id": ObjectId(id)})

    if request.method == "POST":
        collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "name": request.form["name"],
                "cuisine": request.form["cuisine"]
            }}
        )
        return redirect("/")

    return render_template("edit.html", restaurant=restaurant)


# -------------------------
# DELETE
# -------------------------
@app.route("/delete/<id>")
def delete(id):
    collection.delete_one({"_id": ObjectId(id)})
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)