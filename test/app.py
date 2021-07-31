# import necessary libraries
import os
import pandas as pd
import numpy as np
import json
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import all_
from sqlalchemy import log
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func, inspect
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

# from flask_sqlalchemy import SQLAlchemy
app.config['postgresql://postgres:postgres@localhost:5432/test_final_project'] = os.environ.get('postgresql://postgres:postgres@localhost:5432/test_final_project', '') or "sqlite:///db.sqlite"

engine = create_engine("postgresql://postgres:postgres@localhost:5432/test_final_project")
inspector=inspect(engine)
test = inspector.get_table_names()
print(test)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Save reference to the table
Beach = Base.classes.beach

# from .models import Dna
db = SQLAlchemy(app)

class Dna(db.Model):
    __tablename__ = 'beach'

    id = db.Column(db.Integer, primary_key=True)
    station_name = db.Column(db.String(250))
    r_date = db.Column(db.Date)
    precipitation = db.Column(db.Float)
    temperature_max = db.Column(db.Float)
    sample_date = db.Column(db.Date)
    dna_sample_1_reading = db.Column(db.Float)
    dna_sample_2_reading = db.Column(db.Float)
    dna_reading_mean = db.Column(db.Float)
    water_temperature = db.Column(db.Float)

    def __repr__(self):
        return '<DNA %r>' % (self.station_name)

# #################################################
# # Flask Routes
# #################################################

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")


# Query the database and send the jsonified results
@app.route("/send", methods=["GET", "POST"])
def send():
    session = Session(engine)
    if request.method == "POST":
        id = request.form["id"]
        station_name = "CHICAGO OHARE INTERNATIONAL AIRPORT IL US"
        r_date = date.today()
        precipitation = request.form["precipitation"]
        temperature_max = request.form["temperature_max"]
        sample_date = r_date
        dna_sample_1_reading = request.form["dna_sample_1_reading"]
        dna_sample_2_reading = request.form["dna_sample_2_reading"]
        dna_reading_mean = (float(dna_sample_1_reading)+float(dna_sample_2_reading))/2
        water_temperature = request.form["water_temperature"]

        dna = Dna(id=id, station_name=station_name, r_date=r_date, precipitation=precipitation, temperature_max=temperature_max,sample_date=sample_date,dna_sample_1_reading=dna_sample_1_reading,dna_sample_2_reading=dna_sample_2_reading,dna_reading_mean=dna_reading_mean,water_temperature=water_temperature)
        db.session.add(dna)
        db.session.commit()

        print(id,station_name,r_date,precipitation,temperature_max,dna_sample_1_reading,dna_sample_2_reading,dna_reading_mean,water_temperature)
        print(type(r_date))
        return redirect("/", code=302)

    return render_template("form.html")


@app.route("/api/beach")
def beach():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #query the database for data
    results = session.query(Beach.precipitation,Beach.temperature_max,Beach.dna_reading_mean,Beach.water_temperature).all()

    session.close()

    #set variables
    dna_reading_mean = [result[2] for result in results]
    X = [[result[0], result[1],result[3]] for result in results]
    y = np.array(dna_reading_mean).reshape(-1,1)

    #split the data into training and testing
    import xgboost as xgb
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

    from sklearn.preprocessing import StandardScaler

    # Create a StandardScater model and fit it to the training data
    X_scaler = StandardScaler().fit(X_train)
    y_scaler = StandardScaler().fit(y_train)

    # Transform the training and testing data using the X_scaler and y_scaler models
    X_train_scaled = X_scaler.transform(X_train)
    X_test_scaled = X_scaler.transform(X_test)
    y_train_scaled = y_scaler.transform(y_train)
    y_test_scaled = y_scaler.transform(y_test)

    # Create a LinearRegression model and fit it to the scaled training data
    from sklearn.linear_model import LinearRegression
    model = LinearRegression()
    model.fit(X_train_scaled, y_train_scaled)

    # Make predictions using a fitted model
    predictions = model.predict(X_test_scaled)
    model.fit(X_train_scaled, y_train_scaled)

    from sklearn.metrics import mean_squared_error
    MSE = mean_squared_error(y_test_scaled, predictions)

    return jsonify(MSE)


if __name__ == "__main__":
    app.run()
