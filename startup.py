from flask import jsonify

from RedisClient.redis_client import RedisUtil
from TokenManager.token_manager import AmadeusTokenManager


def application_startup():
    access, expiry_at = AmadeusTokenManager.fetch_token()
    print("ADSF>?ASMKF:LSJNFDLKSDJHF")
    RedisUtil.set("access_token", access)
    return access, expiry_at
