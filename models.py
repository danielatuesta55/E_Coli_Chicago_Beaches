from app import db
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
