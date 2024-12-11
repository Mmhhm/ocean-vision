from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

# Todo remove
# client = MongoClient('mongodb://root:example@localhost:27017/')
db = client['ocean_vision']
collection = db['raw_data']