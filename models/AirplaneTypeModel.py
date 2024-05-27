from config.flask_sqlalchemy_init import db


class AirplaneTypeModel(db.Model):
    __tablename__ = 'airplane_type'

    type_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    identifier = db.Column(db.String(50))
    description = db.Column(db.Text)

    __table_args__ = (
        db.Index('description_full', 'identifier', 'description', mysql_prefix='FULLTEXT'),
    )