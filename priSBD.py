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
    return float(balance)

def usd_to_currency(currency_data, currency, amount):
    conv_rate = currency_data['rates'][currency]
    return float(amount)*float(conv_rate)

def main():
    sbd_data = fetch_json(settings.sbd_api_url)[0]
    currency_data = fetch_json(settings.currency_api_url)
    steem = Steemd(settings.steemd_nodes)

    sbd_usd = float(sbd_data['price_usd'])
    available_currencies = [key for key in currency_data['rates']]

    print("1 SBD equals $" + str(sbd_usd) + ".")
    username = input("What's your username?: ")
    owned_sbd = fetch_sbd_balance(username)
    owned_usd = owned_sbd*sbd_usd
    print("You currently have " + str(owned_sbd) + " SBD, equivalent to $" + str(owned_usd) +".")
    print("This is a list of available currencies: ")
    print(available_currencies)
    currency = input("What currency do you want information about?: ")
    converted_sbd = usd_to_currency(currency_data, currency, sbd_usd)
    print("1 SBD equals " + currency + " " + str(converted_sbd) + ".")
    print("You currently have " + str(owned_sbd) + " SBD, equivalent to " + currency + " " + str(usd_to_currency(currency_data, currency, owned_usd)) +".")
    

if __name__ == '__main__':
    main()