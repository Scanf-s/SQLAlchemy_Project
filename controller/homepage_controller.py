from faker import Faker
from faker_airtravel import AirTravelProvider
from flask import Blueprint, abort, render_template
from flask_login import current_user
from flask_restx import Namespace

from config.DatabaseInfo import DatabaseInfo
from config.database_engines import initialize_engine

homepage_blp = Blueprint('HOMEPAGEBLUEPRINT', __name__, url_prefix="/home")
dummy_api = Namespace(name='dummy', path='/home/api', description='Dummy API')
db_connection_engine, inspector = initialize_engine(db_info=DatabaseInfo())
fake = Faker()
fake.add_provider(AirTravelProvider)


@homepage_blp.route("/")
def home():
    if current_user.is_authenticated:
        return render_template("homepage.html")
    else:
        abort(401)
        
        
@homepage_blp.route("/home/post_table")
def post_table():
    if current_user.is_authenticated:
        return render_template("post_table.html")
    else:
        abort(401)
        
        
@homepage_blp.route("/home/post_all")
def post_all():
    if current_user.is_authenticated:
        return render_template("post_all.html")
    else:
        abort(401)
