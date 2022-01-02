import requests
import pprint


from pymongo import MongoClient


client = MongoClient()
db = client.pchome
coll = db.products

# name contains
# 括號內可放條件,用字典裝起來find ({'name':'Evan'})
# namee_condition = {'name': {'$regex': '.*asus.*', '$options': 'i'}}
# data = coll.find(name_condition)

# comparison opertator (price > 3000)
# price_condition = {'price': {'$gt': 19000}}
# data = coll.find(price_condition)

# # and opertator example
# data = coll.find({'$and': [namee_condition,price_condition]})

# for d in data:
#     print(d['name'], '\n', d['price'])

# update
# coll.update_one({'name': '【福利品】ASUS 華碩 PG348Q 34型 IPS 曲面電競螢幕'}, {'$set': {'price': 31800}})
# data =coll.find_one({'name':'【福利品】ASUS 華碩 PG348Q 34型 IPS 曲面電競螢幕'}) 
# print(data['name'], data['price'])


# insert if not exist (使用update_one 搭配options upsert = True來達成)
# coll.update_one({'name': 'Evan'}, {'$set': {'name': 'Evan'}}, upsert=True )

# delete
coll.delete_one({'name': 'Evan'})




