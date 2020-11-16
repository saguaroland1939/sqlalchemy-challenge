# This app 

# Import dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Create app.
app = Flask(__name__)

# When user hits index route, print endpoint instructions.
@app.route("/")
def home():
    return "Welcome to the Hawaii Vacation Prep API!<br><br>\
    Endpoint documentation:<br><br>\
    The Precipitation endpoint returns one year of daily precipitation data in json format:<br>\
    /api/v1.0/precipitation<br><br>\
    The Stations endpoint returns a list of weather stations in Hawaii in json format:<br>\
    /api/v1.0/stations<br><br>\
    The TOBS endpoint returns one year of temperature observations in Fahrenheit from the most active weather station in json format:<br>\
    /api/v1.0/tobs<br><br>\
    The Start endpoint returns the max, min, and average temperature for all days since an input start date in json format:<br>\
    /api/v1.0/{start}<br><br>\
    The Start-End endpoint returns the max, min, and average temperature for all days between and including input start and end dates in json format:<br>\
    /api/v1.0/{start}{end}"

"""
# When user hits /api/v1.0/precipitation route,
@app.route("/about")
def about():
    return jsonify()

# When user hits /api/v1.0/stations route,
@app.route("/about")
def about():
    return jsonify()   

# When user hits /api/v1.0/tobs route,
@app.route("/about")
def about():
    return jsonify()

# When user hits /api/v1.0/{start} route,
@app.route("/about")
def about():
    return jsonify()

# When user hits /api/v1.0/{start}{end} route,
@app.route("/about")
def about():
    return jsonify() """

if __name__ == "__main__":
    app.run(debug=True)
