from flask import Flask, jsonify, make_response, request
from flask_restful import Api, Resource
import tensorflow as tf
import pandas as pd
import prediction
from flask_cors import CORS
# import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import MinMaxScaler

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
    lat = request.args.get("lat")
    long = request.args.get("long")
    result = prediction.transformModel([bedroom, bathroom, den, lat, long])
    return jsonify(str(result))

if __name__ == "__main__":
    app.run(debug=True)
