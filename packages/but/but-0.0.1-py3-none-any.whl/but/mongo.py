from typing import List

from pymongo.database import Database
from pymongo.mongo_client import MongoClient

from .types import SteamOwnedGame


def connect():
    client = MongoClient('mongo', 27017)
    return client['video_games']


def save_steam_owned_games(database: Database, steamid: int, owned_games: List[SteamOwnedGame]):
    games = [{'appid': g['appid'], 'name': g['name']} for g in owned_games]
    database['steam_owned_games'].update_one({'steamid': steamid}, {'$set': {'games': games}}, upsert=True)
