from config.flask_sqlalchemy_init import db


class AirportReachableModel(db.Model):
    __tablename__ = 'airport_reachable'

    airport_id = db.Column(db.SmallInteger, primary_key=True)
    hops = db.Column(db.Integer, default="NULL")