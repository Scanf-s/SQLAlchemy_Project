from sqlalchemy.dialects.mysql import INTEGER

from config.flask_sqlalchemy_init import db


class FlightLogModel(db.Model):
    __tablename__ = 'flight_log'

    flight_log_id = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    log_date = db.Column(db.DateTime, nullable=False)
    user = db.Column(db.String(100), nullable=False)
    flight_id = db.Column(db.Integer, nullable=False)
    flightno_old = db.Column(db.CHAR(8), nullable=False)
    flightno_new = db.Column(db.CHAR(8), nullable=False)
    from_old = db.Column(db.SmallInteger, nullable=False)
    to_old = db.Column(db.SmallInteger, nullable=False)
    from_new = db.Column(db.SmallInteger, nullable=False)
    to_new = db.Column(db.SmallInteger, nullable=False)
    departure_old = db.Column(db.DateTime, nullable=False)
    arrival_old = db.Column(db.DateTime, nullable=False)
    departure_new = db.Column(db.DateTime, nullable=False)
    arrival_new = db.Column(db.DateTime, nullable=False)
    airplane_id_old = db.Column(db.Integer, nullable=False)
    airplane_id_new = db.Column(db.Integer, nullable=False)
    airline_id_old = db.Column(db.SmallInteger, nullable=False)
    airline_id_new = db.Column(db.SmallInteger, nullable=False)
    comment = db.Column(db.String(200), default="NULL")

    __table_args__ = (
        db.Index('flight_log_ibfk_1', 'flight_id'),
    )
