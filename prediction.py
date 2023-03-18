import tensorflow as tf
import pandas as pd
# import matplotlib.pyplot as plt
from flask_restful import Api, Resource
from sklearn.model_selection import train_test_split
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import MinMaxScaler
import requests as requests
import json
import urllib.parse
import os
from dotenv import load_dotenv;

load_dotenv()

def getLatLongByAddress(address):
    res = requests.get( os.getenv('GEOAPIFY_BASE_URL') + urllib.parse.quote(address, safe='') + "&apiKey=" + os.getenv('GEOAPIFY_API_KEY')).json()
    if res["features"][0]["properties"]["city"] == 'Toronto':
        return [res["features"][0]["geometry"]["coordinates"][1], res["features"][0]["geometry"]["coordinates"][0]]
    else: 
        return "ADDRESS_NOT_IN_TORONTO"

def transformModel(params):
    path_to_model = "./assets/model/toronto_rental_prediction_v2.h5"
    path_to_csv = "./assets/model/Toronto_apartment_rentals_2018.csv"
    model = tf.keras.models.load_model(path_to_model)
    rental = pd.read_csv(path_to_csv)    
    # Create X & y
    X = rental.drop(["Price", "Address"], axis=1)
    y = rental["Price"]
    # data = [2, 1, 0, 43.648861, -79.378033]
    data = params
    columns = ["Bedroom", "Bathroom", "Den", "Lat", "Long"]
    df = pd.DataFrame([data], columns=columns)
    # Create column transformer (this will help us normalize/preprocess our data)
    ct = make_column_transformer(
        (MinMaxScaler(), columns), # get all values between 0 and 1
    )

    # Build our train and test sets (use random state to ensure same split as before)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    # Fit column transformer on the training data only (doing so on test data would result in data leakage)
    ct.fit(X_train)

    # Transform training and test data with normalization (MinMaxScalar) and one hot encoding (OneHotEncoder)
    X_test_normal = ct.transform(df)
    result = model.predict(X_test_normal)        
    return result