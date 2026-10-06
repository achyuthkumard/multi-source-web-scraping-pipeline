import requests
import logging
import time

from processing.logger import setup_logger
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timezone
# from processing.models import Record


class BooksScraper:

    BASE_URL = "https://books.toscrape.com/catalogue/page-1.html"

    def __init__(self):
        self.session = requests.Session()
        # self.logger = setup_logger()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0"
            
        })
        self.logger = setup_logger()

    def fetch_page(self, url, max_retries=3):
        """
        Fetch a page with retry handling.

        Retries temporary request failures before
        giving up.
        """

        for attempt in range(1, max_retries + 1):

            try:

                self.logger.info(
                    "Fetching %s (attempt %d/%d)",
                    url,
                    attempt,
                    max_retries
                )

                response = self.session.get(
                    url,
                    timeout=10
                )

                response.raise_for_status()
                time.sleep(0.2)

                return response.text

            except requests.RequestException as error:

                self.logger.warning(
                    "Request failed for %s: %s",
                    url,
                    error
                )

                if attempt == max_retries:

                    self.logger.error(
                        "Giving up on %s after %d attempts",
                        url,
                        max_retries
                    )

                    raise

        return None

    def parse_books(self, html, page_url):
        
        soup = BeautifulSoup(html, "html.parser")

        books = []

        book_cards = soup.select("article.product_pod")

        for card in book_cards:

            title_element = card.select_one("h3 a")
            price_element = card.select_one(".price_color")
            availability_element = card.select_one(".availability")
            rating_element = card.select_one(".star-rating")

            # Title
            title = None
            if title_element:
                title = title_element.get("title")

            # Price
            price = None
            if price_element:
                price = price_element.get_text(strip=True)

            # Availability
            availability = None
            if availability_element:
                availability = availability_element.get_text(
                    " ",
                    strip=True
                )

            # Rating
            rating = None
            if rating_element:
                classes = rating_element.get("class", [])

                if len(classes) > 1:
                    rating = classes[-1]

            # Product URL
            product_url = None

            if title_element:
                relative_url = title_element.get("href")

                if relative_url:
                    product_url = urljoin(
                        page_url,
                        relative_url
                    )
            
            
            # Get detail-page information
            category = None
            description = None

            if product_url:
                

                try:
                    
                    detail_html = self.fetch_page(product_url)

                    details = self.parse_book_details(detail_html)

                    category = details["category"]
                    description = details["description"]

                except requests.RequestException as error:

                    self.logger.warning(
                        "Unable to fetch book detail page %s: %s",
                        product_url,
                        error
                    )
            

            # book = {
            #     "source": "Books to Scrape",
            #     "source_url": product_url,
            #     "name_or_title": title,
            #     "price": price,
            #     "availability": availability,
            #     "rating": rating
            # }
            scraped_at = datetime.now(timezone.utc).isoformat()

            book = {
                "source": "Books to Scrape",
                "source_url": product_url,
                "name_or_title": title,
                "category": category,
                "price": price,
                "rating": rating,
                "author": None,
                "tags": None,
                "description": description,
                "availability": availability,
                "scraped_at": scraped_at,
            }

            books.append(book)

        return books
    def parse_book_details(self, html):
        
        soup = BeautifulSoup(html, "html.parser")

    # -------------------------
    # Category
    # -------------------------
        category = None

        breadcrumb_links = soup.select("ul.breadcrumb li a")

        if len(breadcrumb_links) >= 3:
            category = breadcrumb_links[2].get_text(strip=True)

    # -------------------------
    # Description
    # -------------------------
        description = None

        description_heading = soup.find(
            "h2",
            string=lambda text: text and "Product Description" in text
        )

        if description_heading:
            description_element = description_heading.find_next_sibling("p")

            if description_element:
                description = description_element.get_text(
                    " ",
                    strip=True
                )

        return {
            "category": category,
            "description": description
        }

    def scrape(self):
        all_books = []
        current_url = self.BASE_URL

        while current_url:

            self.logger.info(
                "Scraping listing page: %s",
                current_url
            )

            try:
                html = self.fetch_page(current_url)

                books = self.parse_books(
                    html,
                    current_url
                )

                all_books.extend(books)

                soup = BeautifulSoup(
                    html,
                    "html.parser"
                )

                next_button = soup.select_one(
                    "li.next a"
                )

                if next_button:
                    next_url = next_button.get("href")

                    current_url = urljoin(
                        current_url,
                        next_url
                    )
                else:
                    current_url = None

            except requests.RequestException as error:

                self.logger.error(
                    "Failed to process listing page %s: %s",
                    current_url,
                    error
                )

                current_url = None

        return all_books


if __name__ == "__main__":

    scraper = BooksScraper()

    books = scraper.scrape()

    print("\nTotal books:", len(books))

    print("\nFirst book:")
    print(books[0])
    
if __name__ == "__main__":

    scraper = BooksScraper()

    url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

    html = scraper.fetch_page(url)

    details = scraper.parse_book_details(html)

    print(details)