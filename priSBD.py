###
# priSBD
# A little GUI utility that let's you check how many
# SBDs you have, and their value in a vast amount of
# different currencies, without a hassle.
# 
# Written by Andrés Ignacio Torres
# MIT Licensed
###

# Importing required libraries and tools
import requests
import configparser
import tkinter as tk
from steem.steemd import Steemd

# Fetches the JSON content of a given url
# Useful for cryptocurrency and fiat currency APIs
def fetch_json(url):
    data = requests.get(url)
    dataj = data.json()
    return dataj

# Fetches a given Steemit user's SBD balance
# Returns a numerical value with up to 3 decimals
def fetch_sbd_balance(nodes, username):
    steemd = Steemd(nodes)
    balance = steemd.get_account(username)['sbd_balance']
    balance = balance.strip(' SBD')
    return float(balance)

# Converts a given amount of US dollars to any
# other currency, given by its three-letter 
# international code
def usd_to_currency(currency_data, currency, amount):
    conv_rate = currency_data['rates'][currency]
    return float(amount)*float(conv_rate)

def set_username(config):
    username = input("What's your username?: ")
    config.set('USER','username', username)
    return

# The main procedure
def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    currency = config['USER']['currency']
    username = config['USER']['username']

    sbd_data = fetch_json(config['URLS']['sbd_api'])[0]
    currency_data = fetch_json(config['URLS']['currency_api'])
    main_node = config['URLS']['steemd_nodes']
    steemd_nodes = list()
    steemd_nodes.append(main_node)

    sbd_usd = float(sbd_data['price_usd'])
    available_currencies = [key for key in currency_data['rates']]

    # maybe insert a while here
    gui = tk.Tk()

    logo = tk.PhotoImage(file="assets/steemit-logo.png")
    logo_label = tk.Label(gui, image=logo)
    logo_label.pack()

    if (username != ""): tk.Label(gui, text="Hello, " + username + "!").pack()

    price_label  = tk.Label(gui, text="1 SBD equals $" + str(sbd_usd) + ".")
    price_label.pack()

    if (username == ""):
        username_not_set_label = tk.Label(gui, text="You have not set your Steemit username yet.")
        username_not_set_label.pack()

        username_set_button = tk.Button(gui, text='Set username', width=25)
        username_set_button.pack()
    else:
        owned_sbd = fetch_sbd_balance(steemd_nodes, username)
        owned_usd = owned_sbd*sbd_usd

        owned_sbd_label = tk.Label(gui, text="You currently have " + str(owned_sbd) + " SBD, equivalent to $" + str(owned_usd) + ".")
        owned_sbd_label.pack()
    
    if (currency == "USD"):
        # print("This is a list of available currencies: ")
        # print(available_currencies)
        # currency = input("What currency do you want information about?: ")
        pass
    elif (currency == ""):
        currency_not_set_label = tk.Label(gui, text="You have not set your prefered currency yet.")
        currency_not_set_label.pack()

        currency_set_button = tk.Button(gui, text= "Set currency", width=25)
        currency_set_button.pack()
    else:
        converted_sbd = usd_to_currency(currency_data, currency, sbd_usd)
        
        in_currency_value_label = tk.Label(gui, text="1 SBD equals " + currency + " " + str(converted_sbd) + ".")
        in_currency_value_label.pack()
    
    if (username != "") and (currency != ""): 
        in_currency_label = tk.Label(gui, text="In your prefered currency, you currently have " + currency + " " + str(usd_to_currency(currency_data, currency, owned_usd)) + ".")
        in_currency_label.pack()

    gui.mainloop()
 
if __name__ == '__main__':
    main()