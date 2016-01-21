import pymongo
import os
try:
	connection = pymongo.MongoClient(os.environ['OPENSHIFT_MONGODB_DB_URL'])
except:
	connection = pymongo.MongoClient("mongodb://localhost")
db= connection['wingify']        
users = db.users
store = db.store