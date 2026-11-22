import csv
import requests
from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/"

def scrape_books():
    print("Fetching webpage...")
    response = requests.get(URL, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    results = []
    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text.strip()
        availability = book.find("p", class_="instock availability").text.strip()

        results.append({
            "Title": title,
            "Price": price,
            "Availability": availability
        })

    output_file = "scraped_books.csv"
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Title", "Price", "Availability"])
        writer.writeheader()
        writer.writerows(results)

    print(f"Success! Saved {len(results)} books to {output_file}")

if __name__ == "__main__":
    scrape_books()
