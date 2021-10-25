from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import enum

class Status(enum.Enum):
    unavailable = 0
    available = 1
    bought = 2


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
    
    def connectAndLogin(self, email: str, pswd: str, delay: int):
        self.browser.get(self.url)
        email_field    = None
        password_field = None
        email_xpath    = '//*[@id="ap_email"]'      # Email xpath to search in the webpage
        password_xpath = '//*[@id="ap_password"]'   # Password xpath to search in the webpage
        wait_seconds   = delay                      # Delay to wait before searching for a field (in seconds)
        # Search and click the login button
        login_button = self.browser.find_element(By.ID, "nav-link-accountList")
        login_button.click()
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
            product_page = 'http://www.amazon.com/exec/obidos/ASIN/' + ASIN  # Product page for the specified ASIN
            ASIN_regex = r'^B[A-Z 0-9]{9}'
            pattern = re.compile(ASIN_regex)
            # Check if provided ASIN matches a basic regex pattern
            if pattern.match(ASIN):
                self.browser.get(product_page)
                # Check if the product exist by checking the current page title
                if self.browser.title == 'Page Not Found':
                    self.browser.quit()
                    print("The provided ASIN ({}) does not exist".format(ASIN))
            else:
                self.browser.quit()
                print("The provided ASIN is not valid")
        
    def is_available(self) -> bool:
        buybutton_xpath = '//*[@id="buy-now-button"]'
        buybutton_field = None
        try:
            buybutton_field = self.browser.find_element_by_xpath(buybutton_xpath)
        except:
            return False
        else:
            return True
            
            

class AmazonBot:
    def __init__(self, url: str, email: str, pswd: str, delay: int) -> None:
        self.auth = {
            "email": email,
            "pswd": pswd,
            "delay": delay
        }
        self.browser = WebBrowser(url)
        self.products = []

    def addProduct(self, product: Product):
        self.products.append(product)

    def checkProducts(self):
        while(len(self.products) >= 1):
            for product in self.products:
                if product.status != Status.bought: 
                    self.browser.search_product(product.ID)

                if product.status == Status.unavailable:
                    product.status = Status.available if self.browser.is_available() else Status.unavailable
                if product.status == Status.available:
                    self.buyProduct(product)
                elif product.status == Status.bought:
                    self.products.remove(product)

    def buyProduct(product: Product):
        pass

    def run(self):
        self.browser.connectAndLogin(self.auth["email"], self.auth["pswd"], self.auth["delay"])
        self.browser.search_product('B001F9RA94')
        print(self.browser.is_available())
    
    def __str__(self):
        string = "Email: {}\nPassword: {}".format(self.auth["email"], self.auth["pswd"])
        for p in self.products:
            string += "\n" + str(p)
        return string
