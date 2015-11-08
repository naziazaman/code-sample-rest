import pymongo

PRODUCTS_PER_PAGE = 10
connection_string = "mongodb://localhost:27017"
client = pymongo.MongoClient(connection_string)
db = client.product_database
collection = db.product_collection

products = db.products