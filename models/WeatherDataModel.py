from config.flask_sqlalchemy_init import db


class WeatherDataModel(db.Model):
    __tablename__ = 'weatherdata'

    log_date = db.Column(db.Date, primary_key=True)
    time = db.Column(db.Time, primary_key=True)
    station = db.Column(db.Integer, primary_key=True)
    temp = db.Column(db.DECIMAL(3, 1), nullable=False)
    humidity = db.Column(db.DECIMAL(4, 1), nullable=False)
    airpressure = db.Column(db.DECIMAL(10, 2), nullable=False)
    wind = db.Column(db.DECIMAL(5, 2), nullable=False)
    weather = db.Column(
        db.Enum('Nebel-Schneefall', 'Schneefall', 'Regen', 'Regen-Schneefall', 'Nebel-Regen', 'Nebel-Regen-Gewitter',
             'Gewitter', 'Nebel', 'Regen-Gewitter'))
    winddirection = db.Column(db.SmallInteger, nullable=False)