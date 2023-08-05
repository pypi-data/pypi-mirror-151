import webbrowser
from typing import List
import base64

import requests


class GitHub:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str, scopes: List[str] = None):
        if scopes is None:
            scopes = []
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect = redirect_uri
        self.scopes = scopes
        self.auth_url = f"https://github.com/login/oauth/authorize?client_id={self.client_id}&redirect_uri={self.redirect}&scope={' '.join(self.scopes)}" if scopes != [] else f"https://github.com/login/oauth/authorize?client_id={self.client_id}&redirect_uri={self.redirect}"
        self.token_url = f"https://github.com/login/oauth/access_token?client_id={self.client_id}&client_secret={self.client_secret}"

    def open_window(self):
        webbrowser.open(self.auth_url)

    def get_url(self):
        return self.auth_url

    def get_token(self, code: str):
        return requests.post(self.token_url + f"&code={code}", headers={"Accept": "application/json"}).json()[
            "access_token"
        ]


class Discord:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str, scopes: List[str]):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scopes = scopes
        self.auth_url = f"https://discord.com/api/oauth2/authorize?response_type=code&client_id={client_id}&scope={' '.join(self.scopes)}&redirect_uri={self.redirect_uri}&prompt=consent "
        self.token_url = f"https://discord.com/api/oauth2/token"

    def open_window(self):
        webbrowser.open(self.auth_url)

    def get_url(self):
        return self.auth_url

    def get_token(self, code: str):
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        return requests.post(self.token_url, data=payload, headers=headers).json()["access_token"]


class Spotify:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str, scopes=None):
        if scopes is None:
            scopes = []

        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scopes = scopes
        self.auth_url = f"https://accounts.spotify.com/authorize?response_type=code&client_id={self.client_id}&scope={' '.join(self.scopes)}&redirect_uri={self.redirect_uri}"

    def open_window(self):
        webbrowser.open(self.auth_url)

    def get_url(self):
        return self.auth_url

    def get_token(self, code: str):
        payload = {
            "code": code,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic "+base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        }
        return requests.post(f"https://accounts.spotify.com/api/token", data=payload, headers=headers)["access_token"]
