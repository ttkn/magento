# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 11:10:55 2017
@author: Tony

Creating a process for extracting sales info fom Magento api. Constraints include 
    1. 100 records per api request
    2. JSONS nested within JSONS
    3. unnecessary/duplicate item info for almost every order
Various dataframes created and merged
"""
import requests
from requests_oauthlib import OAuth1Session
from requests_oauthlib import OAuth1 as OAuth
import pandas as pd
import numpy as np
import json
from pandas.io.json import json_normalize

# place oauth details here: client_key, client_secret, resource_owner_key, resource_owner_secret

oauth = OAuth(client_key, client_secret, resource_owner_key, resource_owner_secret)
h = {'Content-Type': 'application/json', 'Accept': 'application/json'}
uri = 'https://modernica.net/shop/api/rest/'

def orders_start(pages, startpg, coroutines):
    # order details producer
    while pages > 0:
        params = {'page':startpg, 'limit':100}
        o = requests.get(url='https://modernica.net/shop/api/rest/orders/', headers=h, auth=oauth, params=params)
        # convert response objects to text for reading into df
        o_t = o.text
        order_details = pd.read_json(o_t, orient='index')
        # send df to shipping & item coroutines
        for coroutine in coroutines:
            coroutine.send(order_details)
        startpg += 1
        pages -= 1
    for coroutine in coroutines:
        coroutine.close()

def items_unpk1(next_coroutine):
    print('initialize order items unpacking')
    try:
        while True:
            df = (yield)
            order_items = pd.DataFrame.from_dict(df.order_items.to_dict(), orient='index')
            next_coroutine.send(order_items)
    except GeneratorExit:
        next_coroutine.close()
        print("=== Done ===")

def items_unpk2(next_coroutine):
    print('order items unpacking stage 2')
    try:
        while True:
            items = (yield)
            df = pd.DataFrame()
            for column in items:
                a = pd.read_json(items[1].to_json(), orient='index')
                df = df.append(a)
        
products0 = requests.get(url='https://modernica.net/shop/api/rest/products',headers=h, auth=oauth)
products = products0.json()

# cannot use; magento's order_id does not correspond to order numbers as seen on invoices
oi = requests.get(url='https://modernica.net/shop/api/rest/orders/order_id/items', headers=h, auth=oauth)

# shipping info
order_add = pd.read_json(order_details.addresses.to_json(), orient='index')
add_bill = pd.read_json(order_add[0].to_json(), orient='index')
add_ship = pd.read_json(order_add[1].to_json(), orient='index')

# order items
items = pd.DataFrame.from_dict(order_details.order_items.to_dict(), orient='index')

#use dict instead of json because of varying lengths. 'ragged array'
item1 = pd.read_json(items[0].to_json(), orient='index')
item1.columns
item3 = pd.read_json(items[2].to_json(), orient='index')

def extract(df):
    ix = pd.read_json(df, orient='index')
    return ix

items.apply(lambda x: x.to_json())
items.apply(lambda x: pd.read_json(x, orient='index')

