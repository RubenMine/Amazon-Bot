class Product:

    def __init__(self, dictProduct) -> None:
        self.ID = dictProduct["ID"]
        self.quantity = dictProduct["quantity"]
        self.price = (float)(dictProduct["price"])
        self.errorPrice = (float)(dictProduct["errorPrice"])

    def __str__(self):
        minPrice = self.price - self.errorPrice
        maxPrice = self.price + self.errorPrice
        txt = "ID: {} | ".format(self.ID) +\
               "quantity: {} | ".format(self.quantity) +\
               "price: {} - {}".format(minPrice, maxPrice)
        return txt


class AmazonBot:
    
    def __init__(self, email, pswd) -> None:
        self.auth = {
            "email":email,
            "pswd":pswd,
        }
        self.products = []

    def addProduct(self, product):
        self.products.append(product)

    def checkProducts():
        pass

    def buyProduct(product:Product):
        pass
    
    def __str__(self):
        txt = "Email: {}\nPassword: {}".format(self.auth["email"], self.auth["pswd"])
        for p in self.products:
            txt += "\n" + str(p)
        return txt


class WebBrowser:

    def __init__(self) -> None:
        self.url = ""
        