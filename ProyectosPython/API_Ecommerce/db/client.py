import sys
from pymongo import MongoClient

if "pytest" in sys.modules:
    client = MongoClient()
    db = client.local
    users_collection = db.test_users
else:
    client = MongoClient()#.local.users
    db = client.local
    users_collection = db.users
