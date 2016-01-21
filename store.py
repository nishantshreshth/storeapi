from config import store
from bson.objectid import ObjectId
from flask import jsonify
from pymongo import ASCENDING, DESCENDING
import json

class Store:
	def __init__():
		pass

	@classmethod
	def modify(cls, item):
		item['itemid']=str(item['_id'])
		item.pop('_id')
		return item

	@classmethod
	def get_all(cls):
		items=[]
		for item in store.find().sort("price"):
			items.append(cls.modify(item))
		return items

	@classmethod
	def insert_item(cls, item):
		item_id=store.insert(item)
		return cls.modify(item)



	@classmethod
	def gen_query(cls,q):
		q_dict={}
		if 'name' in q:
			q_dict['name']={"$regex" : ".*"+q['name'].lower()+".*"}
		if 'seller' in q:
			q_dict['seller']={"$regex" : ".*"+q['seller'].lower()+".*"}
		if 'category' in q:
			q_dict['seller']={"$regex" : ".*"+q['category'].lower()+".*"}
		return q_dict


	@classmethod
	def search_items(cls, query):
		items=[]
		direction=None
		if 'lowtohigh' in query and query['lowtohigh']=="1":
			direction=ASCENDING
		if 'hightolow' in query and query['hightolow']=="1":
			print "YES"
			direction=DESCENDING
		query=cls.gen_query(query)
		for item in store.find(query).sort("price", direction):
			items.append(cls.modify(item))
		return items



	@classmethod
	def delete_item(cls, itemid):
		try:
			store.remove({"_id":ObjectId(str(itemid))})
			return 200
		except:
			return 404
		return 404



	@classmethod
	def update(cls, itemid, item):
		try:
			chk=store.find_one({"_id": ObjectId(itemid)})
		except:
			chk=None
		T={"$set":{}}
		for k in item:
			T["$set"][k]=item[k]
		if chk!=None:
			store.update({"_id": ObjectId(itemid)},T)
			item=store.find_one({"_id": ObjectId(itemid)})
			return cls.modify(item)
		return 404

