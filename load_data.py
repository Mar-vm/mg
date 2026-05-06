import json
from pymongo import MongoClient

uri = "laURL"
client = MongoClient(uri)

db = client["restaurants_db"]
collection = db["restaurants"]

data = []

with open("restaurants.json", encoding="utf-8") as file:
    for line in file:
        data.append(json.loads(line))

collection.insert_many(data)

print("Datos cargados correctamente ")
