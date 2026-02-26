import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

BASE_URL = "https://dota2.fandom.com"
START_URL = "https://dota2.fandom.com/wiki/Category:Unit_icons"

SAVE_DIR = "icons"
os.makedirs(SAVE_DIR, exist_ok=True)

def save_square_image(url, filename):
    r = requests.get(url, stream=True)
    r.raise_for_status()

    img = Image.open(BytesIO(r.content)).convert("RGBA")

    w, h = img.size
    if w != h:
        # crop to square (center crop)
        side = min(w, h)
        left = (w - side) // 2
        top = (h - side) // 2
        right = left + side
        bottom = top + side
        img = img.crop((left, top, right, bottom))

    filepath = os.path.join(SAVE_DIR, filename.replace(" ", "_"))
    img.save(filepath, format="PNG")
    print(f"Saved {filepath} ({img.size[0]}x{img.size[1]})")

def download_images_from_page(url):
    print(f"Fetching {url}")
    resp = requests.get(url)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    for img in soup.select("div.thumb img"):
        parent_a = img.find_parent("a")
        if not parent_a:
            continue
        href = parent_a.get("href")
        if not href or not href.startswith("https"):
            continue

        filename = img.get("data-image-name")
        if not filename:
            filename = href.split("/revision/")[0].split("/")[-1]

        filepath = os.path.join(SAVE_DIR, filename.replace(" ", "_"))
        if os.path.exists(filepath):
            continue  # already downloaded

        try:
            save_square_image(href, filename)
        except Exception as e:
            print(f"❌ Failed {filename}: {e}")

    # follow next page
    next_link = soup.select_one("a[title='Category:Unit icons'][href*='filefrom=']")
    if next_link:
        next_url = BASE_URL + next_link["href"]
        download_images_from_page(next_url)

# start
download_images_from_page(START_URL)
