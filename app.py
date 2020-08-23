import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

from datetime import date
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/sawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
m = Base.classes.measurement
s = Base.classes.station
    

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
        "========================<br>"
        f"Available Routes:<br/>"
        "========================<br><br>"
        
        "Precipitation Results<br>"
        f"/api/v1.0/precipitation<br><br>"
         "========================<br><br>"
        "sawaii Stations<br>"
        f"/api/v1.0/stations<br><br>"
        "========================<br><br>"
        f"/api/v1.0/tobs<br/>"
        f"Temperature for most active station<br><br>"
        "========================<br><br>"
        f"/api/v1.0/YYYY-MM-DD<start><br>"
        f"Retrieve summary statistics for eacs station from start date to current<br>"
        f"Replace YYYY-MM-DD wits start date<br><br>"
        
        "========================<br><br>"
        f"/api/v1.0/YYYY-MM-DD<start>/YYYY-MM-DD<end><br>"
        f"Retrieve summary statistics for eacs station from start date to end date<br>"
        f"Replace YYYY-MM-DD wits start date / end date<br>"
    
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    sel = [m.station, s.name, m.date, m.prcp]
    results = session.query(*sel)\
                    .filter(m.station == s.station)\
                    .all()

    session.close()

    rain = []
    for station, name, date, prcp in results:
        rain_dict = {}
        rain_dict["id"] = station
        rain_dict["name"] = name
        rain_dict["date"] = date
        rain_dict["prcp"] = prcp
        rain.append(rain_dict)

    return jsonify(rain)

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    sel =  [s.station, s.name, s.latitude, s.longitude, s.elevation]
    results = session.query(*sel).all()

    session.close()

    stations_list = []
    for station, name, latitude, longitude, elevation in results:
        stations_dict = {}
        stations_dict["id"] = station
        stations_dict["name"] = name
        stations_dict["latitude"] = latitude
        stations_dict["longitude"] = longitude
        stations_dict["elevation"] = elevation
        stations_list.append(stations_dict)

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)
    sel = [m.station, s.name, m.date, m.tobs]
    results = session.query(*sel)\
                        .filter(m.station == s.station)\
                        .filter(m.station == "USC00519397")\
                        .filter(m.date >= "2017-01-01")\
                        .all()

    session.close()

    top_tobs = []
    for station, name, date, tobs in results:
        top_tobs_dict = {}
        top_tobs_dict["station_id"] = station
        top_tobs_dict["name"] = name
        top_tobs_dict["date"] = date
        top_tobs_dict["temp"]= tobs
        top_tobs.append(top_tobs_dict)

    return jsonify(top_tobs)

@app.route("/api/v1.0/<start>")
def query_startdate(start):
    session = Session(engine)

    sel = [m.station,\
         s.name,\
            func.min(m.tobs),\
            func.avg(m.tobs),\
            func.max(m.tobs)]
    results = session.query(*sel)\
                .group_by(m.station)\
                .filter(m.station == s.station)\
                .filter(m.date >= start)\
                .all()
    session.close()

    query_start = []
    for station, name, min_1, avg_1, max_1 in results:
        query_start_dict = {}
        query_start_dict["station_id"] = station
        query_start_dict["name"] = name
        query_start_dict["min_temp"] = min_1
        query_start_dict["avg_temp"] = round(avg_1,0)
        query_start_dict["max_temp"] = max_1
        query_start.append(query_start_dict)

    return jsonify(query_start)

@app.route("/api/v1.0/<start>/<end>")
def query_startend(start, end):
    session = Session(engine)

    sel = [m.station,\
         s.name,\
            func.min(m.tobs),\
            func.avg(m.tobs),\
            func.max(m.tobs)]
    
    results = session.query(*sel)\
                        .group_by(m.station)\
                        .filter(m.date >= start)\
                        .filter(m.date <= end)\
                        .all()

    session.close()

    query = []
    for station, name, min_1, avg_1, max_1 in results:
        query_dict = {}
        query_dict["station_id"] = station
        query_dict["name"] = name
        query_dict["min_temp"] = min_1
        query_dict["avg_temp"] = avg_1
        query_dict["max_temp"] = max_1
        query.append(query_dict)

    return jsonify(query)

if __name__ == '__main__':
    app.run(debug=True)
