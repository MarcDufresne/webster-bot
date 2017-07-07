import argparse
from datetime import datetime

import telegram.bot
from webster.plugins.amazon import (
    listing_filter_products, listing_generate_amazon_search_url,
    listing_get_products)

from webster.utils.scrapper import get_page

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--search')
parser.add_argument('-t', '--title')
parser.add_argument('-p', '--publisher')
parser.add_argument('--token')
parser.add_argument('--id')

TOKEN = ""
CHAT_ID = ""


def main(search_term: str, title_match: str = None,
         publisher_match: str = None):
    search_url = listing_generate_amazon_search_url(search_term)
    page = get_page(search_url)

    all_products = listing_get_products(page)

    if title_match or publisher_match:
        all_products = listing_filter_products(
            all_products, title_match, publisher_match)

    print(f"[{datetime.now().isoformat()}] Found: {len(all_products)} matching"
          f" title [{title_match}] and publisher [{publisher_match}]"
          f" with query [{search_term}]")

    telegram_bot = telegram.bot.Bot(TOKEN)
    for t, d in all_products.items():
        telegram_bot.send_message(CHAT_ID, f"{t} on Amazon: {d['link']}")


if __name__ == '__main__':
    args = parser.parse_args()
    TOKEN = args.token
    CHAT_ID = args.id
    main(args.search, args.title, args.publisher)
