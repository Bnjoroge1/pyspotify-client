import pyspotify.core as core
from .auth_config import AuthMode
from ..exceptions import BadRequestError
import base64
import json
import os
import requests
#from pyspotify.core import BadRequestError
from .authorization import Authorization


def _get_access_token(client_secret, client_id):
     byte_keys = bytes(f'{client_id} : {client_secret}', 'utf-8')
     encode_key = base64.b64encode(byte_keys)
     return encode_key.decode('utf-8')

def _get_auth_code(conf):
     """FUnction for getting the authorization code for authorization to access user data.

     Args:
         conf ([namedTuple]): [Conf object that contains values]

     Raises:
         IOError: [description]

     Returns:
         [type]: [description]
     """     
     current_dir = os.path.abspath(os.curdir)
     file_path = os.path.join(current_dir, 'pyspotify')

     auth_key = _get_access_token(conf.client_id, conf.client_secret)

     

def _authorization_code_request(auth_code):
     config = core.read_config_file()
     auth_key = _get_access_token(config.client_id, config.client_secret)
     response_type = 'code'
     headers = {'Authorization': f'Basic {auth_key}',
                'Content-Type': 'application/x-www-form-urlencoded' }
     options = {
     'client_id': f'{config.client_id}',
     'response_type': f'{response_type}',
     #'code': f'{auth_code}',
     'redirect_uri': 'http://localhost:5000/callback',
     'scope': 'user-read-private user-read-email user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-recently-played user-library-read user-library-modify user-top-read user-read-playback-position user-modify-playback-state streaming app-remote-control playlist-read-private playlist-modify-private playlist-read-collaborative playlist-modify-public',

     #'grant_type': f'client_credentials&client_id={config.client_id}client_secret={config.client_secret}',
 }
     response = requests.post(
     config.access_token_url,
     headers=headers,
     data=options
 )
 
     content = json.loads(response.content.decode('utf-8'))
     if response.status_code != 200:
          error_description = content.get('error_description', '')
          raise BadRequestError(error_description)
     #return code and state
     code = content.get('code', None)
     #access_token = content.get('access_token', None)
     #token_type = content.get('token_type', None)
     #expires_in = content.get('expires_in', None)
     #scope = content.get('scope', None)
     #refresh_token = content.get('refresh_token', None)
     return code
     #return Authorization(access_token, token_type, expires_in,
          #scope, refresh_token)

def _authentication_request(conf):
     """FUnction that makes authentication request for client credentials.

     Args:
         conf ([namedTuple Object]): [Object containing the configuration values]

     Raises:
         e: [standard exceptions]
         error_desc: [custom error description]

     Returns:
         [namedTuple]: [Authorization Object that contains the access_token, client, credentials etc. ]
     """     
     auth_code = _get_auth_code(conf)
     auth_key = _get_access_token(conf.client_secret, conf.client_id)
     headers = f'Authorization : Basic {auth_key}, Content-Type : application/x-www-form-urlencoded'

     options = {
          'grant_type' : 'authorization_code',
          'code' : f'{auth_code}',
          'redirect_uri' : 'http://localhost:5000/callback',
     }
     try:
          response = requests.post(
               'https://accounts.spotify.com/api/token',
               headers = headers,
               data = options,
          )

          content = json.loads(response.content.decode('utf-8'))
     except requests.ConnectionError as e: 
          raise e
     if response.status_code == 400:
          error_desc = content.get('error_description')
          #raise BadRequestError(error_desc)
          raise error_desc

     access_token = content.get('access_token', None)
     token_type = content.get('token_type', None)
     expires_in = content.get('expires_in', None)
     refresh_token = content.get('refresh_token', None)
     scope = content.get('scope', None)
     return Authorization(access_token, token_type, expires_in, scope, refresh_token)

def _refresh_access_token(auth_key, refresh_token):
     headers = f'Authorization : Basic {auth_key}, Content-Type : application/x-www-form-urlencoded'
     options = {
          'grant_type' : 'refresh_token',
          'refresh_token' : f'{refresh_token}',
     }

     response = requests.post('https://accounts.spotify.com/api/token',
     data=options, 
     headers=headers)

     content = json.loads(response)
     if not response.ok:
          error_dec = content.get('error_descripttion', None)
          raise BadRequestError(error_dec)

     access_token = content.get('access_token')
     token_type = content.get('token_type', None)
     scope = content.get('token_type', None)
     expires_in = content.get('expires_in', None)

     return Authorization(access_token,token_type,expires_in, scope)  

def authenticate(conf):
     if conf.auth_mode == AuthMode.CLIENT_CREDENTIALS:
          return _authentication_request(conf)
     elif conf.auth_mode == AuthMode.AUTHORIZATION_CREDENTIALS:
          return _authorization_code_request(conf)
     
     
     return _get_auth_code(conf)


