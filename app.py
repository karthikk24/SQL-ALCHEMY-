import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime
from flask import Flask, jsonify

#Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite",connect_args={'check_same_thread': False}, echo=True)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """List all available  routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
# Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Convert the query results to a Dictionary using date as the 'key 'and 'prcp' as the value."""
    results = session.query(Measurement.date, Measurement.prcp).\
                        order_by(Measurement.date).all()

    # Create a dictionary from the row data and append to a list of for the precipitation data
    preci_data = []
    for x in results:
        x_dict = {}
        x_dict["Date"] = x.date
        x_dict["Precipitation"] = x.prcp
        preci_data.append(x_dict)
        
    return jsonify(preci_data)


# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    """Return a json list of stations from the dataset."""
    # Query all stations
    results = session.query(Station).all()

    # Create a dictionary from the row data and append to a list of all stations
    stations = []
    for x in results:
        stations_dict = {}
        stations_dict["Station"] = x.station
        stations_dict["Station Name"] = x.name
        stations_dict["Latitude"] = x.latitude
        stations_dict["Longitude"] = x.longitude
        stations_dict["Elevation"] = x.elevation
        stations.append(stations_dict)
    
    return jsonify(stations)

# query for the dates and temperature observations from a year from the last data point.
# Return a JSON list of Temperature Observations (tobs) for the previous year.
# last data date 8/23/2017

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of Temperature Observations (tobs) for the previous year"""
    # Query all the stations and for the Temperature Observations for the previous year. 
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
                    group_by(Measurement.date).\
                    filter(Measurement.date > 23-8-2016).\
                    order_by(Measurement.station).all()
                    
    # Create a dictionary from the row data and append to a list of for the temperature data.
    temp = []
    for x in results:
        tobs_dict = {}
        tobs_dict["Station"] = x.station
        tobs_dict["Date"] = x.date
        tobs_dict["Temperature"] = x.tobs
        temp.append(tobs_dict)
    
    return jsonify(temp)



if __name__ == '__main__':
    app.run(debug=True)
