from config.flask_sqlalchemy_init import db


class EmployeeModel(db.Model):
    __tablename__ = 'employee'

    employee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    sex = db.Column(db.CHAR(1))
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    zip = db.Column(db.SmallInteger, nullable=False)
    country = db.Column(db.String(100), nullable=False)
    emailaddress = db.Column(db.String(120))
    telephoneno = db.Column(db.String(30))
    salary = db.Column(db.DECIMAL(8, 2))
    department = db.Column(db.Enum('Marketing', 'Buchhaltung', 'Management', 'Logistik', 'Flugfeld'))
    username = db.Column(db.String(20))
    password = db.Column(db.CHAR(32))

    __table_args__ = (
        db.UniqueConstraint('username', name='user_unq'),
    )