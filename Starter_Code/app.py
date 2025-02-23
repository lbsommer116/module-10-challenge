# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect,text

from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt

from datetime import datetime
from dateutil.relativedelta import relativedelta


#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect the tables
Base = automap_base()
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
stations_table = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
        
    )

# Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
@app.route("/api/v1.0/precipitation")
def precipitation():

# Perform a query to retrieve the data and precipitation scores
    query = session.query(measurement.date,measurement.prcp).\
        filter(measurement.date >= '2016-08-23')


 # Create a dictionary from the row data and append to a list of all_passengers
    precipitation = []
    for date, prcp in query:
        dict = {}
        dict['date'] = date
        dict['precipitation'] = prcp
        precipitation.append(dict)
    
    return jsonify(precipitation) 

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    
    query = session.query(stations_table.name,stations_table.station)

    station_names = []
    for name,station in query:
        dict2 = {}
        dict2['name'] = name
        dict2['station number'] = station
        station_names.append(dict2)

    return jsonify(station_names)

# Query the dates and temperature observations of the most-active station for the previous year of data.
@app.route("/api/v1.0/tobs")
def popular_station():
    query = session.query(measurement.date,measurement.prcp).\
        filter(measurement.station == 'USC00519281')
    
    popular_station_data = []
    for date, prcp in query:
        dict3 = {}
        dict3['date'] = date
        dict3['precipitation'] = prcp
        popular_station_data.append(dict3)

    return jsonify(popular_station_data)

# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

# Create query
query = session.query(measurement.date,measurement.tobs).all()

# Convert query results to DataFrame
df1 = pd.DataFrame(query, columns = ['date','tobs'])
df1['date'] = pd.to_datetime(df1['date'])
#print(df1.head())

# Start date page
@app.route('/api/v1.0/<start>', methods=['GET'])
def get_temperature_start(start):
    
    # Convert start date to datetime
    start_date = pd.to_datetime(start)
    filtered_data1 = df1[df1['date'] >= start_date]

    # Calculate min, max and average
    min_temp = round(filtered_data1['tobs'].min())
    max_temp = round(filtered_data1['tobs'].max())
    avg_temp = round(filtered_data1['tobs'].mean())

    return jsonify({'Min': min_temp, 'Max': max_temp, 'Avg': avg_temp})

# Start and End date page
@app.route('/api/v1.0/<start>/<end>', methods=['GET'])
def get_temperature_start_end(start, end):
    
    # Convert start date to datetime
    start_date = pd.to_datetime(start)
    end_date = pd.to_datetime(end)
    filtered_data2 = df1[(df1['date'] >= start_date) & (df1['date'] < end_date)]

    # Calculate min, max and average
    min_temp2 = round(filtered_data2['tobs'].min())
    max_temp2 = round(filtered_data2['tobs'].max())
    avg_temp2 = round(filtered_data2['tobs'].mean())

    return jsonify({'Min': min_temp2, 'Max': max_temp2, 'Avg': avg_temp2})

session.close()


if __name__ == '__main__':
    app.run(debug=True)