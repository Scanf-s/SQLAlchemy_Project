from faker import Faker
from faker_airtravel import AirTravelProvider
from flask import Blueprint, abort, render_template, jsonify, request
from flask_login import current_user
from flask_restx import Namespace, Resource
from markupsafe import escape

from config.DatabaseInfo import DatabaseInfo
from config.database_engines import initialize_engine
from util.database_utils import insert_dummy_data, print_table
from util.utils import table_mapper

homepage_blp = Blueprint('HOMEPAGEBLUEPRINT', __name__, url_prefix="/home")
dummy_api = Namespace(name='dummy', path='/api', description='Dummy API')
db_connection_engine, inspector = initialize_engine(db_info=DatabaseInfo())
fake = Faker()
fake.add_provider(AirTravelProvider)


@homepage_blp.route("/")
def home():
    if current_user.is_authenticated:
        return render_template("homepage.html")
    else:
        abort(401)


@dummy_api.route("/dummy/generate", methods=["GET"])
@dummy_api.doc(params={'generate_num': 'Number of dummy data to generate', 'table_name': 'Table name', 'mode': 'y or n. If y, initialize the database before insert'}, responses={200: 'success', 401: 'unauthorized'})
@dummy_api.header('content-type', 'application/json')
class GenerateDummyAPI(Resource):
    @dummy_api.response(200, description="Inserts the specified number of dummy data into the table and returns a success message.")
    def get(self):
        if current_user.is_authenticated:
            generate_num = request.args.get('generate_num')
            table_name = request.args.get('table_name')
            mode = request.args.get('mode')

            if not generate_num or not generate_num.isdigit():
                return jsonify({"error": "Invalid generate_num parameter"}), 400

            if table_name not in table_mapper():
                return jsonify({"error": "Invalid table_name parameter"}), 400

            try:
                dummy_data = table_mapper()[table_name](fake, int(generate_num))
                insert_dummy_data(db_connection_engine, table_name, dummy_data, mode)
                return jsonify(
                    {
                        "status": "success",
                        "message": "Dummy data generated successfully!"
                    }
                ), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        else:
            abort(401)


@dummy_api.route("/show")
@dummy_api.doc(params={'table_name': 'Table name'}, responses={200: 'success', 401: 'unauthorized'})
@dummy_api.header('content-type', 'application/json')
class ShowDummyAPI(Resource):
    @dummy_api.response(200, description="Show specific table's row data")
    def get(self):
        if not current_user.is_authenticated:
            return jsonify({"error": "Unauthorized"}), 401
        else:
            table_name = request.args.get('table_name')
            data = print_table(db_connection_engine, table_name=table_name)
            return jsonify(data)
