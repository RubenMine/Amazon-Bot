from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class Product:
    def __init__(self, dictProduct) -> None:
        self.ID = dictProduct["ID"]
        self.quantity = dictProduct["quantity"]
        self.price = (float) (dictProduct["price"])
        self.errorPrice = (float) (dictProduct["errorPrice"])

    def __str__(self):
        minPrice = self.price - self.errorPrice
        maxPrice = self.price + self.errorPrice
        string = "ID: {} | ".format(self.ID) +\
                 "Quantity: {} | ".format(self.quantity) +\
                 "Price: {} - {}".format(minPrice, maxPrice)
        return string


class WebBrowser:
    def __init__(self, url: str) -> None:
        self.url = url
        self.browser = webdriver.Firefox()
    
    def connectAndLogin(self, email: str, pswd: str):
        self.browser.get(self.url)
        temp = self.browser.find_element(By.ID, "nav-link-accountList")
        temp.click()
        temp = self.browser.find_element(By.ID, "ap_email")
        temp.send_keys(email, Keys.ENTER)
        temp = self.browser.find_element(By.ID, "ap_password")
        temp.send_keys(pswd, Keys.ENTER)

class AmazonBot:
    def __init__(self, email: str, pswd: str, url: str) -> None:
        self.auth = {
            "email": email,
            "pswd": pswd,
        }
        self.browser = WebBrowser(url)
        self.products = []

    def addProduct(self, product: Product):
        self.products.append(product)

    def checkProducts():
        pass

    def buyProduct(product: Product):
        pass

    def run(self):
        self.browser.connectAndLogin(self.auth["email"], self.auth["pswd"])

    
    def __str__(self):
        string = "Email: {}\nPassword: {}".format(self.auth["email"], self.auth["pswd"])
        for p in self.products:
            string += "\n" + str(p)
        return string