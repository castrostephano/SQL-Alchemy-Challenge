# 1. import Flask (makes it a webpage) and other imports
from datetime import datetime
import numpy as np
import os
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from dateutil.relativedelta import relativedelta

#look in the same folder
os.chdir(os.path.dirname(os.path.abspath(__file__)))


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model

base = automap_base()

# reflect the tables

base.prepare(engine, reflect = True)

# Save references to each table
measurement = base.classes.measurement
station = base.classes.station



# 2. Create an app, being sure to pass __name__ _ _ means initalizing a class
app = Flask(__name__)


# 3. Define what to do when a user hits the index route. app is the variable we created. 
# the two underscores tells us where the homepage is
@app.route("/")
def home():
    #List all available api routes
    return (
        f"The available Routes are:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"List of stations: /api/v1.0/stations<br/>"
        f"One year temperature observations: /api/v1.0/tobs<br/>"
        f"Temperature stats from start date: /api/v1.0/yyyy-mm-dd<br/>"
        f"Temperature stats from start to end date: /api/v1.0/yyyy-mm-dd/yyyy-mm-dd<br/>"
    )

     
# 4. Define what to do when a user hits the /about route
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    # sel = [measurement.date, func.avg(measurement.prcp)]
    # results = session.query(*sel).\
    #    group_by(measurement.date).all()
    last_data = session.query(func.max(measurement.date))

    date_time_obj = datetime.strptime(last_data.scalar(),'%Y-%m-%d')
    new_date = date_time_obj + relativedelta(years=-1)
    new_date_string = datetime.strftime(new_date, '%Y-%m-%d').replace(' 0', ' ')


    last_year_prec = session.query(measurement.date,measurement.prcp).\
        filter(measurement.date > new_date_string).all()
    # Terminate session
    session.close()

    # create empty list to store dictionaries
    l = []
    for date, prcp in last_year_prec:
        d = {}
        d["Date"] = date
        d["Precipitation"] = prcp
        l.append(d)

    # Convert list to a JSON object and return
    return jsonify(l)




@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    # Query the station data
    #sel = [Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation]
    #results = session.query(*sel).all()

    scount = session.query(station).count()
    active_stations = session.query(measurement.station,func.count(measurement.id)).\
           group_by(measurement.station).\
              order_by(func.count(measurement.id).desc()).all()


    # Terminate session
    session.close()

    # Convert list to a JSON object and return
    return jsonify(active_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    #copied only for new date string reference, everytime there's a return, 
    #that block of code is enclosed in the ():, which is why we need to bring
    #the code for 'new date string' back here, since it was used in the later query

    last_data = session.query(func.max(measurement.date))

    date_time_obj = datetime.strptime(last_data.scalar(),'%Y-%m-%d')
    new_date = date_time_obj + relativedelta(years=-1)
    new_date_string = datetime.strftime(new_date, '%Y-%m-%d').replace(' 0', ' ')

    high_temp = session.query(measurement.tobs,measurement.date).\
        filter(measurement.station == 'USC00519281').\
            filter(measurement.date>= new_date_string).all()

    # Convert list to a JSON object and return
    return jsonify(high_temp)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)

    start_date = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).\
        filter(measurement.date >= start).all()

    # Terminate session
    session.close()

    start_date = list(np.ravel(start_date))

    # Convert list to a JSON object and return
    return jsonify(start_date)

@app.route("/api/v1.0/<start>/<end>")
def end(start,end):
    session = Session(engine)


    result_data = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()


    # Terminate session
    session.close()

    result_data = list(np.ravel(result_data))

    # Convert list to a JSON object and return
    return jsonify(result_data)



if __name__ == "__main__":
    app.run()