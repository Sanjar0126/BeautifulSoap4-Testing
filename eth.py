from bs4 import BeautifulSoup as bs
import requests
import logging
import re
logging.basicConfig(level=logging.INFO, format='%(message)s')

BASE_URL = "https://etherscan.io/block/"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

#### CHANGE THIS ####
# INITIAL = 15041812
INITIAL = 15560704
ITR_RANGE = 24
#### CHANGE THIS ####

if __name__ == '__main__':
    output = ""
    
    for index in range(ITR_RANGE):
        block_id = INITIAL + index
        
        link = f"{BASE_URL}{block_id}"
        
        logging.info(f"{index+1} - {link}")
        
        r = requests.get(link, headers=HEADERS)
        soup = bs(r.content, 'lxml')
        
        main_box = soup.find('div', class_='card-body')
        
        box_list = main_box.find_all('div', class_='row align-items-center')
                
        block_height = block_id
        date = box_list[1].find('div', class_='col-md-9').get_text()
        timestamp = re.search('\((.+?)\)', date).group(1)
        transactions = main_box.find('div', {'id': 'ContentPlaceHolder1_div_tx_fieldvalue'}).get_text().strip()
        mined_by = box_list[3].find('div', class_='col-md-9').get_text().strip()
        block_reward = box_list[4].find('div', class_='col-md-9').get_text().strip().split('(', 1)[0]
        uncles_reward = box_list[5].find('div', class_='col-md-9').get_text().strip().split('(', 1)[0]
        difficulty = box_list[6].find('div', class_='col-md-9').get_text().strip().split('(', 1)[0]
        total_difficulty = box_list[7].find('div', class_='col-md-9').get_text().strip().split('(', 1)[0]
        size = box_list[8].find('div', class_='col-md-9').get_text().strip().split('(', 1)[0]
        gas_used = box_list[9].find('div', class_='col-md-9').get_text().strip()
        gas_limit = box_list[10].find('div', class_='col-md-9').get_text().strip().split('(', 1)[0]
        extra_data = box_list[13].find('div', class_='col-md-9').get_text().strip()
        hash = box_list[15].find('div', class_='col-md-9').get_text().strip()
        parent_hash = box_list[16].find('div', class_='col-md-9').get_text().strip()
        sha3_uncles = box_list[17].find('div', class_='col-md-9').get_text().strip()
        state_root = box_list[18].find('div', class_='col-md-9').get_text().strip()
        nonce = box_list[19].find('div', class_='col-md-9').get_text().strip()
        
        output = output + f"\n\t{index+1}. [A] BLOCK #{block_id}\n(i) Block height: {block_height}\n(ii) Timestamp: {timestamp}\n" + \
            f"(iii) Transactions: {transactions}\n(iv) Mined By: {mined_by}\n(v) Block Reward: {block_reward}\n(vi) Uncles reward: {uncles_reward}\n" + \
            f"(vii) Difficulty: {difficulty}\n(viii) Total Difficulty: {total_difficulty}\n(ix) Size: {size}\n(x) Gas Used: {gas_used}\n" + \
            f"(xi) Gas Limit: {gas_limit}\n(xii) Extra Data: {extra_data}\n(xiii) Hash: {hash}\n(xiv) Parent Hash: {parent_hash}\n" + \
            f"(xv) Sha3Uncles: {sha3_uncles}\n(xvi) StateRoot: {state_root}\n(xvii) Nonce: {nonce}\n" + \
            f"[B] {link}\n[C] \n"
        
    with open("output_eth", "w") as text_file:
        text_file.write(output)
