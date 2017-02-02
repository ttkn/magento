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
uri = 'https://modernica.net/shop/api/rest/orders'

def orders(uri, pages, startpg):
    # order details producer
    df_final = pd.DataFrame()
    def unpk(df):
        # each item/address in an order is stored in its own JSON
        print('pg {}. {} pages remaining.'.format(startpg, pages))
        unpacked = pd.DataFrame()
        for column in df:
            # take each JSON and append to new dataframe
            a = pd.read_json(df[column].to_json(), orient='index')
            unpacked = unpacked.append(a)
        return unpacked
    # main evaluation loop, order details returned from magento's api change for each iteration
    while pages > 0:
        params = {'page':startpg, 'limit':100}
        o = requests.get(uri, headers=h, auth=oauth, params=params)
        # convert response objects to text for reading into df
        o_t = o.text
        order_details = pd.read_json(o_t, orient='index')
        # sub dataframes for items and addresses
        # use dict instead of json because of varying lengths. 'ragged array'
        order_items = pd.DataFrame.from_dict(order_details.order_items.to_dict(), orient='index')
        address = pd.DataFrame.from_dict(order_details.addresses.to_dict(), orient='index')
        # extract the nest JSONs from each
        df_i = unpk(order_items)
        df_a = unpk(address)
        # use outer join on the results
        combine = pd.merge(df_i, df_a, how='outer', left_index=True, right_index=True)
        df_final = df_final.append(combine)
        startpg += 1
        pages -= 1
    # filter out empty rows ('None' values in name) and duplicate items (NaN values in base_original_price)
    df_final = df_final.dropna(subset=['name', 'base_original_price'])
    return df_final

orders_complete = orders(uri, 24, 1)
orders_complete.to_csv('magento orders 2-1-2017.csv')
order_details.to_csv('magento 2-1-2017.csv')
# for future extraction: startpg 24 - 2/1/2017
 
products0 = requests.get(url='https://modernica.net/shop/api/rest/products',headers=h, auth=oauth)
products = products0.json()
