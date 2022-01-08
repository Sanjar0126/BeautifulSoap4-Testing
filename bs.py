from bs4 import BeautifulSoup as bs
import requests
import json
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

number = 1

base_url = 'https://facebar.com.ua/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

categories = ['osnovnoy-uhod/', 'volosy/', 'makiyazh/', 'telo/', 'bioaktivnye-dobavki/',]

product_links = ['https://facebar.com.ua/osnovnoy-uhod/drzonskin-penka-dlya-zhirnoy-problemnoy-i-kombinirovannoy-kozhi-n-zon-face-wash/']

# for category in categories:
#     if category == 'osnovnoy-uhod/':
#         page_range = 29
#     elif category == 'volosy/':
#         page_range = 5
#     elif category == 'makiyazh/':
#         page_range = 3
#     elif category == 'telo/':
#         page_range = 4
#     elif category == 'bioaktivnye-dobavki/':
#         page_range = 2
#     for x in range(1,page_range): 
#         r = requests.get(base_url+category+f'page-{x}/', headers=headers)
#         soup = bs(r.content, 'lxml')

#         main_grid = soup.find('div', class_="ty-pagination-container cm-pagination-container")
#         product_list = main_grid.find_all('div', class_='ty-grid-list__image')

        
#         for item in product_list:
#             for link in item.find_all('a', href=True):
#                 product_links.append(link["href"])
#         logging.info(len(product_links))
            
products = []

for link in product_links:
    r = requests.get(link, headers=headers)
    soup = bs(r.content, 'lxml')

    try:
        title = soup.find('h1', class_='ty-product-block-title').text.strip()
    except:
        title = ""

    try:
        price = soup.find('span', class_='ty-price-num').text.strip()
    except:
        price = ""
    
    try:
        block_description = soup.find('div', class_='ty-product-block__description').text.strip()
    except:
        block_description = ""
    
    description_title = soup.find('div', class_='tab-list-title ab-spt-title', id='description')
    description = soup.find('div', class_='ty-wysiwyg-content content-description', id='content_description')

    if description == None:
        description = description_title = ""
    
    manual_title = soup.find('div',class_='tab-list-title ab-spt-title', id='product_tab_12')
    use_manual = soup.find('div',class_='ty-wysiwyg-content content-product_tab_12', id='content_product_tab_12')
    
    if use_manual == None:
        use_manual = manual_title = ""
        
    property_title = soup.find('div', class_='tab-list-title ab-spt-title', id='product_tab_13')
    properties = soup.find('div', class_='ty-wysiwyg-content content-product_tab_13', id='content_product_tab_13')

    if properties is None:
        properties = property_title = ""

    try:
        thumb = soup.find('a', class_='cm-image-previewer cm-previewer ty-previewer', href=True)
    except:
        thumb = ""
        
    # print(thumb)

    features_soup = soup.find_all('div', class_='ty-product-feature')
    features = []

    for item in features_soup:
        try:
            label = item.find('div', class_='ty-product-feature__label').text[:-1].strip()
        except:
            label = ""
        
        try:
            value = item.find('div', class_='ty-product-feature__value').text.strip()
        except:
            value = ""
        
        features.append({'label': label, 'value': value})

    product = {
        'title': title,
        'price': price,
        'block_description': block_description,
        'description': description,
        'use_manual': use_manual,
        'properties': properties,
        'thumb': thumb,
        'features': features
    }
    logging.info(str(number) + ' - ' + title)
    number += 1
    products.append(product)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=4)