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

# When user hits the index route, print endpoint instructions.
@app.route("/")
def home():
    return "Welcome to the Hawaii Vacation Prep API!<br><br>\
    Endpoint documentation:<br><br>\
    To use the Hawaii Vacation Prep API, you must have a copy of the hawaii.sqlite database saved in a\
    directory called Resources located in the same directory as this app.py file.<br><br>\
    The Precipitation endpoint returns one year of daily precipitation data in json format:<br>\
    http://localhost:5000//api/v1.0/precipitation<br><br>\
    The Stations endpoint returns a list of weather stations in Hawaii in json format:<br>\
    http://localhost:5000//api/v1.0/stations<br><br>\
    The TOBS endpoint returns one year of temperature observations in Fahrenheit from the most\
    active weather station in json format:<br>\
    http://localhost:5000//api/v1.0/tobs<br><br>\
    The Start endpoint returns the max, min, and average temperature for all days since an input\
    start date in json format:<br>\
    http://localhost:5000//api/v1.0/{start}<br><br>\
    The Start-End endpoint returns the max, min, and average temperature for all days between and\
    including input start and end dates in json format:<br>\
    http://localhost:5000//api/v1.0/{start}{end}"

"""
# When user hits the Precipitation route, query 
@app.route("/api/v1.0/precipitation")
def about():
    return jsonify()

# When user hits the Stations route,
@app.route("/api/v1.0/stations")
def about():
    return jsonify()   

# When user hits the TOBS route,
@app.route("/api/v1.0/tobs")
def about():
    return jsonify()

# When user hits the Start route,
@app.route("/api/v1.0/{start}")
def about():
    return jsonify()

# When user hits the Start-End route,
@app.route("/api/v1.0/{start}{end}")
def about():
    return jsonify() """

if __name__ == "__main__":
    app.run(debug=True)
