import requests
from bs4 import BeautifulSoup


URL = "https://quotes.toscrape.com/page/1/"


def main():
    response = requests.get(URL, timeout=10)

    print("Status code:", response.status_code)

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    print("Page title:", soup.title.get_text(strip=True))

    quotes = soup.select("div.quote")

    print("Quotes found:", len(quotes))

    first_quote = quotes[0]

    text = first_quote.select_one("span.text").get_text(
        strip=True
    )

    author = first_quote.select_one(
        "small.author"
    ).get_text(strip=True)

    tags = [
        tag.get_text(strip=True)
        for tag in first_quote.select("div.tags a.tag")
    ]

    print("\nFirst quote")
    print("--------------------")
    print("Text:", text)
    print("Author:", author)
    print("Tags:", tags)

    next_button = soup.select_one("li.next a")

    if next_button:
        print("Next page:", next_button.get("href"))
    else:
        print("No next page")


if __name__ == "__main__":
    main()