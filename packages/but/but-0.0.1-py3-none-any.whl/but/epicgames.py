from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from .html import get_epicgames_picture_url
from .http import client as http_client

EPIC_APP_URL = 'https://store.epicgames.com/en-US/p/%s'
EPIC_SEARCH_URL = 'https://store.epicgames.com/en-US/browse'


def fetch_picture(egsid: str):
    r = http_client.get(
        EPIC_SEARCH_URL,
        params={
            'q': egsid,
            'sortBy': 'relevancy',
            'sortDir': 'DESC',
            'count': '40',
        },
        allow_redirects=False,
    )
    if r.status_code == 200:
        picture_url = get_epicgames_picture_url(r.text, egsid)
        picture_url = urlunsplit(urlsplit(picture_url)._replace(query=''))

        r = http_client.get(picture_url, allow_redirects=False)
        if r.status_code == 200:
            jpeg = Path(f'/storage/pictures/epicgames/{egsid}.jpeg')
            jpeg.write_bytes(r.content)
            return jpeg
