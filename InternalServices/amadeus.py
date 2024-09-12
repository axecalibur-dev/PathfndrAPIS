import requests
import os

from RedisClient.redis_client import RedisUtil
from TokenManager.token_manager import AmadeusTokenManager

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Amadeus:
    @classmethod
    def get_from_amadeus(cls, origin: str, destination: str, departure_date: str):
        flight_search_url = os.environ.get('AMADEUS_FLIGHT_SEARCH_URL')
        params = {
            'originLocationCode': origin,
            'destinationLocationCode': destination,
            'departureDate': departure_date,
            'adults': 1,
        }

        headers = {
            'Authorization': f'Bearer {AmadeusTokenManager.get_access_token()}',
            'Content-Type': 'application/json'
        }

        logger.info(f'Talking to Amadeus for {origin} to {destination} on {departure_date} for 1 adult.')
        try:
            response = requests.get(flight_search_url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                if not data or 'data' not in data:
                    logger.warning('No flight data found in response.')
                    return {}

                logger.info("Request successful.Calculating cheapest flight options.")
                cheapest_flight = min(data['data'], key=lambda flight: float(flight['price']['total']))
                client_response = {
                    "origin": origin,
                    "destination": destination,
                    "departure_date": departure_date,
                    'price': cheapest_flight['price']['total'],
                }
                return client_response

            elif response.status_code == 401:
                logger.warning("Access token expired. Refreshing token.")
                fresh_token = AmadeusTokenManager.token_refresh(generate_new_token=True)
                RedisUtil.set("access_token", fresh_token)
                headers['Authorization'] = f'Bearer {fresh_token}'
                response = requests.get(flight_search_url, headers=headers, params=params)

                if response.status_code == 200:
                    data = response.json()
                    if not data or 'data' not in data:
                        logger.warning('No flight data found in response after token refresh.')
                        return {}

                    logger.info("Request successful ( TKN RFRSH ) .Calculating cheapest flight options.")
                    cheapest_flight = min(data['data'], key=lambda flight: float(flight['price']['total']))
                    client_response = {
                        "origin": origin,
                        "destination": destination,
                        "departure_date": departure_date,
                        'price': cheapest_flight['price']['total'],
                    }
                    return client_response

                else:
                    logger.error(f"Failed after token refresh: {response.status_code} - {response.text}")
                    return {}

            elif response.status_code == 403:
                logger.error("Authorization failed with Amadeus.")
                return {}

            elif response.status_code == 500:
                logger.error("Something went wrong with Amadeus token.")
                return {}

            else:
                logger.error(f"Unexpected response status code: {response.status_code} - {response.text}")
                return {}

        except requests.RequestException as req_err:
            logger.error(f" A request error has occurred with error message: {req_err}")
            return {}
        except Exception as e:
            logger.error(f"An exception occurred: {e}")
            return {}
