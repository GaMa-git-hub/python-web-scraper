import requests
from bs4 import BeautifulSoup
import csv
import logging

class Scraper:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/91.0.4472.124 Safari/537.36"
        }

    def fetch_data(self):
        logging.info(f"Fetching data from {self.url}")
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data: {e}")
            return None

    def parse_data(self, html):
        soup = BeautifulSoup(html, "html.parser")
        quotes = []

        quote_blocks = soup.find_all("div", class_="quote")

        for block in quote_blocks:
            quote = block.find("span", class_="text")
            author = block.find("small", class_="author")  # fixed here

            if quote and author:
                quotes.append([quote.text.strip(), author.text.strip()])
            else:
                logging.warning("Skipping quote due to missing data.")

        return quotes

    def save_to_csv(self, quotes, filename="quotes.csv"):
        try:
            logging.info(f"Saving quotes to {filename}")
            with open(filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Quote", "Author"])
                writer.writerows(quotes)
        except PermissionError:
            logging.error(f"Permission denied: close {filename} if it’s open in another app.")
        except Exception as e:
            logging.error(f"Unexpected error saving to CSV: {e}")

    def run(self):
        html = self.fetch_data()
        if html:
            quotes = self.parse_data(html)
            if quotes:
                self.save_to_csv(quotes)
            else:
                logging.warning("No quotes found.")
        else:
            logging.error("Failed to retrieve HTML content.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    url = "http://quotes.toscrape.com"
    scraper = Scraper(url)
    scraper.run()
