import json

import requests
import os
from dotenv import load_dotenv

from InternalServices.amadeus import Amadeus
from RedisClient.redis_client import RedisUtil
from TokenManager.token_manager import AmadeusTokenManager

load_dotenv()


class FlightsServices:

    @classmethod
    def get_flight_info(cls, origin_code, destination_code, departure_date, get_from_cache_flag=1):

        get_from_cache = False if get_from_cache_flag == 1 else True
        print("GET FROM REDIS",get_from_cache)
        if get_from_cache or get_from_cache is None:
            cached_info = RedisUtil.get(f'{origin_code}:{destination_code}:{departure_date}')
            print("RETURNING - CACHED DATA",cached_info)
            if not cached_info:
                print("DID NOT FOUND IN CACHE WILL TALK TO AMADEUS")
                client_response = Amadeus.get_from_amadeus(origin=origin_code,destination=destination_code, departure_date=departure_date)

                try:
                    redisSet = RedisUtil.set_with_expiry(
                    key=f'{origin_code}:{destination_code}:{departure_date}', value=json.dumps(client_response), expiry_in_seconds=600
                    )
                except Exception as e:
                    print("REDIS EXCEPTION",e)
                return client_response
            else:
                return json.loads(cached_info)
        else:
            print("SINCE NO CACHE THEN FORCE TALK TO AMADEUS")
            client_response = Amadeus.get_from_amadeus(origin=origin_code, destination=destination_code,
                                                       departure_date=departure_date)
            try:
                redisSet = RedisUtil.set_with_expiry(
                    key=f'{origin_code}:{destination_code}:{departure_date}', value=json.dumps(client_response), expiry_in_seconds=600
                )
            except Exception as e:
                print("REDIS EXCEPTION", e)
            return client_response

