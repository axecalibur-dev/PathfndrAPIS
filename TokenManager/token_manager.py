import requests
import os
import time

from RedisClient.redis_client import RedisUtil


class AmadeusTokenManager:
    access_token = None
    token_expiry = 0

    @classmethod
    def fetch_token(cls):
        response = requests.post(
            os.environ.get('AMADEUS_TEST_URL'),
            data={
                'grant_type': 'client_credentials',
                'client_id': os.environ.get('AMADEUS_CLIENT_ID'),
                'client_secret': os.environ.get('AMADEUS_CLIENT_SECRET'),
            }
        )
        response_data = response.json()
        cls.access_token = response_data['access_token']
        cls.token_expiry = time.time() + response_data['expires_in']
        return cls.access_token, cls.token_expiry

    @classmethod
    def token_refresh(cls, generate_new_token):
        if cls.access_token is None or time.time() >= cls.token_expiry - 1800:
            cls.fetch_token()
        if generate_new_token is True:
            cls.fetch_token()

        return cls.access_token

    @classmethod
    def get_access_token(cls):
        return RedisUtil.get("access_token")
