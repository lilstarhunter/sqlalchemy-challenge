import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
hawaii_station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(measurement.station, measurement.date, measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    rain = []
    for station, date, prcp in results:
        measurement_dict = {}
        measurement_dict["station"] = station
        measurement_dict["date"] = date
        measurement_dict["prcp"] = prcp
        rain.append(measurement_dict)

    return jsonify(rain)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(hawaii_station.station, hawaii_station.name).all()

    session.close()


    stations_list = []
    for station, name in results:
        stations_dict = {}
        stations_dict["station_id"] = station
        stations_dict["name"] = name
        stations_list.append(stations_dict)

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(measurement.station, measurement.date, measurement.tobs)\
                        .filter(measurement.station == "USC00519397")\
                        .filter(measurement.date >= "2017-01-01")\
                        .all()

    session.close()

    top_tobs = []
    for station, date, tobs in results:
        top_tobs_dict = {}
        top_tobs_dict["station_id"] = station
        top_tobs_dict["date"] = date
        top_tobs_dict["temp"]= tobs
        top_tobs.append(top_tobs_dict)

    return jsonify(top_tobs)




if __name__ == '__main__':
    app.run(debug=True)
