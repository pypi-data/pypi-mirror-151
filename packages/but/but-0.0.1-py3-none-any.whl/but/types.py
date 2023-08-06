from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, TypedDict


class LabelRelation(Enum):
    genre = 'genre'


@dataclass
class AppLabel:
    app: Application
    relation: LabelRelation
    value: str


@dataclass
class Application:
    title: str
    labels: List[AppLabel]


class SteamAccount(TypedDict):
    steamid: int
    apikey: str


class SteamOwnedGame(TypedDict):
    appid: int
    name: str
    img_icon_url: str
    has_community_visible_stats: bool
    playtime_forever: int
    playtime_windows_forever: int
    playtime_mac_forever: int
    playtime_linux_forever: int
