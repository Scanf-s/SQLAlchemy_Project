from config.flask_sqlalchemy_init import db


class AirportModel(db.Model):
    __tablename__ = 'airport'

    airport_id = db.Column(db.SmallInteger, primary_key=True, autoincrement=True)
    iata = db.Column(db.CHAR(3), nullable=False)
    icao = db.Column(db.CHAR(4), nullable=False)
    name = db.Column(db.String(50), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('icao', name='icao_unq'),
        db.Index('name_idx', 'name'),
        db.Index('iata_idx', 'iata'),
    )