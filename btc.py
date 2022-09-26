from bs4 import BeautifulSoup as bs
import requests
import json
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

BASE_URL = "https://www.blockchain.com/explorer/blocks/btc/"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

INITIAL = 754649
ITR_RANGE = 48

if __name__ == '__main__':
    output = ""
    
    for index in range(ITR_RANGE):
        block_id = INITIAL + index
        
        link = f"{BASE_URL}{block_id}"
        
        logging.info(f"{index} - {link}")
        
        r = requests.get(link, headers=HEADERS)
        soup = bs(r.content, 'lxml')
        
        main_box = soup.find('div', class_="sc-e7f1e30c-0 gpa-dQC")
        
        box = main_box.find_all('div', class_='sc-e7f1e30c-2 geZHKv')
        
        block_hash = box[0].find('div', class_="sc-e1190e8f-2 dctWDI").get('data-tool-tip')
        confirmations = box[1].find('div', class_='sc-e1190e8f-2 eWPOdW').get_text().strip()
        timestamp = box[31].find('div', class_='sc-e1190e8f-2 eWPOdW').get_text().strip()
        height = box[32].find('div', class_='sc-e1190e8f-2 eWPOdW').get_text().strip()
        miner = box[34].find('div', class_='sc-e1190e8f-2 eWPOdW').get_text().strip()
        num_of_transactions = box[11].find('div', class_='sc-e1190e8f-2 eWPOdW').get_text().strip()
        difficulty = box[24].find('div', class_='sc-e1190e8f-2 eWPOdW').get_text().strip()
        merkle_root = box[23].find('div', class_='sc-e1190e8f-2 dctWDI').get('data-tool-tip').strip()
        version = box[22].find('div', class_='sc-e1190e8f-2 eWPOdW').get_text().strip()
        bits = box[26].find('div', class_='sc-e1190e8f-2 eWPOdW').get_text().strip()
        weight = box[27].find('div', class_='sc-e1190e8f-2 eWPOdW').get_text().strip()
        size = box[21].find('div', class_='sc-e1190e8f-2 eWPOdW').get_text().strip()
        nonce = box[25].find('div', class_='sc-e1190e8f-2 eWPOdW').get_text().strip()
        transaction_volume = box[4].find('div', class_='sc-e1190e8f-2 eWPOdW').get_text().strip()
        block_reward = box[30].find('div', class_='sc-e1190e8f-2 eWPOdW').get_text().strip()
        fee_reward = box[15].find('div', class_='sc-e1190e8f-2 eWPOdW').get_text().strip()
        
        output = output + f"\n[A] BLOCK #{block_id}\n(i) Hash (Block Hash): {block_hash}\n(ii) Confirmations: {confirmations}\n" + \
            f"(iii) Timestamp: {timestamp}\n(iv) Height: {height}\n(v) Miner: {miner}\n(vi) Number of transactions: {num_of_transactions}\n" + \
            f"(vii) Difficulty: {difficulty}\n(viii) Merkle root: {merkle_root}\n(ix) Version: {version}\n(x) Bits: {bits}\n" + \
            f"(xi) Weight: {weight}\n(xii) Size: {size}\n(xiii) Nonce: {nonce}\n(xiv) Transaction volume: {transaction_volume}\n" + \
            f"(xv) Block Reward: {block_reward}\n(xvi) Fee Reward: {fee_reward}\n(xvii)Describe clearly the details of a single transaction in this block of Bitcoin Blockchain.\n" + \
            f"[B] {link}\n[C] \n"
        
    with open("output", "w") as text_file:
        text_file.write(output)
