import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# Flask Routes
@app.route("/")
def home():

    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]"
    )


@app.route("/precipitation")
def precipiation():
    session = Session(engine)

    """Return a list of all Precipitation"""
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


@app.route("/stations")
def stations():
    session = Session(engine)

    """Return a list of all stations"""
    results = session.query(station.station).\
        order_by(station.station).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/tobs")
def tobs():
    session = Session(engine)

    """Return a list of all tobs"""
    results = session.query(measurement.date, measurement.prcp, measurement.tobs).\
        filter(measurement.date > "2016-08-22").\
        filter(measurement.station == "USC00519281").\
        order_by(measurement.date).all()

    session.close()

    all_tobs = []
    for date, prcp, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_dict["prcp"] = prcp
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)


@app.route("/start")
def start_date():

    session = Session(engine)
    start = '2016-08-23'

    """Return a list of all min, avg, and max for a start date"""
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start)

    session.close()

    start_tobs = []
    for min, avg, max in results:
        start_tobs_dict = {}
        start_tobs_dict["min_temp"] = min
        start_tobs_dict["avg_temp"] = avg
        start_tobs_dict["max_temp"] = max
        start_tobs.append(start_tobs_dict)

    return jsonify(start_tobs)


if __name__ == "__main__":
    app.run(debug=True)
