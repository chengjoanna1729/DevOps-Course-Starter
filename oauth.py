import os
import requests
from oauthlib.oauth2 import WebApplicationClient

class OAuthClient:
    def __init__(self):
        self.client_id = os.getenv("OAUTH_CLIENT_ID")
        self.client_secret = os.getenv("OAUTH_CLIENT_SECRET")
        self.authorization_url = 'https://github.com/login/oauth/authorize'
        self.token_url = 'https://github.com/login/oauth/access_token'
        self.user_url = 'https://api.github.com/user'
        self.client = WebApplicationClient(self.client_id)

    def redirect_to_github(self):
        return self.client.prepare_request_uri(self.authorization_url)

    def get_access_token(self, authorization_response):
        request = self.client.prepare_token_request(self.token_url, authorization_response, client_secret=self.client_secret)
        self.client.parse_request_body_response(requests.post(request).json())

