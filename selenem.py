from unicodedata import category
from dotenv import load_dotenv
import os
from selenium.webdriver.common.by import By
from selenium import webdriver

load_dotenv()

BASE_URL = os.getenv('TAFS_URL')
USERNAME = os.getenv('TAFS_USER')
PASSWORD = os.getenv('TAFS_PASS')

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

username.send_keys(USERNAME)
password.send_keys(PASSWORD)

browser.find_element(value="btn_login", by=By.ID).click()
