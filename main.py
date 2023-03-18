from flask import Flask, jsonify, make_response, request
from flask_restful import Api, Resource
import prediction
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

@app.route('/')
def default():
    return "Flask heroku app"

@app.route('/get-rental-prediction-price', methods=['GET'])
def get_rental_prediction_price():
    bedroom = request.args.get("bedroom")
    bathroom = request.args.get("bathroom")
    den = request.args.get("den")
    address = request.args.get("address")
    coordinates = prediction.getLatLongByAddress(address)
    if (coordinates == "ADDRESS_NOT_IN_TORONTO"):
        return coordinates
    else:
        result = prediction.transformModel([bedroom, bathroom, den, coordinates[0], coordinates[1]])
        return jsonify(str(result))

if __name__ == "__main__":
    app.run(debug=True)
