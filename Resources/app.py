import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
#`date` as the key and `prcp` as the val

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates and precipitation measurements"""
    # Query all dates and prcp measurements
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

      # Create a dictionary from the row data and append to a list of all_prcp


    all_prcp = []
    for date, prcp in results:
          prcp_dict = {}
          prcp_dict[date] = prcp
          all_prcp.append(prcp_dict)
  
    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of station IDs and names"""
    # Query all passengers
    session = Session(engine)
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
#query for the dates and temperature observations from a year from the last data point.
#note: last data point is 
#Return a JSON list of Temperature Observations (tobs) for the previous year.

#Define a year from last data point

def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of dates and temps"""
    session = Session(engine)
    tobs_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23').all()

    session.close()

    # Convert list of tuples into normal list
    all_tobs = []
    for date, tobs in tobs_results:
          tobs_dict = {}
          tobs_dict["Date"] = date
          tobs_dict["Temperature"] = tobs
          all_tobs.append(tobs_dict)
  

    return jsonify(all_tobs)


if __name__ == '__main__':
    app.run(debug=True)
