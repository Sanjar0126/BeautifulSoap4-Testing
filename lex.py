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

def main():
    r = requests.get(link, headers=HEADERS)
    soup = bs(r.content, 'lxml')

    main_box = soup.find('div', class_="docBody__container")

    act_title = main_box.find('div', class_='ACT_TITLE').find('a').get_text().strip()

    div_cont = main_box.find('div', id='divCont')
    allowed_classes = {"TEXT_HEADER_DEFAULT", "CLAUSE_DEFAULT", "ACT_TEXT"}

    div_list = div_cont.find_all('div', class_=list(allowed_classes))

    header_list = list()
    text_header = ""
    clause_header = ""
    content = ""
    is_list = False

    for idx, div in enumerate(div_list):
        if div.has_attr('class'):
            if 'TEXT_HEADER_DEFAULT' in div['class']:
                text_header = div.find('a').get_text().strip()
                prev_is_list_end = False
            elif 'CLAUSE_DEFAULT' in div['class']:
                clause_header = div.find('a').get_text().strip()
                content = ""
                prev_is_list_end = False
            elif 'ACT_TEXT' in div['class']:
                topic_text =  f'{text_header}. {clause_header}.'
                act_text =  f'{div.find("a").get_text().strip()}'
                
                if 'возможность в случаях, установленных настоящим Кодексом или иным законом, предусматривать в трудовом договоре дополнительные основания его прекращения.' in act_text:
                    print('here')
                
                if check_if_list(act_text):
                    content = content + " " + act_text
                    is_list = True
                    continue
                if check_if_list_head(act_text):
                    content = act_text
                    is_list = True
                    continue
                
                if is_list:
                    content = content + " " + act_text
                    is_list = False
                elif not is_list:
                    content = content + " " + act_text
            
                next_act_condition = idx + 1 < len(div_list) and \
                    'ACT_TEXT' in div_list[idx + 1]['class'] and check_if_list_head(f'{div_list[idx + 1].find("a").get_text().strip()}')
                next_clause_condition = idx + 1 < len(div_list) and 'CLAUSE_DEFAULT' in div_list[idx + 1]['class']
                next_header_condition = idx + 1 < len(div_list) and 'TEXT_HEADER_DEFAULT' in div_list[idx + 1]['class']
                curr_prev_act_condition = 'ACT_TEXT' in div_list[idx - 1]['class'] and \
                    check_if_list(f'{div_list[idx - 1].find("a").get_text().strip()}') and not check_if_list(act_text) and not check_if_list_head(act_text)
                
                if next_header_condition or next_clause_condition or next_act_condition or curr_prev_act_condition:
                    header_list.append({
                        'topic': topic_text,
                        'content': content.strip()
                    }) 
                    content = ""
                

    header_list.append({
                    'topic': topic_text,
                    'content': content.strip()
                }) 
        
    # file_count = len(glob.glob1(".","lex_*"))
    file_count = 1
    
    final_list = {
        "Header title": act_title,
        "Contents": header_list
    }

    print(f'saving lex_{file_count}.json')

    with open(f'lex_{file_count}.json', 'w', encoding='utf-8') as f:
        json.dump(final_list, f, ensure_ascii=False, indent=4)

def check_if_list_head(text):
    if text[-1] == ":":
        return True
    return False

def check_if_list(text):
    if text[-1] == ";":
        return True
    return False

if __name__ == "__main__":
    main()