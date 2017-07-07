from typing import Dict, List
from urllib.parse import urlencode

import bs4

from webster.utils.slug_utils import to_lower

Products = Dict[str, Dict]

_BASE_SEARCH_URL = "https://www.amazon.ca/s/?"


def listing_get_products(page: bs4.BeautifulSoup) -> Products:
    all_products: List[bs4.Tag] = page.find_all(
        class_="s-access-detail-page")

    parsed_products = {}
    for product in all_products:
        publisher_lines: List[bs4.Tag] = product.parent.parent.find_all(
            "span", class_="a-size-small a-color-secondary")
        publisher_string = " ".join(t.text for t in publisher_lines)

        parsed_products[product.text] = {
            "link": product.attrs['href'],
            "title": product.text,
            "publisher": publisher_string
        }

    return parsed_products


def listing_filter_products(products: Products, title_match: str = None,
                            publisher_match: str = None) -> Products:
    if title_match and publisher_match:
        filtered_products = {
            k: v for k, v in products.items()
            if to_lower(title_match) in to_lower(v['title'])
               and to_lower(publisher_match) in to_lower(v['publisher'])
        }
    elif title_match:
        filtered_products = {
            k: v for k, v in products.items()
            if to_lower(title_match) in to_lower(v['title'])
        }
    elif publisher_match:
        filtered_products = {
            k: v for k, v in products.items()
            if to_lower(publisher_match) in to_lower(v['publisher'])
        }
    else:
        filtered_products = products

    return filtered_products


def listing_generate_amazon_search_url(search_term: str) -> str:
    search_arg = urlencode({'field-keywords': search_term})
    return _BASE_SEARCH_URL + search_arg
