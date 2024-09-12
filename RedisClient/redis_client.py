import os

import redis


class RedisUtil:
    client = redis.Redis(host='localhost', port=6379,decode_responses=True)

    @classmethod
    def set(cls, key, value, ex=None):
        cls.client.set(key, value, ex=ex)

    @classmethod
    def get(cls, key):
        value = cls.client.get(key)
        return value

    @classmethod
    def delete(cls, key):
        cls.client.delete(key)

    @classmethod
    def set_with_expiry(cls, key, value, expiry_in_seconds):
        cls.client.setex(key, int(expiry_in_seconds),value, )