from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
            print("Can't find field {}", email_xpath)
            self.browser.quit()
        else:
            email_field.send_keys(email, Keys.ENTER)
        # Search for the password input field    
        try:
            password_field = WebDriverWait(self.browser, wait_seconds).until(
            EC.presence_of_element_located((By.XPATH, password_xpath)))
        except:
            print("Can't find field {}", password_xpath)
            self.browser.quit()
        else:
            password_field.send_keys(pswd, Keys.ENTER)

    def search_product(self, ASIN: str, delay: int):
            searchbar           = None
            product             = None
            searchbar_xpath     = '//*[@id="twotabsearchtextbox"]'
            product_xpath       = '/html/body/div[1]/div[2]/div[1]/div[1]/div/span[3]/div[2]/div[1]/div/div/div/div/div[3]/div[1]/h2/a'
            wait_seconds        = delay
            searchbar = WebDriverWait(self.browser, wait_seconds).until(
                        EC.presence_of_element_located((By.XPATH, searchbar_xpath)))
            searchbar.send_keys(ASIN, Keys.ENTER)
            try:
                product = WebDriverWait(self.browser, wait_seconds).until(
                EC.presence_of_element_located((By.XPATH, product_xpath)))
            except:
                print("Can't find any product with the ASIN: {}", ASIN)
                self.browser.quit()
            else:
                product.click()


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

    def checkProducts():
        pass

    def buyProduct(product: Product):
        pass

    def run(self):
        self.browser.connectAndLogin(self.auth["email"], self.auth["pswd"], self.auth["delay"])
        self.browser.search_product("B071JM699B", self.auth["delay"])

    
    def __str__(self):
        string = "Email: {}\nPassword: {}".format(self.auth["email"], self.auth["pswd"])
        for p in self.products:
            string += "\n" + str(p)
        return string