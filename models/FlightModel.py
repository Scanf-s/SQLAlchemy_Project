from config.flask_sqlalchemy_init import db


class FlightModel(db.Model):
    __tablename__ = 'flight'

    flight_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flightno = db.Column(db.CHAR(8), nullable=False)
    from_airport = db.Column(db.SmallInteger, nullable=False)
    to_airport = db.Column(db.SmallInteger, nullable=False)
    departure = db.Column(db.DateTime, nullable=False)
    arrival = db.Column(db.DateTime, nullable=False)
    airline_id = db.Column(db.SmallInteger, nullable=False)
    airplane_id = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.Index('from_idx', 'from_airport'),
        db.Index('to_idx', 'to_airport'),
        db.Index('departure_idx', 'departure'),
        db.Index('arrivals_idx', 'arrival'),
        db.Index('airline_idx', 'airline_id'),
        db.Index('airplane_idx', 'airplane_id'),
        db.Index('flightno', 'flightno'),
    )