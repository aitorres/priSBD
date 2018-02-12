import settings
import requests
import tkinter as tk
from steem.steemd import Steemd

def fetch_json(url):
    data = requests.get(url)
    dataj = data.json()
    return dataj

def fetch_sbd_balance(username):
    steemd = Steemd(settings.steemd_nodes)
    balance = steemd.get_account(username)['sbd_balance']
    balance = balance.strip(' SBD')
    return balance

def main():
    sbd_data = fetch_json(settings.sbd_api_url)
    currency_data = fetch_json(settings.currency_api_url)
    steem = Steemd(settings.steemd_nodes)
    
    
if __name__ == '__main__':
    main()