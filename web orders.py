# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 11:10:55 2017

@author: Tony
"""
import requests
from requests_oauthlib import OAuth1Session
from requests_oauthlib import OAuth1 as OAuth
import pandas as pd
import numpy as np
import json
from pandas.io.json import json_normalize

url = r'https://modernica.net/shop/index.php/'
client_key = '41a9c59ef8f373e9746609559e4287f2'
client_secret = '523a185f096691cb9c55e3f935b6725a'
resource_owner_key = 'ee1d47aa95bb20126fccc6f334b9374f'
resource_owner_secret = 'ba101e6ce8110763a2b050823150c6ca'

oauth = OAuth(client_key, client_secret, resource_owner_key, resource_owner_secret)
h = {'Content-Type': 'application/json', 'Accept': 'application/json'}
uri = 'https://modernica.net/shop/api/rest/'
# magento api can only return 100 records per call
params = {'page': 20, 'limit':100}


products0 = requests.get(url='https://modernica.net/shop/api/rest/products',headers=h, auth=oauth)
products = products0.json()

# building dataframe for orders
oi = requests.get(url='https://modernica.net/shop/api/rest/orders/1040/items', headers=h, auth=oauth, params=params)

'''
generate order numbers 1 by 1
appened to uri for auth url
retreive order items
send to dataframe
modify params for next set of 100 orders
'''

o = requests.get(url='https://modernica.net/shop/api/rest/orders/', headers=h, auth=oauth, params=params)

# convert response objects to text
oi_t = oi.text
order_items = pd.read_json(oi_t, orient='index')

o_t = o.text
order_details = pd.read_json(o_t, orient='index')

# shipping info
order_add = pd.read_json(haha.addresses.to_json(), orient='index')
add_bill = pd.read_json(order_add[0].to_json(), orient='index')
add_ship = pd.read_json(order_add[1].to_json(), orient='index')

# items
items = pd.DataFrame.from_dict(haha.order_items.to_dict(), orient='index')

#use dict instead of json because of varying lengths. 'ragged array'
item1 = pd.read_json(items[0].to_json(), orient='index')
item1.columns
item3 = pd.read_json(items[2].to_json(), orient='index')

def extract(df):
    ix = pd.read_json(df, orient='index')
    return ix

items.apply(lambda x: x.to_json())
items.apply(lambda x: pd.read_json(x, orient='index')

for column in items:
    pd.read_json(items[column].to_json(), orient='index')
    