from config.flask_sqlalchemy_init import db


class PassengerModel(db.Model):
    __tablename__ = 'passenger'

    passenger_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    passportno = db.Column(db.CHAR(9), nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('passportno', name='pass_unq'),
    )