import pytest
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotify_models import Artist


@pytest.fixture
def auth_manager():
    return SpotifyClientCredentials(
        client_id="41f2c1f5326542aa80fa32d186e3ee40",
        client_secret="cb9d05da4aba443c85a094914f4f3ca9")


@pytest.fixture
def spotify(auth_manager):
    return spotipy.Spotify(auth_manager=auth_manager)


def test_parse_justin_bieber(spotify: spotipy.Spotify):
    justin_bieber_spotify_uri = "spotify:artist:1uNFoZAHBGtllmzznpCI3s"
    justin_bieber = Artist(name="Justin Bieber", uri=justin_bieber_spotify_uri)
    result = spotify.artist(justin_bieber_spotify_uri)
    assert justin_bieber == Artist(**result)
