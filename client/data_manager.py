from .menu import MenuItem
from pyspotify.core import Search
from  pyspotify.exceptions import EmptyResultsError
from pyspotify.auth import authenticate
from pyspotify.core import read_config_file


class DataManager():
     def __init__(self) -> None:
              self._config = read_config_file()
              self._auth = authenticate(self._config)

     def search_artist(self, criteria):
          results = Search().search_artist(criteria, self._auth)
          items =  results['artists']['items']

          if not items:
               raise EmptyResultsError(f'COuld not find the artist : {criteria}')

          return items[0]

     def _format_artist_label(self, item):
          return f'{item["name"]} ({item["type"]})'

     def _format_track_label(self, item):
          time = int(item['duration_ms'])
          minutes = int((time / 60000) % 60)
          seconds = int((time / 1000) % 60)
          track_name = item['name']
          return f'{track_name} - [{minutes}:{seconds}]'

     def get_artist_albums(self, artist_id, max_items=20):
          albums = Search().get_artists_albums(artist_id, self._auth)['items']
          if not albums:
               raise EmptyResultsError(f'Could not find any albums for the artist_id: {artist_id}')
          return [MenuItem(self._format_artist_label(album), album) for album in albums[:max_items]]
     
     def get_album_tracklist(self, album_id):
          results = Search().get_album_tracks(album_id, self._auth)
          if not results:
                raise EmptyResultsError('Could not find the tracks for this album')
          tracks = results['items']
          return [MenuItem(self._format_track_label(track), track)
          for track in tracks]

     def play(self, track_uri):
          Search().play(self._auth, track_uri)
 