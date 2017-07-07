import random
from typing import Dict

import bs4
import requests


def __random_user_agent() -> str:
    possible_user_agents = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 '
        f'Firefox/{random.randint(37,41)}.{random.randint(0,1)}',

        'Mozilla/5.0 (Macintosh; Intel Mac OS X '
        f'10_12_{random.randint(0,5)}) AppleWebKit/537.36 '
        f'(KHTML, like Gecko) Chrome/{random.randint(55,59)}'
        f'.0.3071.{random.randint(0,999)} Safari/537.36',

        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
        f'(KHTML, like Gecko) Chrome/42.0.2311.{random.randint(0,999)} '
        f'Safari/537.36 Edge/12.{random.randint(230,470)}'

    ]
    return random.choice(possible_user_agents)


def __get_headers() -> Dict[str, str]:
    return {
        'User-Agent': __random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                  'image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip',
        'Accept-Language': 'en-US,en;q=0.8',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Expires': '0'
    }


def get_page(url: str) -> bs4.BeautifulSoup:
    response = requests.get(url, headers=__get_headers(), timeout=30)
    page = bs4.BeautifulSoup(response.text, "html.parser")
    return page
