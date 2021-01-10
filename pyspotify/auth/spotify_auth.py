from .authenticate import _refresh_access_token
from pyspotify.auth.auth_config import AuthMode
from urllib.parse import urlencode

import requests
import json

from flask import Flask, render_template, url_for, redirect,request
from pyspotify.core import read_config_file, BadRequestError
from pyspotify.auth import _authentication_request, Authorization, _get_access_token, _authorization_code_request

app  =  Flask(__name__)

@app.route('/')
def home():
     config = read_config_file()
     params = {
          'client_id ' : config.client_id,
          'response_type' : 'code',
          'redirect_uri' : 'https://localhost:5000/callback',
          'scope' : 'user-read-private user-modify-state playlist-modify-private user-read-recently-played user-top-read user-library-modify library-read',
     }
     encoded_url = urlencode(params)
     url = f'{config.AUTH_URL}?{encoded_url}'
     
     return render_template('index.html', url=url)

@app.route('/callback')
def callback():
     config = read_config_file()
     code = request.args.get('code ', '')
     response = _authorization_code_request(config, code)

     with open('.pyspotify', mode='w', encoding='utf-8') as auth_code_file:
          auth_code_file.write(response.refresh_token)
     
     return 'ALl set. Please close the window'


     


if'__name__' == __main__:
     app.run(host='localhost', port=5000)
