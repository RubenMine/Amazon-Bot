from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import enum
import time


class Status(enum.Enum):
    unavailable = 0
    available = 1
    bought = 2


class Product:
    def __init__(self, dictProduct) -> None:
        self.ASIN = dictProduct["ASIN"]
        self.quantity = dictProduct["quantity"]
        self.price = (float) (dictProduct["price"])
        self.errorPrice = (int) (dictProduct["errorPrice"])
        self.status = Status.unavailable

    def __str__(self):
        minPrice = self.price - self.errorPrice
        maxPrice = self.price + self.errorPrice
        string = "ASIN: {} | ".format(self.ASIN) +\
                 "Quantity: {} | ".format(self.quantity) +\
                 "Price: {} - {}".format(minPrice, maxPrice)
        return string


class WebBrowser:
    def __init__(self, url: str) -> None:
        self.url = url
        self.browser = webdriver.Firefox()
    
    def login(self, email: str, pswd: str, delay: int):
        email_field    = None
        password_field = None
        email_xpath    = '//*[@ID="ap_email"]'      # Email xpath to search in the webpage
        password_xpath = '//*[@ID="ap_password"]'   # Password xpath to search in the webpage
        wait_seconds   = delay                      # Delay to wait before searching for a field (in seconds)

        # Search for the email input field
        try:
            email_field = self.browser.find_element_by_xpath(email_xpath)
            #email_field = WebDriverWait(self.browser, wait_seconds).until(
            #EC.presence_of_element_located((By.XPATH, email_xpath)))
        except:
            print("Can't find field {}".format(email_xpath))
            self.browser.quit()
        else:
            email_field.send_keys(email, Keys.ENTER)
        # Search for the password input field
        try:
            password_field = WebDriverWait(self.browser, wait_seconds).until(
            EC.presence_of_element_located((By.XPATH, password_xpath)))
        except:
            print("Can't find field {}".format(password_xpath))
            self.browser.quit()
        else:
            password_field.send_keys(pswd, Keys.ENTER)

    def search_product(self, ASIN: str):
            product_page = 'http://www.amazon.it/dp/' + ASIN  # Product page for the specified ASIN
            ASIN_regex = r'^B[A-Z 0-9]{9}'
            pattern = re.compile(ASIN_regex)
            # Check if provASINed ASIN matches a basic regex pattern
            #if pattern.match(ASIN):
            self.browser.get(product_page)
                # Check if the product exist by checking the current page title
            if self.browser.title == 'Page Not Found':
                self.browser.quit()
                print("The provASINed ASIN ({}) does not exist".format(ASIN))
           #else:
                self.browser.quit()
                print("The provASINed ASIN is not valASIN")
        
    def is_available(self, price: float, errorPrice: int) -> bool:
        buybutton_xpath = '//*[@id="buy-now-button"]'
        buyprice_xpath = '//*[@id="price_inside_buybox"]'

        try:
            buybutton_field = self.browser.find_element_by_xpath(buybutton_xpath)
            buyprice_field = self.browser.find_element_by_xpath(buyprice_xpath)
        except:
            return False
        else:
            buyprice = (float)(buyprice_field.text[:-1].replace(",", "."))
            if buyprice < price+errorPrice and buyprice > price-errorPrice:
                return True
            else:
                return False
    
    def find_and_click(self, xpath: str):
        a = self.browser.find_element_by_xpath(xpath)
        self.browser.execute_script("arguments[0].click();", a)
            
            
class AmazonBot:
    def __init__(self, url: str, email: str, pswd: str, delay: int) -> None:
        self.auth = {
            "email": email,
            "pswd": pswd,
            "delay": delay
        }
        self.browser = WebBrowser(url)
        self.products = []

    def add_product(self, product: Product):
        self.products.append(product)

    def check_product(self):
        while(len(self.products) >= 1):
            for product in self.products:
                if product.status != Status.bought: 
                    self.browser.search_product(product.ASIN)
                
                
                if product.status == Status.unavailable:
                    product.status = Status.available if self.browser.is_available(product.price, product.errorPrice) else Status.unavailable

                if product.status == Status.bought:
                    self.products.remove(product)    
                elif product.status == Status.available:
                    self.buy_product(product)
                    product.status = Status.bought

                print(product.status)

                time.sleep(1)

    def buy_product(self, product: Product):
        buybutton_xpath = '//*[@id="buy-now-button"]'
        self.browser.find_and_click(buybutton_xpath)

        time.sleep(self.auth["delay"])
        self.browser.login(self.auth["email"], self.auth["pswd"], self.auth["delay"])
        time.sleep(self.auth["delay"]+5)

        buybutton_xpath = '/html/body/div[5]/div/div[2]/form/div/div/div/div[2]/div/div[1]/div/div[1]/div/span/span/input'
        self.browser.find_and_click(buybutton_xpath)
        print("ORDINE EFFETTUATO CON SUCCESSO!")
        time.sleep(10)

    def run(self):
        self.check_product()
    
    def __str__(self):
        string = "Email: {}\nPassword: {}".format(self.auth["email"], self.auth["pswd"])
        for p in self.products:
            string += "\n" + str(p)
        return string
