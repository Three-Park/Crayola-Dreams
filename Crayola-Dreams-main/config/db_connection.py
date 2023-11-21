from pymongo import MongoClient
uri="mongodb://threepark:y397jue3kPm8WbLo@ac-8a1feb0-shard-00-00.ot5bv2g.mongodb.net:27017,ac-8a1feb0-shard-00-01.ot5bv2g.mongodb.net:27017,ac-8a1feb0-shard-00-02.ot5bv2g.mongodb.net:27017/?ssl=true&replicaSet=atlas-bv7ifs-shard-0&authSource=admin&retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri)

for db_name in client.list_database_names():
    print(db_name)

client.close()