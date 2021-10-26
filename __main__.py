from selenium import webdriver
from src.bot import AmazonBot, Product
import json

def fetchData():
    path = "Amazon-Bot\configs\config.json"

    with open(path, "r") as configs:
        global bot
        c = json.loads(configs.read())

        auth = c["Auth"]
        bot = AmazonBot(auth["url"], auth["email"], auth["password"], auth["delay"])

        for product in c["Products"]:
            p = Product(product)
            bot.add_product(p)
    
def main():
    bot.run()

if __name__ == "__main__":
    fetchData()
    main()