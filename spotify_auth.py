from os import error
from pyspotify.auth.authenticate import _refresh_access_token
from pyspotify.auth.auth_config import AuthMode
from urllib.parse import urlencode

import requests
import json

from flask import Flask, render_template, url_for, redirect,request
from pyspotify.core import read_config_file, BadRequestError
from pyspotify.auth import _authentication_request, Authorization, _get_access_token, _authorization_code_request

app  =  Flask(__name__)
config = read_config_file()

@app.route('/')
def home():     
     params = {
          'response_type' : 'code',
          'client_id' : config.client_id,
          'redirect_uri' : 'http://localhost:5000/callback',
          'scope' : 'user-read-private playlist-modify-private user-read-recently-played user-top-read user-library-modify user-library-read',
     }
     encoded_url = urlencode(params)
     url = f'{config.AUTH_URL}?{encoded_url}'
     
     return render_template('index.html', url=url)

@app.route('/callback')
def callback():
     code = request.args.get('code', '')
     response = _authorization_code_request(code)

     try:
          with open('.pyspotify', mode='w', encoding='utf-8') as auth_code_file:
               auth_code_file.write(response.refresh_token) 
     except error as err:
          raise BadRequestError(err)

     finally:
          return f'All set. Please close the window.'


     


if __name__ == '__main__':
     app.run(host='localhost', port=5000)
