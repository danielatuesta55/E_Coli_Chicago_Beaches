from .app import db


class Dna(db.Model):
    __tablename__ = 'beach'

    id = db.Column(db.Integer, primary_key=True)
    station_name = db.Column(db.String(250))
    date = db.Column(db.date)
    precipitation = db.Column(db.Float)
    temperature_max = db.Column(db.Float)
    sample_date = db.Column(db.date)
    dna_sample_1_reading = db.Column(db.Float)
    dna_sample_2_reading = db.Column(db.Float)
    dna_reading_mean = db.Column(db.Float)
    water_temperature = db.Column(db.Float)

    def __repr__(self):
        return '<DNA %r>' % (self.station_name)
