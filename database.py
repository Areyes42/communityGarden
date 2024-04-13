from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://delsterone:jVYEYXmkXofN1jH8@cluster0.xf2gegz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1')) # this is what we will use to reference the database client
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
collection = client['gettingStarted']['people']

# create new documents
peopleDocuments = [
    {
      "name": { "first": "Alan", "last": "Turing" },
      "contribs": [ "Turing machine", "Turing test", "Turingery" ],
      "views": 1250000
    }, 
    {
      "name": { "first": "Grace", "last": "Hopper" },
      "contribs": [ "Mark I", "UNIVAC", "COBOL" ],
      "views": 3860000
    }
]
# insert documents
result = collection.find_one({ "name.last": "Turing" })
print(result)
collection.insert_many(peopleDocuments)
print(collection)