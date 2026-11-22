import csv
import time
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

def scrape_multiple_pages(max_pages=5):
    all_books = []

    for page in range(1, max_pages + 1):
        url = BASE_URL.format(page)
        print(f"Scraping page {page} of {max_pages}...")
        
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Stopped at page {page} (Status: {response.status_code})")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")

        for book in books:
            title = book.h3.a["title"]
            # Clean encoding artifact (Â£ -> £)
            raw_price = book.find("p", class_="price_color").text.strip()
            clean_price = raw_price.replace("Â", "")
            availability = book.find("p", class_="instock availability").text.strip()

            all_books.append({
                "Page": page,
                "Title": title,
                "Price": clean_price,
                "Availability": availability
            })

        time.sleep(0.5)  # Polite delay to avoid rate-limiting

    output_file = "all_scraped_books.csv"
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Page", "Title", "Price", "Availability"])
        writer.writeheader()
        writer.writerows(all_books)

    print(f"\nDone! Extracted {len(all_books)} total records into {output_file}")

if __name__ == "__main__":
    scrape_multiple_pages(max_pages=5)
