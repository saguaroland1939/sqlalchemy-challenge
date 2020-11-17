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
from flask import Flask, jsonify, request

# Create db engine for sqlite db.
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Read (reflect) sqlite db into SQLAlchemy Base object.
Base = automap_base()
Base.prepare(engine, reflect = True)
# Create reference to each table in Base.
Station = Base.classes.station
Measurement = Base.classes.measurement

# This function, called `start_temps` accepts a start date in the format '%Y-%m-%d' 
# and returns the max, min, and average temperatures for all dates in the Measurement
# table since the start date.
def start_temps(date):
    # Start SQLAlchemy query session.
    session = Session(engine)
    return session.query(func.max(Measurement.tobs), func.min(Measurement.tobs),\
    func.avg(Measurement.tobs)).filter(Measurement.date >= date).all()
    session.close()
   
# This function, called `start_end_temps` accepts start and end dates in the format '%Y-%m-%d' 
# and returns the max, min, and average temperatures for all observations in the Measurement
# table that fall within the date range.
def start_end_temps(start_date, end_date):
    # Start SQLAlchemy query session.
    session = Session(engine)
    return session.query(func.max(Measurement.tobs), func.min(Measurement.tobs),\
    func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).\
    filter(Measurement.date <= end_date).all()
    session.close()

# Create app.
app = Flask(__name__)

# When user hits the index route, print endpoint instructions.
@app.route("/")
def home():
    return "Welcome to the Hawaii Vacation Prep API!<br><br>\
    Endpoint documentation:<br><br>\
    The Precipitation endpoint returns one year of daily precipitation data in inches in json format:\
    <br>http://localhost:5000//api/v1.0/precipitation<br><br>\
    The Stations endpoint returns a list of weather stations in Hawaii in json format:<br>\
    http://localhost:5000//api/v1.0/stations<br><br>\
    The TOBS endpoint returns one year of temperature observations in Fahrenheit from the most\
    active weather station in json format:<br>\
    http://localhost:5000//api/v1.0/tobs<br><br>\
    The Start endpoint returns the max, min, and average temperature for all days since an input\
    start date (YYYY-MM-DD) in json format:<br>\
    http://localhost:5000//api/v1.0/<startdate><br><br>\
    The Start-End endpoint returns the max, min, and average temperature for all days between and\
    including input start and end dates (YYYY-MM-DD) in json format:<br>\
    http://localhost:5000//api/v1.0/<startdate>/<enddate>"

# When user hits the Precipitation route, query the hawaii.sqlite database and return the prcp column.
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Compute date one year before last date present in database.
    # Start SQLAlchemy query session.
    session = Session(engine)
    # Query last date in Measurement.
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    session.close()
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

# When user hits the stations route, return a list of stations in json format.
@app.route("/api/v1.0/stations")
def stations():
    # Query list of stations from Station table
    # Start SQLAlchemy query session.
    session = Session(engine)
    result = session.query(Station.station).all()
    session.close()
    normal_list = list(np.ravel(result))
    return jsonify(normal_list)   

# When user hits the temperature route, return one year of temperature observations from
# station with the most observations in json format.
@app.route("/api/v1.0/tobs")
def temperature():
    # Compute date one year before last date present in database.
    # Start SQLAlchemy query session.
    session = Session(engine)
    # Query last date in database.
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    session.close()
    # Index into last_date.
    last_date_string = last_date[0]
    # Format string as datetime object.
    format_str = '%Y-%m-%d'
    datetime_obj = dt.datetime.strptime(last_date_string, format_str)
    # Subtract 365 years from datetime object.
    year_ago = datetime_obj - dt.timedelta(days = 365)
    # Find the station with the most measurements by grouping the Measurement table by station, 
    # aggregating to count, and sorting descending. This station should provide the most reliable
    # information about Hawaii weather.
    # Start SQLAlchemy query session.
    session = Session(engine)
    # Query
    result = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    session.close()
    # Extract first cell of first row.
    highest_number = result[0][0]
    # For the station with the most observations, query the last year of temperature data.
    results = session.query(Measurement.tobs).filter(Measurement.station == highest_number).\
    filter(Measurement.date >= year_ago).all()
    session.close()
    normal_list = list(np.ravel(results))
    return jsonify(normal_list)

# When user hits the Start, return temperature stats based on user input timespan\
#(start date --> last date in table).
@app.route("/api/v1.0/<date>")
def start(date):
    # Call start_temps function with user input start date to get temp stats.
    stats = start_temps(date)
    # Convert session.query object into a "normal" list.
    normal_list = list(np.ravel(stats))
    return jsonify(normal_list)

# When user hits the Start-End route,
@app.route("/api/v1.0/<startdate>/<enddate>")
def start_end(startdate, enddate):
    # Call start_end_temps function with user input start and end dates to get temp stats.
    stats = start_end_temps(startdate, enddate)
    # Convert session.query object into a "normal" list.
    normal_list = list(np.ravel(stats))
    return jsonify(normal_list)

if __name__ == "__main__":
    app.run(debug=True)
