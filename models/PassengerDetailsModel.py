from config.flask_sqlalchemy_init import db


class PassengerDetailsModel(db.Model):
    __tablename__ = 'passengerdetails'

    passenger_id = db.Column(db.Integer, primary_key=True)
    birthdate = db.Column(db.Date, nullable=False)
    sex = db.Column(db.CHAR(1))
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    zip = db.Column(db.SmallInteger, nullable=False)
    country = db.Column(db.String(100), nullable=False)
    emailaddress = db.Column(db.String(120))
    telephoneno = db.Column(db.String(30))