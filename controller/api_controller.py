import json

from faker import Faker
from faker_airtravel import AirTravelProvider
from flask import jsonify, request, send_file
from flask_login import current_user
from flask_restx import Namespace, Resource

from config.DatabaseInfo import DatabaseInfo
from config.database_engines import initialize_engine
from util.CustomJSONEncoder import CustomJSONEncoder
from util.database_utils import (
    insert_dummy_data,
    print_table,
    get_view_list_details,
    make_column_details_dictionary,
    get_ddl_script,
    create_all_dummy
)
from util.utils import table_mapper

dummy_api = Namespace(name='dummy', path='/home/api', description='Dummy API')
db_connection_engine, inspector = initialize_engine(db_info=DatabaseInfo())


@dummy_api.route("/generate/table", methods=["GET"])
@dummy_api.doc(params={'generate_num': 'Number of dummy data to generate', 'table_name': 'Table name', 'mode': 'y or n. If y, initialize the database before insert'}, responses={200: 'success', 401: 'unauthorized'})
@dummy_api.header('content-type', 'application/json')
class GenerateDummy(Resource):
    @dummy_api.response(200, description="Inserts the specified number of dummy data into the table and returns a success message.")
    def get(self):
        fake = Faker()
        fake.add_provider(AirTravelProvider)

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
                return jsonify({"success": "Dummy data inserted successfully"})
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        else:
            return jsonify({"error": "Unauthorized"}), 401


@dummy_api.route("/generate/all", methods=["GET"])
@dummy_api.doc(params={'generate_num': 'Number of dummy data to generate', 'table_name': 'Table name', 'mode': 'y or n. If y, initialize the database before insert'}, responses={200: 'success', 401: 'unauthorized'})
@dummy_api.header('content-type', 'application/json')
class GenerateDummyAtOnce(Resource):
    @dummy_api.response(200, description="Inserts the specified number of dummy data into the table and returns a success message.")
    def get(self):
        fake = Faker()
        fake.add_provider(AirTravelProvider)

        if current_user.is_authenticated:
            generate_num = request.args.get('generate_num')
            mode = request.args.get('mode')

            if not generate_num or not generate_num.isdigit():
                return jsonify({"error": "Invalid generate_num parameter"}, 400)

            try:
                create_all_dummy(engine=db_connection_engine, fake=fake, n=int(generate_num), mode=mode)
                return jsonify({"success": "Dummy data inserted successfully"}, 200)
            except Exception as e:
                return jsonify({"error": str(e)}, 500)
        else:
            return jsonify({"error": "Unauthorized"}, 401)


@dummy_api.route("/show/table/data", methods=["GET"])
@dummy_api.doc(params={'table_name': 'Table name'}, responses={200: 'success', 401: 'unauthorized'})
@dummy_api.header('content-type', 'application/json')
class GetDummy(Resource):
    @dummy_api.response(200, description="Show specific table's row data")
    def get(self):
        if not current_user.is_authenticated:
            return jsonify({"error": "Unauthorized"}, 401)
        else:
            table_name = request.args.get('table_name')
            data = print_table(engine=db_connection_engine, table_name=table_name)
            serialized_data = json.loads(json.dumps(data, cls=CustomJSONEncoder))
            return jsonify(serialized_data)


@dummy_api.route("/show/schema/list", methods=["GET"])
@dummy_api.doc(responses={200: 'success', 401: 'unauthorized'})
@dummy_api.header('content-type', 'application/json')
class GetSchemaList(Resource):
    @dummy_api.response(200, description="Show schema list")
    def get(self):
        if not current_user.is_authenticated:
            return jsonify({"error": "Unauthorized"}, 401)
        else:
            return jsonify({"schema_list": inspector.get_schema_names()})


@dummy_api.route("/show/table/list", methods=["GET"])
@dummy_api.doc(responses={200: 'success', 401: 'unauthorized', 400: 'bad request'})
@dummy_api.header('content-type', 'application/json')
class GetTableList(Resource):
    @dummy_api.response(200, description="Show table list")
    def get(self):
        if not current_user.is_authenticated:
            return jsonify({"error": "Unauthorized"}, 401)

        schema_name = request.args.get('schema_name')
        if not schema_name:
            return jsonify({"error": "Schema name is required"}, 400)

        if schema_name not in inspector.get_schema_names():
            return jsonify({"error": "Invalid schema name"}, 400)

        table_list = inspector.get_table_names(schema_name)
        return jsonify({schema_name: table_list})


@dummy_api.route("/show/table/list/detail", methods=["GET"])
@dummy_api.doc(responses={200: 'success', 401: 'unauthorized', 400: 'bad request'})
@dummy_api.header('content-type', 'application/json')
class GetTableListDetail(Resource):
    @dummy_api.response(200, description="Show 'table' details in specified schema")
    def get(self):
        if not current_user.is_authenticated:
            return jsonify({"error": "Unauthorized"}, 401)

        schema_name = request.args.get('schema_name')
        if not schema_name:
            return jsonify({"error": "Schema name is required"}, 400)

        if schema_name not in inspector.get_schema_names():
            return jsonify({"error": "Invalid schema name"}, 400)

        result = []
        tables = inspector.get_table_names(schema_name)
        for table in tables:
            result.append(make_column_details_dictionary(db_connection_engine, inspector, table, DatabaseInfo()))

        return jsonify(
            {
                schema_name: result
            }
        )


@dummy_api.route("/show/view/list", methods=["GET"])
@dummy_api.doc(responses={200: 'success', 401: 'unauthorized', 400: 'bad request'})
@dummy_api.header('content-type', 'application/json')
class GetViewListDetail(Resource):
    @dummy_api.response(200, description="Show 'view' details in specified schema")
    def get(self):
        if not current_user.is_authenticated:
            return jsonify({"error": "Unauthorized"}, 401)

        schema_name = request.args.get('schema_name')
        if not schema_name:
            return jsonify({"error": "Schema name is required"}, 400)

        if schema_name not in inspector.get_schema_names():
            return jsonify({"error": "Invalid schema name"}, 400)

        view_list = inspector.get_view_names(schema_name)
        return jsonify({schema_name: view_list})


@dummy_api.route("/show/view/list/detail", methods=["GET"])
@dummy_api.doc(responses={200: 'success', 401: 'unauthorized', 400: 'bad request'})
@dummy_api.header('content-type', 'application/json')
class GetViewListDetail(Resource):
    @dummy_api.response(200, description="Show view list details")
    def get(self):
        if not current_user.is_authenticated:
            return jsonify({"error": "Unauthorized"}, 401)

        schema_name = request.args.get('schema_name')
        if not schema_name:
            return jsonify({"error": "Schema name is required"}, 400)

        if schema_name not in inspector.get_schema_names():
            return jsonify({"error": "Invalid schema name"}, 400)

        result = get_view_list_details(db_connection_engine, inspector, DatabaseInfo())
        return jsonify(
            {
                schema_name: result
            }
        )


@dummy_api.route("/show/table/details", methods=['GET'])
@dummy_api.doc(responses={200: 'success', 401: 'unauthorized', 400: 'bad request'})
@dummy_api.header('content-type', 'application/json')
class GetTableInformation(Resource):
    @dummy_api.response(200, description="Show table column details, comments")
    def get(self):
        if not current_user.is_authenticated:
            return jsonify({"error": "Unauthorized"}, 401)

        table_name = request.args.get('table_name')

        if not table_name:
            return jsonify({"error": "Schema name is required"}, 400)

        if table_name not in table_mapper().keys():
            return jsonify({"error": "Invalid schema name"}, 400)

        result = [make_column_details_dictionary(db_connection_engine, inspector, table_name, DatabaseInfo())]
        return jsonify(
            {
                table_name: result
            }
        )


@dummy_api.route("/show/table/ddl", methods=['GET'])
@dummy_api.doc(responses={200: 'success', 401: 'unauthorized', 400: 'bad request'})
@dummy_api.header('content-type', 'application/json')
class GetTableDDL(Resource):
    @dummy_api.response(200, description="Show table column details, comments")
    def get(self):

        if not current_user.is_authenticated:
            return jsonify({"error": "Unauthorized"})

        table_name = request.args.get('table_name')

        if not table_name:
            return jsonify({"error": "Schema name is required"})

        if table_name not in table_mapper().keys():
            return jsonify({"error": "Invalid schema name"})

        ddl = get_ddl_script(db_connection_engine, table_name)

        file_path = f"./ddl_tmp/{table_name}.sql"
        with open(file_path, "w") as ddl_file:
            ddl_file.write(str(ddl))

        return send_file(file_path, as_attachment=True, download_name=f"{table_name}.sql")

