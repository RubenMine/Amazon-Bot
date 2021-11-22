from typing import overload
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import enum
import time

class Status(enum.Enum):
    unavailable = 0
    available = 1
    bought = 2

class Product:
    def __init__(self, dictProduct) -> None:
        self.ASIN       = dictProduct["ASIN"]
        self.quantity   = dictProduct["quantity"]
        self.price      = (float) (dictProduct["price"])
        self.errorPrice = (int) (dictProduct["errorPrice"])
        self.status     = Status.unavailable

    def __str__(self) -> str:
        minimum_price = self.price - self.errorPrice
        maximum_price = self.price + self.errorPrice
        string = "ASIN: {} | ".format(self.ASIN) +\
                 "Quantity: {} | ".format(self.quantity) +\
                 "Price: {} - {}".format(minimum_price, maximum_price)
        return string

class WebBrowser:
    def __init__(self, url: str, delay: int) -> None:
        self.url          = url                     # Amazon url selected by the user
        self.wait_seconds = delay                   # Delay to wait before searching for a field (in seconds)
        self.browser      = webdriver.Firefox()     # Browser instance
    
    def login(self, email: str, pswd: str) -> None:
        email_field    = None
        password_field = None
        login_xpath    = '//*[@id="nav-link-accountList"]'  # Login button xpath to search in the webpage
        email_xpath    = '//*[@ID="ap_email"]'              # Email xpath to search in the webpage
        password_xpath = '//*[@ID="ap_password"]'           # Password xpath to search in the webpage
        self.browser.get(self.url)
        # Click login button
        self.click_element(login_xpath)
        # Search for the email input field
        try:
            email_field = WebDriverWait(self.browser, self.wait_seconds).until(
            EC.presence_of_element_located((By.XPATH, email_xpath)))
        except:
            print("Can't find field {}".format(email_xpath))
            self.browser.quit()
        else:
            email_field.send_keys(email, Keys.ENTER)
        # Search for the password input field
        try:
            password_field = WebDriverWait(self.browser, self.wait_seconds).until(
            EC.presence_of_element_located((By.XPATH, password_xpath)))
        except:
            print("Can't find field {}".format(password_xpath))
            self.browser.quit()
        else:
            password_field.send_keys(pswd, Keys.ENTER)
        # Wait before searching a product, necessary for the login to take action
        time.sleep(self.wait_seconds)

    def search_product(self, ASIN: str) -> None:
            product_page = self.url + 'dp/' + ASIN  # Product page for the specified ASIN
            self.browser.get(product_page)
        
    def is_available(self, price: float, errorPrice: int) -> bool:
        buybutton_xpath = '//*[@id="buy-now-button"]'
        #buyprice_xpath  = '/html/body/div[2]/div[2]/div[6]/div[3]/div[1]/div[4]/div/div/div/form/div/div/div/div/div[2]/div/div/span/span[1]'
        buyprice_xpath  = '//*[@id="corePrice_feature_div"]/div/span/span[2]'
        maximum_price   = price + errorPrice
        minimum_price   = price - errorPrice
        try:
            print('[PRICE] Min price {}, Max price {}'.format(minimum_price, maximum_price))
            buybutton_field = WebDriverWait(self.browser, self.wait_seconds).until(
            EC.presence_of_element_located((By.XPATH, buybutton_xpath)))
            print('[OK] Product is available')
            # non funziona
            buyprice_field = WebDriverWait(self.browser, self.wait_seconds).until(
            EC.presence_of_element_located((By.XPATH, buyprice_xpath)))
            print('[OK] Price found')
        except:
            print("[ERROR] Product not available or price not found")
            return False
        else:
            buyprice = (float) (buyprice_field.text[:-1].replace(",", "."))
            if buyprice < maximum_price and buyprice > minimum_price:
                return True
            else:
                return False
    
    def click_element(self, xpath: str, delay: int = None) -> None:
        if delay is not None:
            element = WebDriverWait(self.browser, delay).until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
            self.browser.execute_script("arguments[0].click();", element)
        else:
            element = WebDriverWait(self.browser, self.wait_seconds).until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
            self.browser.execute_script("arguments[0].click();", element)

    def refresh(self):
        self.browser.refresh()
                   
class AmazonBot:
    def __init__(self, url: str, email: str, pswd: str, delay: int) -> None:
        self.auth = {
            "email": email,
            "pswd": pswd,
        }
        self.browser  = WebBrowser(url, delay)
        self.products = []

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def check_product(self) -> None:
        while(len(self.products) >= 1):
            for product in self.products:
                if product.status != Status.bought: 
                    self.browser.search_product(product.ASIN)
                
                if product.status == Status.unavailable:
                    product.status = Status.available if self.browser.is_available(product.price, product.errorPrice) else Status.unavailable

                if product.status == Status.bought:
                    self.products.remove(product)    
                if product.status == Status.available:
                    print('Buying {}'.format(product.ASIN))
                    self.buy_product(product)
                print(product.ASIN, ' ', product.status)

    def buy_product(self, product: Product) -> None:
        # TODO:
        # - Controllare il numero di prodotti disponibili
        #   se il numero supera la quantità selezionata nei
        #   config acquista la quantità selezionata, altrimenti
        #   acquista il numero di prodotti disponibili.
        # - Controllare se l'acquisto è andato a buon fine prima
        #   di assegnare lo status "bought" ad un prodotto.
        quantity     = product.quantity
        add_to_cart  = '//*[@id="add-to-cart-button"]'
        go_to_cart   = '//*[@id="hlb-ptc-btn-native"]'
        confirmation = '/html/body/div[5]/div/div[2]/form/div/div/div/div[2]/div[1]/div[1]/div/div[1]/div/span/span/input'
        try:
            self.browser.click_element(add_to_cart)
            time.sleep(2) #
            print("[OK] Add to cart")
            self.browser.click_element(go_to_cart)
            print("[OK] Go to cart")
            time.sleep(2) #
            self.browser.click_element(confirmation)
            time.sleep(2) #
            print("[OK] Confirmation")
        except:
            print("[ERROR] Can't buy {}".format(product.ASIN))
        else:
            print("[OK] {}: ({}x) successfully bought.".format(product.ASIN, quantity))
            product.status = Status.bought

    def run(self) -> None:
        self.browser.login(self.auth["email"], self.auth["pswd"])
        self.check_product()
    
    def __str__(self) -> str:
        string = "Email: {}\nPassword: {}".format(self.auth["email"], self.auth["pswd"])
        for p in self.products:
            string += "\n" + str(p)
        return string
