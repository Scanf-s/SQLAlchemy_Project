from config.flask_sqlalchemy_init import db
from sqlalchemy.dialects.mysql import INTEGER


class AirplaneModel(db.Model):
    __tablename__ = 'airplane'

    airplane_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    capacity = db.Column(INTEGER(unsigned=True), nullable=False)
    type_id = db.Column(db.Integer, nullable=False)
    airline_id = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.Index('type_id', 'type_id'),
    )