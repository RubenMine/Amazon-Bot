import sys
sys.path.insert(0, 'src')
from src import bot

from selenium import webdriver
from bot import AmazonBot
from bot import Product
from bot import WebBrowser
import json

def fetchData():
    path = "configs\config.json"

    with open(path, "r") as configs:
        global bot
        c = json.loads(configs.read())

        auth = c["Auth"]
        bot = AmazonBot(auth["email"], auth["password"], auth["url"])

        for product in c["Products"]:
            p = Product(product)
            bot.addProduct(p)
    
def main():
    bot.run()

if __name__ == "__main__":
    fetchData()
    main()