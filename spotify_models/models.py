from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import datetime
from enum import Enum
from functools import wraps
from typing import Callable, ClassVar

from iso3166 import Country
import spotipy


@dataclass
class SpotifyItem(ABC):
    _spotify: ClassVar[spotipy.Spotify] = None

    uri: str
    last_fetch: datetime.datetime = field(default=None, init=False, compare=False)

    @classmethod
    @property
    def spotify(cls):
        if not cls._spotify:
            auth_manager = spotipy.SpotifyClientCredentials(
                client_id="41f2c1f5326542aa80fa32d186e3ee40",
                client_secret="cb9d05da4aba443c85a094914f4f3ca9")
            cls._spotify = spotipy.Spotify(auth_manager=auth_manager)
        return cls._spotify

    def fetch_if_stale(fetch_method: Callable):
        def decorator(func):
            def wrapper(self):
                THRESHOLD = datetime.timedelta(days=1)
                if not self.last_fetch or self.last_fetch < datetime.datetime.now() - THRESHOLD:
                    self.fill(fetch_method(self.uri))
                    self.last_fetch = datetime.datetime.now()
                return func(self)
            return wrapper
        return decorator

    @abstractmethod
    def fill(self, data: dict):
        pass


@dataclass
class Artist(SpotifyItem):
    _name: str = field(default=None, init=False)
    _genres: list[str] = field(default_factory=list, repr=False, compare=False)
    _images: list[ImageRef] = field(default_factory=list, repr=False, compare=False)
    _popularity: int = field(default=None, repr=False, compare=False)
    _followers: int = field(default=None, repr=False, compare=False)
    _external_urls: dict[str, str] = field(default_factory=dict, repr=False, compare=False)

    @property
    @SpotifyItem.fetch_if_stale(SpotifyItem.spotify.artist)
    def name(self):
        return self._name
    
    @property
    @SpotifyItem.fetch_if_stale(SpotifyItem.spotify.artist)
    def genres(self):
        return self._genres
    
    @property
    @SpotifyItem.fetch_if_stale(SpotifyItem.spotify.artist)
    def images(self):
        return self._images
    
    @property
    @SpotifyItem.fetch_if_stale(SpotifyItem.spotify.artist)
    def popularity(self):
        return self._popularity
    
    @property
    @SpotifyItem.fetch_if_stale(SpotifyItem.spotify.artist)
    def followers(self):
        return self._followers
    
    @property
    @SpotifyItem.fetch_if_stale(SpotifyItem.spotify.artist)
    def external_urls(self):
        return self._external_urls

    def fill(self, data: dict):
        self._name = data.get("name", None)
        self._genres = data.get("genres", [])
        self._images = [ImageRef(**image) for image in data.get("images", [])]
        self._popularity = data.get("popularity", None)
        self._followers = data.get("followers", {}).get("total", None)
        self._external_urls = data.get("external_urls", {})


@dataclass
class Track:
    name: str
    artists: list[Artist]
    album: Album
    duration_ms: int
    explicit: bool = field(default=False)
    popularity: int = field(default=None, repr=False, compare=False)
    uri: str = None
    is_local: bool = field(default=None, compare=False)
    disc_number: int = field(default=None, repr=False, compare=False)
    track_number: int = field(default=None, repr=False, compare=False)
    available_markets: list[Country] = field(default_factory=list, repr=False, compare=False)
    external_ids: dict[str, str] = field(default_factory=dict, repr=False, compare=False)
    external_urls: dict[str, str] = field(default_factory=dict, repr=False, compare=False)
    is_playable: bool = field(default=None, repr=False, compare=False)
    linked_from: bool = field(default=None, repr=False, compare=False)
    preview_url: str = field(default=None, repr=False, compare=False)
    restrictions: list[str] = field(default_factory=list, repr=False, compare=False)


class AlbumType(Enum):
    SINGLE = "single"
    ALBUM = "album"


@dataclass
class Album:
    name: str
    artists: list[Artist]
    album_type: AlbumType
    tracks: list[Track]
    genres: list[str]
    images: list[ImageRef]
    popularity: int
    release_date: datetime
    uri: str
    available_markets: list[Country]
    copyrights: dict[str, str]
    external_ids: dict[str, str]
    external_urls: dict[str, str]


@dataclass
class ImageRef:
    height: int
    width: int
    url: str
