from pathlib import Path, PurePosixPath
from typing import List
from urllib.parse import urlsplit

import toml

from .html import get_canonical_url
from .http import client as http_client
from .types import SteamAccount, SteamOwnedGame

STEAM_API_OWNED_GAMES_URL = 'https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/'

STEAM_APP_URL = 'https://store.steampowered.com/app/%d/'

STEAM_APP_JPEG_URLS = [
    'https://steamcdn-a.akamaihd.net/steam/apps/%d/library_600x900_2x.jpg',
    'https://cdn.cloudflare.steamstatic.com/steam/apps/%d/library_600x900_2x.jpg',
]


def get_accounts() -> List[SteamAccount]:
    a = Path('/run/secrets/steam.toml').read_text(encoding='utf-8')
    return toml.loads(a).get('accounts', [])


def get_url_name(appid: int):
    try:
        r = http_client.get(
            STEAM_APP_URL % appid,
            cookies={'birthtime': '0', 'wants_mature_content': '1'},
            allow_redirects=False,
        )
        assert r.status_code == 200

        canonical_url = get_canonical_url(r.text)
        assert canonical_url

        url_name = PurePosixPath(urlsplit(canonical_url).path).name
        assert url_name
        return url_name

    except AssertionError as err:
        raise RuntimeError(f'Cannot get url_name for appid {appid}') from err


def fetch_picture(appid: int, url_name=None):
    for url in STEAM_APP_JPEG_URLS:
        url = url % appid

        r = http_client.get(url, allow_redirects=False)
        if r.status_code == 200:
            if url_name is None:
                url_name = get_url_name(appid)

            jpeg = Path(f'/storage/pictures/steam/{url_name}.jpeg')
            jpeg.write_bytes(r.content)
            return jpeg


def get_owned_games(steamid: int, apikey: str) -> List[SteamOwnedGame]:
    'https://partner.steamgames.com/doc/webapi/IPlayerService#GetOwnedGames'

    r = http_client.get(
        STEAM_API_OWNED_GAMES_URL,
        params={
            'key': apikey,
            'steamid': steamid,
            'include_appinfo': 1,
            'include_played_free_games': 1,
        },
        allow_redirects=False,
    )
    if r.status_code == 200:
        return r.json()['response']['games']

    return []
