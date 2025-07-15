import requests
from bs4 import BeautifulSoup
import json
import os
import urllib.parse

def clean_filename(filename):
    name = os.path.basename(filename)
    name = urllib.parse.unquote(name)
    name = name.replace('_', ' ').replace('.pdf', '').strip().title()
    return name

def scrape_beu_notices():
    url = "https://beu-bih.ac.in/notification"
    base_url = "https://beu-bih.ac.in/"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    notices = []

    for link in soup.find_all("a", href=True):
        href = link['href']
        if ".pdf" in href.lower():
            title = clean_filename(href)
            full_url = href if href.startswith("http") else base_url + href.lstrip('/')
            notices.append({
                "title": title,
                "url": full_url
            })

    with open("notices.json", "w", encoding='utf-8') as f:
        json.dump(notices, f, indent=2, ensure_ascii=False)

    print(f"✅ Scraped {len(notices)} notices and saved to notices.json")

if __name__ == "__main__":
    scrape_beu_notices()
