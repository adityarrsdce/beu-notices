import requests
from bs4 import BeautifulSoup
import json

def scrape_beu_notices():
    url = "https://beu-bih.ac.in/notification"
    base_url = "https://beu-bih.ac.in"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    notices = []

    # Target table rows
    rows = soup.select("table tbody tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 3:
            date = cols[1].get_text(strip=True)
            title = cols[2].get_text(strip=True)
            link_tag = cols[3].find("a")
            if link_tag and link_tag.get("href"):
                href = link_tag["href"]
                full_url = href if href.startswith("http") else f"{base_url}/{href.lstrip('/')}"
                notices.append({
                    "date": date,
                    "title": title,
                    "url": full_url
                })

    with open("notices.json", "w", encoding="utf-8") as f:
        json.dump(notices, f, indent=2, ensure_ascii=False)

    print(f"✅ Scraped {len(notices)} notices and saved to notices.json")

if __name__ == "__main__":
    scrape_beu_notices()
