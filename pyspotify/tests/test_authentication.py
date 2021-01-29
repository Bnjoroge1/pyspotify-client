import pytest
import base64

from pyspotify.core import read_config_file

config = read_config_file()
class TestAuthentication:     
     def test_read_config_file():
          config = read_config_file()
          assert  isinstance(config, dict)
     def test_contains_client_id():
          assert config.has_key('client_id')

