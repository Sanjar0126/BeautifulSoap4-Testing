from email.mime import image
import json
import time
from unicodedata import category
from bs4 import BeautifulSoup as bs
import requests
from selenium.webdriver.common.by import By
from selenium import webdriver

BASE_URL = "https://www.macrocenter.com.tr"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

WAIT_TIME = 3

def wait():
    print("waiting 3 sec...")
    time.sleep(WAIT_TIME)


def get_site_categories(cat_element):
    categories = list()
    cat_soap = bs(cat_element, 'lxml')
        
    cat_list = cat_soap.find_all("mc-nav-tree-large-item")
    
    for cat in cat_list:
        subcat_list = cat.find_all("fe-category-flyout-simple")
        
        for subcat in subcat_list:
            cat_title_list = subcat.find_all("a")
            
            for category_link in cat_title_list:
                categories.append(category_link['href'])
    
    return categories

def get_site_products(list_element):
    links = list()
    list_soap = bs(list_element, 'lxml')
    
    product_list = list_soap.find_all("fe-product-card")
    
    for prod in product_list:
        prod_link = prod.find("fe-product-image").find("a", href=True)
        links.append(prod_link['href'])
    
    return links

def scroll_down(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(3)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def get_product_categories(html_soap):
    sub_categories = list()
    main_category = None

    category_html = html_soap.find_all("li", class_="breadcrumbs__item ng-star-inserted")
    for cat_index, category in enumerate(category_html):
        if cat_index == 0:
            main_category = category.text.strip()
        
        sub_categories.append({
            "title": category.text.strip(),
            "tier": cat_index
        })
    
    return sub_categories, main_category

def get_images(html_soap):
    images = list()
    
    images_html = html_soap.find_all("figure")
    
    for count, image_html in enumerate(images_html):
        images.append({
            "link": image_html.next['src'],
            "order": count
        })
    
    return images

def get_product_details(inner_html):
    output = dict()
    
    html_soap = bs(inner_html, 'lxml')
    
    sub_categories, main_category = get_product_categories(html_soap)
    
    output['title'] = html_soap.find('fe-product-name').text.strip()
    output['brand'] = html_soap.find('fe-product-brand').text.strip()
    output['price'] = html_soap.find('span', class_="amount").text.strip()
    output['main_category'] = main_category
    output['sub_categories'] = sub_categories
    output['images'] = get_images(html_soap)
    
    print(output['title'])
    
    return output
    

if __name__ == '__main__':
    errors = []
    
    firefox_profile = webdriver.FirefoxOptions()
    firefox_profile.set_preference('permissions.default.image', 2)

    browser = webdriver.Firefox(options=firefox_profile)
        
    browser.get(BASE_URL)
    wait()
    
    cat_element = browser.find_element(by=By.TAG_NAME, value="mc-nav-tree-large").get_attribute('innerHTML')
    categories = get_site_categories(cat_element)
    
    product_links = []
    for category_link in categories:
        try:
            browser.get(f'{BASE_URL}{category_link}')
            wait()
            
            scroll_down(driver=browser)
            
            product_list_field = browser.find_element(by=By.TAG_NAME, value="fe-product-list").get_attribute('innerHTML')
                
            product_links.append(get_site_products(product_list_field))
        except Exception as e:
            errors.append({
                "error": e,
                "msg": "error while getting product links"
            })
            continue
            
    product_details = []
    
    for product_link in product_links:
        try:
            browser.get(f'{BASE_URL}{product_link}')
            wait()
            
            product_details_field = browser.find_element(by=By.TAG_NAME, value="mc-product-detail-page").get_attribute('innerHTML')
            
            product_details.append(get_product_details(product_details_field))
        except Exception as e:
            errors.append({
                "error": e,
                "msg": "error while getting product links"
            })
            continue
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(product_details, f, ensure_ascii=False, indent=4)
    
    if len(errors) != 0:
        with open('errors.json', 'w', encoding='utf-8') as f:
            json.dump(errors, f, ensure_ascii=False, indent=4)
    
    browser.quit()
