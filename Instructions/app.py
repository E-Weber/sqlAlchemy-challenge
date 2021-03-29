import numpy as np
import sqlalchemy
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
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]"
    )


@app.route("/precipitation")
def precipiation():
    session = Session(engine)

    """Return a list of all Precipitation"""
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date > "2016-08-22").all()

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
    print("Server received request for 'tobs' page..."),
    return "'tobs' page."


if __name__ == "__main__":
    app.run(debug=True)
