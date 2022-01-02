import requests
import pprint
import re

from pymongo import MongoClient
client = MongoClient()


for i in range(1, 101):
    url ='https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=%E6%9B%B2%E9%9D%A2%E8%9E%A2%E5%B9%95&page={}&sort=sale/dc'.format(i) 
    r = requests.get(url)
    if r.status_code != requests.codes.ok:
        print(i)
        print('error', status_code)
        continue

    else:
        try:
            data = r.json()
            for product in data['prods']:
                client.pchome.products.insert_one(product)

        except:
            print('ERROR',data)





    