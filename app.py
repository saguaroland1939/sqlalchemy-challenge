# This api returns temperature and precipitation data for Hawaii. This script references a copy of
# the hawaii.sqlite database located in a folder called Resources within the same directory.

# Import dependencies.
from matplotlib import style
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime, timedelta
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify

# Create db engine for sqlite db.
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Create inspector object to view tables and columns in sqlite db.
inspector = inspect(engine)
# Start SQLAlchemy query session for precipitation analysis.
session = Session(engine)
# Create Pandas connection for temperature analysis.
conn = engine.connect()
# Read (reflect) sqlite db into SQLAlchemy Base object.
Base = automap_base()
Base.prepare(engine, reflect = True)
# Create reference to each table in Base.
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create app.
app = Flask(__name__)

# When user hits the index route, print endpoint instructions.
@app.route("/")
def home():
    return "Welcome to the Hawaii Vacation Prep API!<br><br>\
    Endpoint documentation:<br><br>\
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


# When user hits the Precipitation route, query the hawaii.sqlite database and return the prcp column.
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Compute date one year before last date present in database.
    # Query last date in Measurement.
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    # Index into last_date.
    last_date_string = last_date[0]
    # Format string as datetime object.
    format_str = '%Y-%m-%d'
    datetime_obj = dt.datetime.strptime(last_date_string, format_str)
    # Subtract 365 years from datetime object.
    year_ago = datetime_obj - dt.timedelta(days = 365)
    # Get average observed precipitation for each day over last year of data.
    #Because there are multiple readings per day, group data by day and aggregate to average.
    results = session.query(func.min(Measurement.date), func.avg(Measurement.prcp)).\
    filter(Measurement.date >= year_ago).group_by(Measurement.date)
    # Convert session.query object into a dictionary.
    prcp_list = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_list.append(prcp_dict)
    # Convert dictionary to json and return to caller.
    return jsonify(prcp_list)

# When user hits the Stations route, return a list of stations in json format.
@app.route("/api/v1.0/stations")
def stations():
    # Query list of stations from Station table
    result = session.query(Station.station).all()
    normal_list = list(np.ravel(result))
    return jsonify(normal_list)   
"""
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
