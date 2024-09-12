import os

from flask import Flask, jsonify,request
from dotenv import load_dotenv
from pydantic import ValidationError

from InternalServices.flights_services import FlightsServices
from Pydantic.request_dto import FlightRequestDto
from RedisClient.redis_client import RedisUtil
from TokenManager.token_manager import AmadeusTokenManager
from startup import application_startup

app = Flask(__name__)
load_dotenv()
application_startup()


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "ok",
    })


@app.route('/flights/ping', methods=['GET'])
def service_check():
    return jsonify({"data": "pong"})


@app.route('/flights/price', methods=['GET'])
def get_flights_info():
    query_params = request.args.to_dict()
    try:
        validated_data = FlightRequestDto(**query_params)
    except ValidationError as e:
        errors = [{
            "loc": err.get("loc"),
            "msg": err.get("msg"),
            "type": err.get("type")
        } for err in e.errors()]
        return jsonify({"errors": errors}), 400

    flight_details = FlightsServices.get_flight_info(origin_code=validated_data.originCode,destination_code=validated_data.destinationCode,departure_date=validated_data.date,get_from_cache_flag=validated_data.no_cache)
    return jsonify({"data": flight_details})


# if __name__ == '__main__':
#
#     print("HE>>>>>")
#     print(os.environ.get('PORT'))
#     app.run(debug=True,port=os.environ.get('SERVER_PORT'))
