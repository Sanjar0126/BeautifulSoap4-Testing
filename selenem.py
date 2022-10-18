import time
from unicodedata import category
from bs4 import BeautifulSoup as bs
import requests
from selenium.webdriver.common.by import By
from selenium import webdriver

BASE_URL = "https://portal.tafs.com/"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

firefox_profile = webdriver.FirefoxOptions()
firefox_profile.set_preference('permissions.default.image', 2)
firefox_profile.accept_insecure_certs = True

browser = webdriver.Firefox(options=firefox_profile)

browser.get(BASE_URL)

username = browser.find_element(by=By.ID, value="txt_username")
password = browser.find_element(by=By.ID, value="txt_password")

username.send_keys("200970768")
password.send_keys("0768PUNT")

browser.find_element(value="btn_login", by=By.ID).click()
