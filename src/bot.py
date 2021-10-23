class Product:
    def __init__(self, productsList) -> None:
        self.ID = productsList["ID"]
        self.quantity = productsList["quantity"]
        self.price = (float) (productsList["price"])
        self.errorPrice = (float) (productsList["errorPrice"])

    def __str__(self):
        minPrice = self.price - self.errorPrice
        maxPrice = self.price + self.errorPrice
        str = "ID: {} | ".format(self.ID) +\
               "quantity: {} | ".format(self.quantity) +\
               "price: {} - {}".format(minPrice, maxPrice)
        return str

class AmazonBot:
    def __init__(self, email: str, pswd: str) -> None:
        self.auth = {
            "email": email,
            "pswd": pswd,
        }
        self.products = []

    def addProduct(self, product: Product):
        self.products.append(product)

    def checkProducts():
        pass

    def buyProduct(product: Product):
        pass
    
    def __str__(self):
        str = "Email: {}\nPassword: {}".format(self.auth["email"], self.auth["pswd"])
        for p in self.products:
            str += "\n" + str(p)
        return str

class WebBrowser:
    def __init__(self) -> None:
        self.url = ""
        