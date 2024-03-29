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

categories = ['doglyad-za-oblichchyam/', 'kosmetika-dlya-volossya/', 'kosmetika-dlya-makiyazhu/', 'tilo/', 'bioaktivnye-dobavki-uk/',]

product_links = []

for category in categories:
    if category == 'doglyad-za-oblichchyam/':
        page_range = 29
    elif category == 'kosmetika-dlya-volossya/':
        page_range = 5
    elif category == 'kosmetika-dlya-makiyazhu/':
        page_range = 3
    elif category == 'tilo/':
        page_range = 4
    elif category == 'bioaktivnye-dobavki-uk/':
        page_range = 2
    for x in range(1,page_range): 
        r = requests.get(base_url+category+f'page-{x}/', headers=headers)
        soup = bs(r.content, 'lxml')

        main_grid = soup.find('div', class_="ty-pagination-container cm-pagination-container")
        product_list = main_grid.find_all('div', class_='ty-grid-list__image')
        
        for item in product_list:
            for link in item.find_all('a', href=True):
                product_links.append(link["href"])
        logging.info(len(product_links))
            
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
        
    body = description_title
    body.extend(description)
    
    manual_title = soup.find('div',class_='tab-list-title ab-spt-title', id='product_tab_12')
    use_manual = soup.find('div',class_='ty-wysiwyg-content content-product_tab_12', id='content_product_tab_12')
    
    if use_manual == None:
        use_manual = manual_title = ""
        
    body.extend(manual_title)
    body.extend(use_manual)
        
    property_title = soup.find('div', class_='tab-list-title ab-spt-title', id='product_tab_13')
    properties = soup.find('div', class_='ty-wysiwyg-content content-product_tab_13', id='content_product_tab_13')
    
    if properties is None:
        properties = property_title = ""

    body.extend(property_title)
    body.extend(properties)
    
    
    thumb = []
    
    img_container = soup.find('div', class_='ab_vg-images-wrapper clearfix')
    for link in img_container.find_all('a', href=True):
        if 'http' in link['href']:
            thumb.append(link['href'])

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
        'description': str(body).replace("\"", "'"),
        'thumb': thumb,
        'features': features
    }
    
    logging.info(str(number) + ' - ' + title)
    number += 1
    products.append(product)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=4)