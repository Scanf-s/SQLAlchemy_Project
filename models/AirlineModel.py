from config.flask_sqlalchemy_init import db


class AirlineModel(db.Model):
    __tablename__ = 'airline'

    airline_id = db.Column(db.SmallInteger, primary_key=True, autoincrement=True)
    iata = db.Column(db.CHAR(2), nullable=False)
    airlinename = db.Column(db.String(30), default='NULL')
    base_airport = db.Column(db.SmallInteger, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('iata', name='iata_unq'),
        db.Index('base_airport_idx', 'base_airport'),
    )