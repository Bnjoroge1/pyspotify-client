from pyspotify.core.config import read_config_file
from pyspotify.auth.auth_config import AuthMode
from pyspotify.core.exceptions import BadRequestError

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

     try:
          with open(file_path, mode='r', encoding = 'UTF-8') as file:
               refresh_token = file.readline()
               if refresh_token:
                    return _refresh_access_token(auth_key,refresh_token)

     except IOError as io_err:
          raise IOError(
     'Please authorise the application. The .pyspotify file was not found')

def _authorization_code_request(auth_code):
     config = read_config_file()
     auth_key = _get_access_token(config.client_id, config.client_secret)
     headers = {'Authorization': f'Basic {auth_key}', }
     options = {
     'code': auth_code,
     'redirect_uri': 'http://localhost:3000/callback',
     'grant_type': 'authorization_code',
     'json': True
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

     access_token = content.get('access_token', None)
     token_type = content.get('token_type', None)
     expires_in = content.get('expires_in', None)
     scope = content.get('scope', None)
     refresh_token = content.get('refresh_token', None)
     
     return Authorization(access_token, token_type, expires_in,
          scope, refresh_token)

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
     auth_key = _get_access_token(conf.client_secret, conf.client_id)
     headers = {'Authorization' : f'Basic {auth_key}'}

     options = {
          'grant_type' : 'client_credentials',
          'json' : True,
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
     scope = content.get('scope', None)
     return Authorization(access_token, token_type, expires_in, scope, None)

def _refresh_access_token(auth_key, refresh_token):
     headers = f'Authorization : Basic {auth_key}'
     options = {
          'refresh_token' : refresh_token,
          'grant_type' : 'refresh_token',
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

     return Authorization(access_token,token_type,expires_in,scope, refresh_token)  

def authenticate(conf):
     if conf.auth_mode == AuthMode.CLIENT_CREDENTIALS:
          return _authentication_request(conf)
     
     return _get_auth_code(conf)


