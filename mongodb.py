from pymongo import MongoClient
client = MongoClient("mongodb+srv://user:Passw0rd@aliciaproject-fn9lx.mongodb.net/test?retryWrites=true&w=majority")
db = client.get_database('aliciaDB')
collection_feedback = db.feedback
