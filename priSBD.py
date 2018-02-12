import requests
import configparser
import tkinter as tk
from steem.steemd import Steemd

def fetch_json(url):
    data = requests.get(url)
    dataj = data.json()
    return dataj

def fetch_sbd_balance(nodes, username):
    steemd = Steemd(nodes)
    balance = steemd.get_account(username)['sbd_balance']
    balance = balance.strip(' SBD')
    return float(balance)

def usd_to_currency(currency_data, currency, amount):
    conv_rate = currency_data['rates'][currency]
    return float(amount)*float(conv_rate)

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    sbd_data = fetch_json(config['URLS']['sbd_api'])[0]
    currency_data = fetch_json(config['URLS']['currency_api'])
    main_node = config.get('URLS', 'steemd_nodes')
    steemd_nodes = list()
    steemd_nodes.append(main_node )

    sbd_usd = float(sbd_data['price_usd'])
    available_currencies = [key for key in currency_data['rates']]

    print("1 SBD equals $" + str(sbd_usd) + ".")
    username = input("What's your username?: ")
    owned_sbd = fetch_sbd_balance(steemd_nodes, username)
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