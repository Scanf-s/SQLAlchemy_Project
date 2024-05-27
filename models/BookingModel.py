from config.flask_sqlalchemy_init import db


class BookingModel(db.Model):
    __tablename__ = 'booking'

    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flight_id = db.Column(db.Integer, nullable=False)
    seat = db.Column(db.CHAR(4))
    passenger_id = db.Column(db.Integer, nullable=False)
    price = db.Column(db.DECIMAL(10, 2), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('flight_id', 'seat', name='seatplan_unq'),
        db.Index('flight_idx', 'flight_id'),
        db.Index('passenger_idx', 'passenger_id'),
    )