import api
import requests

api = api.LeagueOfLegendsClientAPI()
session = api.get('/lol-login/v1/session').json()
accId = session["accountId"]
transaction = api.get_token('/storefront/v3/history/purchase').json()
transactionId = transaction['transactions']
i = 1
for e in transactionId:
    first = e['transactionId']
    if i == 1:
        break
    i += 1
data = {"accountId":accId,"transactionId":first,"inventoryType":"CHAMPION","language":"en_US"}
boost = api.postRefund('/storefront/v3/refund', data)
