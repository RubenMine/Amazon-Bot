from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def main():
    browser = webdriver.Firefox()
    browser.get("https://google.com/ncr")



if __name__ == "__main__":
    main()