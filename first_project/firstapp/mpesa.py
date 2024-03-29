import requests
from requests.auth import *
import json
import os 
import datetime

from dotenv import load_dotenv

load_dotenv()



# getting the credentials
def get_token():
    url = os.getenv("url")
    key=os.getenv("key")
    secret=os.getenv("secret")
    res=requests.get(url,auth=HTTPBasicAuth(key,secret))
    return json.loads(res.text)["access_token"]

# initiate stk-push 
def stk_push(phone,amount):
    url='https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    headers={"Authorization":f"Bearer {get_token()}","Content-type":"application/json"}
    req={
        "BusinessShortCode": 174379,
    "Password": os.getenv("password"),
    "Timestamp": "20220913114249",
    "TransactionType": "CustomerPayBillOnline",
    "Amount": amount,
    "PartyA": phone,
    "PartyB": 174379,
    "PhoneNumber": phone,
    "CallBackURL":os.getenv("conf_url"),
    "AccountReference": "CompanyXLTD",
    "TransactionDesc": "Payment of X" 
    }
    resp=requests.post(url,json=req,headers=headers)

    return {"info":json.loads(resp.text)},200

def c_2_b_reg_url():


    url = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl'
    headers = { 'Authorization': f"Bearer {get_token()}"}

    req_body = {    
                   "ShortCode": 600991,
                   "ResponseType":"Completed",
                   "ConfirmationURL":os.getenv("conf_url"),
                   "ValidationURL":os.getenv("val_url"),
    }
    

    resp = requests.post(url,json=req_body,headers=headers)
    
    return resp.json()

def sim_c_2_b():
     
    url = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate'

    headers = { 'Authorization': f"Bearer {get_token()}"}

    req_body = {
            "ShortCode": 600991,
    "CommandID": "CustomerBuyGoodsOnline",
    "Amount": 100,
    "Msisdn": "254705912645",
    "BillRefNumber": "",
    }

    response = requests.post(url,json=req_body,headers=headers)
    return response.json()

