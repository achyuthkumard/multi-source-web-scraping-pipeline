import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://books.toscrape.com/catalogue/page-1.html"


def main():
    response = requests.get(URL, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.select("article.product_pod")

    print("Books found:", len(books))

    first_book = books[0]

    title = first_book.h3.a.get("title")

    price = first_book.select_one(".price_color").get_text(strip=True)

    availability = first_book.select_one(
        ".availability"
    ).get_text(strip=True)

    rating_element = first_book.select_one(".star-rating")

    rating = rating_element.get("class")[-1]

    relative_url = first_book.h3.a.get("href")

    product_url = urljoin(URL, relative_url)

    print("\nFirst book")
    print("--------------------")
    print("Title:", title)
    print("Price:", price)
    print("Availability:", availability)
    print("Rating:", rating)
    print("URL:", product_url)

    next_button = soup.select_one("li.next a")

    if next_button:
        next_url = urljoin(URL, next_button.get("href"))
        print("\nNext page:", next_url)
    else:
        print("\nNo next page")


if __name__ == "__main__":
    main()