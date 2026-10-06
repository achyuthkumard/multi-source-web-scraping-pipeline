import requests

from processing.logger import setup_logger
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timezone
# from processing.models import Record

class QuotesScraper:

    BASE_URL = "https://quotes.toscrape.com/page/1/"

    def __init__(self):
        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "Mozilla/5.0"
        })
        self.logger = setup_logger()

    def fetch_page(self, url):
        response = self.session.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        return response.text

    def parse_quotes(self, html, page_url):

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        quotes = []

        quote_blocks = soup.select(
            "div.quote"
        )

        for block in quote_blocks:

            # -------------------------
            # Quote text
            # -------------------------

            text_element = block.select_one(
                "span.text"
            )

            text = None

            if text_element:
                text = text_element.get_text(
                    strip=True
                )

            # -------------------------
            # Author
            # -------------------------

            author_element = block.select_one(
                "small.author"
            )

            author = None

            if author_element:
                author = author_element.get_text(
                    strip=True
                )

            # -------------------------
            # Tags
            # -------------------------

            tags = [
                tag.get_text(strip=True)
                for tag in block.select(
                    "div.tags a.tag"
                )
            ]

            # -------------------------
            # Record
            # -------------------------

            scraped_at = datetime.now(timezone.utc).isoformat()

            quote = {
                "source": "Quotes to Scrape",
                "source_url": page_url,
                "name_or_title": text,
                "category": None,
                "price": None,
                "rating": None,
                "author": author,
                "tags": tags,
                "description": None,
                "availability": None,
                "scraped_at": scraped_at,
            }

            quotes.append(quote)

        return quotes

    def scrape(self):

        all_quotes = []

        current_url = self.BASE_URL

        while current_url:

            print(
                f"Scraping: {current_url}"
            )

            try:

                html = self.fetch_page(
                    current_url
                )

                quotes = self.parse_quotes(
                    html,
                    current_url
                )

                all_quotes.extend(quotes)

                soup = BeautifulSoup(
                    html,
                    "html.parser"
                )

                next_button = soup.select_one(
                    "li.next a"
                )

                if next_button:

                    next_url = next_button.get(
                        "href"
                    )

                    current_url = urljoin(
                        current_url,
                        next_url
                    )

                else:

                    current_url = None

            except requests.RequestException as error:

                print(
                    f"Request failed for "
                    f"{current_url}: {error}"
                )

                current_url = None

        return all_quotes


if __name__ == "__main__":

    scraper = QuotesScraper()

    quotes = scraper.scrape()

    print(
        "\nTotal quotes:",
        len(quotes)
    )

    print("\nFirst quote:")

    print(quotes[0])