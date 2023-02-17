from pymongo import MongoClient

# replace <username>, <password>, <dbname>, and <clustername> with your actual values
# connection_string = f"mongodb+srv://<username>:<password>@<clustername>.mongodb.net/<dbname>?retryWrites=true&w=majority"
# client = MongoClient(connection_string)

# # test the connection
# db = client.test
# collection = db.test_collection
# collection.insert_one({'test': 'test'})
# This will create a new document in a collection called test_collection in the test database of your MongoDB cluster.
client = MongoClient("mongodb://localhost:27017/")
db = client["buchidb"]
# adoptions = db["adoptions"]
# customers = db["customers"]
# pets = db["pets"]
