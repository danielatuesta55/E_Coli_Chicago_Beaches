# import necessary libraries
import os
from datetime import date
import pickle
from flask import (Flask, render_template,jsonify,request,redirect)
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import log, create_engine, func, inspect
from sqlalchemy.sql.expression import all_
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.automap import automap_base

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Database Setup
#################################################
engine = create_engine("postgresql://USERNAME:PASSWORD@localhost:5432/chicago_beaches")

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Save reference to the table
full_result = Base.classes.full_result
prediction = Base.classes.prediction

db = SQLAlchemy(app)

#define classes
class DNA(db.Model):
    __tablename__ = 'full_result'

    id = db.Column(db.Integer, primary_key=True)
    station_name = db.Column(db.String(250))
    r_date = db.Column(db.Date)
    precipitation_inches = db.Column(db.Float)
    max_air_temperature = db.Column(db.Float)
    max_water_temperature = db.Column(db.Float)
    dna_sample_1_reading = db.Column(db.Float)
    dna_sample_2_reading = db.Column(db.Float)
    dna_reading_mean = db.Column(db.Float)
    
    def __repr__(self):
        return '<DNA %r>' % (self.station_name)

class Prediction(db.Model):
    __tablename__ = 'prediction'

    id = db.Column(db.Integer, primary_key=True)
    station_name = db.Column(db.String(250))
    r_date = db.Column(db.Date)
    precipitation_inches = db.Column(db.Float)
    max_air_temperature = db.Column(db.Float)
    max_water_temperature = db.Column(db.Float)
    
    def __repr__(self):
        return '<Prediction %r>' % (self.station_name)

# #################################################
# Flask Routes
# #################################################
# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        id = request.form["id"]
        station_name = "CHICAGO OHARE INTERNATIONAL AIRPORT IL US"
        r_date = date.today()
        precipitation_inches = request.form["precipitation"]
        max_air_temperature = request.form["temperature_max"]
        max_water_temperature = request.form["water_temperature"]
        dna_sample_1_reading = request.form["dna_sample_1_reading"]
        dna_sample_2_reading = request.form["dna_sample_2_reading"]
        dna_reading_mean = (float(dna_sample_1_reading)+float(dna_sample_2_reading))/2

        myobject = DNA(id = id, station_name = station_name, r_date = r_date, 
        precipitation_inches=precipitation_inches,
        max_air_temperature_max=max_air_temperature,
        max_water_temperature=max_water_temperature,
        dna_sample_1_reading=dna_sample_1_reading,
        dna_sample_2_reading=dna_sample_2_reading,dna_reading_mean=dna_reading_mean)

        session.add(myobject)
        session.commit()
        return redirect("#4thPage", code=302)

    return render_template("index.html")

@app.route("/send1", methods=["GET", "POST"])
def send1():
    if request.method == "POST":
        id = request.form["id"]
        station_name = "CHICAGO OHARE INTERNATIONAL AIRPORT IL US"
        r_date = date.today()
        precipitation_inches = request.form["precipitation"]
        max_air_temperature = request.form["temperature_max"]
        max_water_temperature = request.form["water_temperature"]
        
        

        myobject = Prediction(id = id, station_name = station_name, r_date = r_date, 
        precipitation_inches=precipitation_inches,
        max_air_temperature=max_air_temperature,
        max_water_temperature=max_water_temperature)

        session.add(myobject)
        session.commit()
        return redirect("#3rdPage", code=302)

    return render_template("index.html")

if __name__ == "__main__":
    app.run()