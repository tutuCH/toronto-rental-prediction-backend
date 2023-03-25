from flask import Flask, jsonify, make_response, request
from flask_restful import Api, Resource
import prediction
from flask_cors import CORS
import urllib.parse
import os
from dotenv import load_dotenv;

load_dotenv()
app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "https://tutuch.github.io"]}})

@app.route('/')
def default():
    return "Flask heroku app"

@app.route('/get-rental-prediction-price', methods=['GET'])
def get_rental_prediction_price():
    bedroom = request.args.get("bedroom")
    bathroom = request.args.get("bathroom")
    den = request.args.get("den")
    lat = request.args.get("lat")
    long = request.args.get("long")
    try:
        result = prediction.transformModel([bedroom, bathroom, den, lat, long])
        return jsonify(str(result))
    except:
        return "get-rental-prediction-price error"

if __name__ == "__main__":
    app.run(debug=True)
