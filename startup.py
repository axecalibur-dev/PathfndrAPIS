from flask import jsonify

from RedisClient.redis_client import RedisUtil
from TokenManager.token_manager import AmadeusTokenManager


def application_startup():
    access, expiry_at = AmadeusTokenManager.fetch_token()
    RedisUtil.set("access_token", access)
    return access, expiry_at
