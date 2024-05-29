from config.flask_sqlalchemy_init import db


class AirportGeoModel(db.Model):
    __tablename__ = 'airport_geo'

    airport_id = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), default="NULL")
    country = db.Column(db.String(50), default="NULL")
    latitude = db.Column(db.DECIMAL(11, 8), nullable=False)
    longitude = db.Column(db.DECIMAL(11, 8), nullable=False)