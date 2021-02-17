import requests
import json
from urllib.parse import urlencode
from .request_type import RequestType
from .config import read_config_file
from .api_request import execute_request
from .parameters import prepare_params


class Search:
     def __init__(self, criteria, auth, search_type) -> None:
          self.criteria = criteria
          self.auth = auth
          self.search_type = search_type
              
     def _search(self,criteria, auth, search_type):
          conf = read_config_file()
          if not criteria:
               raise AttributeError('Parameter `criteria` is required.')
          q_type = search_type.name.lower()
          url = urlencode(f'{conf.base_url}/search?{criteria}&type={q_type}')

          headers = {'Authorization': f'Bearer {auth.access_token}'}

          response = requests.get(url, headers=headers)

          return json.loads(response.text)
     
     def search_artist(self, criteria, auth):
          return   self._search(criteria, auth, SearchType.ARTIST)

     def search_album(self, criteria, auth):
          return self._search(criteria, auth, SearchType.ALBUM)

     def search_playlist(self, criteria, auth):
          return self._search(criteria, auth, SearchType.PLAYLIST)

     def search_track(self, criteria, auth):
          return self._search(criteria, auth, SearchType.TRACK)
     

     def get_artists_albums(artist_id, auth, params=None):
          if artist_id is None or artist_id is "":
               raise AttributeError("Parameter 'Artist id' cannot be none. ")
          url_template = '{base_url}/{area}/{artistid}/{postfix}{query}'
          url_params = {
               'query' :  prepare_params(params),
               'area': 'albums',
               'albumid': artist_id,
               'postfix': 'tracks',
          }
          return execute_request(url_template, auth, url_params)

     def get_album_tracks(album_id, auth, params=None):
          if album_id is None or album_id is '':
               raise AttributeError('Parameter `album_id` cannot be `None`  or empty.')
          url_template = '{base_url}/{area}/{albumid}/{postfix}{query}'
          url_params = {
          'query': prepare_params(params),
          'area': 'albums',
          'albumid': album_id,
          'postfix': 'tracks',
          }
          return execute_request(url_template, auth, url_params)

     def play(track_uri, auth, params=None):
          if track_uri is None or track_uri is '':
               raise AttributeError("Parameter 'track_uri' cannot be empty")
          url_template = f'{base_url}/{area}{post_fix}'
          url_params = {
               'query': prepare_params(params),
               'area' : 'me',
               'postfix' : 'player/play'          }
          payload = {
               'uris':[track_uri],
               'offset' : {'uri' : track_uri}
          }
          return execute_request(url_template, auth, params)
