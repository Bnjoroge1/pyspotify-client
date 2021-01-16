import os, yaml
from collections import namedtuple
from ..auth  import AuthMode


Config = namedtuple('Config', ['client_id',
 'client_secret',
 'access_token_url',
 'AUTH_URL',
 'api_version',
 'api_url',
 'base_url',
 'auth_mode', ])

def read_config_file():
     current_dir = os.path.abspath(os.curdir)
     file_path = os.path.join(current_dir, 'config.yaml')
     """Function reads  A Yaml Config File and yaml is used to load the contents to a python object. The appropriate and necessary config values are assigned to the object variables.

     Returns:
         [type NamedTUple]: An instance of the named tuple with correct values.
     """     
     try:
          with open(file_path, 'r', encoding='UTF-8') as yaml_file:
               config_file = yaml.safe_load(yaml_file)
               config_file['base_url'] = f'{config_file["api_url"]}/{config_file["api_version"]}'
               auth_mode = config_file['auth_mode']
               config_file['auth_mode'] = AuthMode.__members__.get(auth_mode)

               return Config(**config_file)

     except  IOError as err:
          print('''Error: Could not load the YAML FIle on your current directory.
          Please ensure you have used the following format : 
          client_id: 'your_client_id'
          client_secret: 'you_client_secret'
          access_token_url: 'https://accounts.spotify.com/api/token'
          auth_url: 'http://accounts.spotify.com/authorize'
          api_version: 'v1'
          api_url: 'http//api.spotify.com'
          auth_method: 'authentication method'

          * auth_method can be CLIENT_CREDENTIALS or
          AUTHORIZATION_CODE
          ''')
          raise err
