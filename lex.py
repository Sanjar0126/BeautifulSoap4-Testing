import glob
import json
import requests
from bs4 import BeautifulSoup as bs

remove = "Предложения по документу"

link = 'https://lex.uz/ru/docs/6257291'
# link = 'https://lex.uz/en/docs/6130752' # small pp

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

r = requests.get(link, headers=HEADERS)
soup = bs(r.content, 'lxml')

main_box = soup.find('div', class_="docBody__container")

act_title = main_box.find('div', class_='ACT_TITLE').find('a').get_text().strip()

div_cont = main_box.find('div', id='divCont')

i = 0
header_list = list()
prev = ""
text_header = ""
clause_header = ""
content = ""
is_list = False

for div in div_cont.find_all('div'):
    if div.has_attr('class'):
        if 'TEXT_HEADER_DEFAULT' in div['class']:
            text_header = div.find('a').get_text().strip()
        elif 'CLAUSE_DEFAULT' in div['class']:
            clause_header = div.find('a').get_text().strip()
            content = ""
        elif 'ACT_TEXT' in div['class']:
            topic_text =  f'{text_header}. {clause_header}.'
            act_text =  f'{div.find("a").get_text().strip()}'
            
            if act_text[-1] == ";":
                content = content + " " + act_text
                is_list = True
                continue
            if act_text[-1] == ":":
                content = act_text
                is_list = True
                continue
            
            if is_list:
                content = content + " " + act_text
                is_list = False
            else:
                content = content + " " + act_text
            
            header_list.append({
                'topic': topic_text,
                'content': content.strip()
            }) 
    
# file_count = len(glob.glob1(".","lex_*"))
file_count = 1

print(f'saving lex_{file_count}.json')

with open(f'lex_{file_count}.json', 'w', encoding='utf-8') as f:
    json.dump(header_list, f, ensure_ascii=False, indent=4)
