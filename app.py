# This app 

# Import dependencies
from flask import Flask
from flask import jsonify

# Create app.
app = Flask(__name__)

# When user hits index route, print all routes.
@app.route("/")
def home():
    print("Welcome to the Hawaii Weather Research API!")
    print("")
    print("Check out the documentation for each endpoint:")
    print("")
    print("The Precipitation endpoint returns a JSON")
    print("/api/v1.0/precipitation")
    print("/api/v1.0/stations")
    print("/api/v1.0/tobs")
    print("/api/v1.0/<start>")
    print("/api/v1.0/<start>/<end>")
    return "Welcome to my 'Home' page!"


# When user hits ___ route,
@app.route("/about")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"

# When user hits ___ route,
@app.route("/about")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"

# When user hits ___ route,
@app.route("/about")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"

# When user hits ___ route,
@app.route("/about")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"

# When user hits ___ route,
@app.route("/about")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"

if __name__ == "__main__":
    app.run(debug=True)
