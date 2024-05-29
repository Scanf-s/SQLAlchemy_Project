from config.flask_sqlalchemy_init import db


class FlightScheduleModel(db.Model):
    __tablename__ = 'flightschedule'

    flightno = db.Column(db.CHAR(8), primary_key=True)
    from_airport = db.Column(db.SmallInteger, nullable=False)
    to_airport = db.Column(db.SmallInteger, nullable=False)
    departure = db.Column(db.Time, nullable=False)
    arrival = db.Column(db.Time, nullable=False)
    airline_id = db.Column(db.SmallInteger, nullable=False)
    monday = db.Column(db.Integer, default=0)
    tuesday = db.Column(db.Integer, default=0)
    wednesday = db.Column(db.Integer, default=0)
    thursday = db.Column(db.Integer, default=0)
    friday = db.Column(db.Integer, default=0)
    saturday = db.Column(db.Integer, default=0)
    sunday = db.Column(db.Integer, default=0)

    __table_args__ = (
        db.Index('from_idx', 'from_airport'),
        db.Index('to_idx', 'to_airport'),
        db.Index('airline_idx', 'airline_id'),
    )