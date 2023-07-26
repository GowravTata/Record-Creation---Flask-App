"""
File consisting of all the routes for the API
"""
# Standard Library
import http
from datetime import timedelta

# Third Party Library
from flask import Flask, jsonify, make_response, request
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from swagger_ui import api_doc

# Custom Library
from app.models.exceptions import InvalidPayloadException, RecordExistenceError, RecordInExistenceError
from app.models.record_manager import MongoService

ACCESS_EXPIRES = timedelta(hours=1)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)

api_doc(app, config_path='app/views/swagger.yaml', url_prefix='/docs', title='API doc')

auth = HTTPBasicAuth()


@auth.verify_password
def verify(username, password):
    """
    Method to check the credentials
    """
    credentials = {"admin": "password"}
    if not (username and password):
        return False
    return credentials.get(username) == password


@app.route("/token", methods=["GET"])
@auth.login_required
def login():
    """
    API to get the access token
    """
    access_token = create_access_token(identity="example_user")
    return jsonify(access_token=access_token)


@app.route("/heartbeat")
@auth.login_required
def router():
    """
    API to check the heartrate of the Service
    """
    return "I'm Up", 200


@app.route('/record/<id>', methods=['GET', 'DELETE'])
@app.route('/record', methods=['POST', 'GET', 'PUT'])
@jwt_required()
def route_v1(id=None):
    """
    Method for routing all the services
    """
    try:
        mongo = MongoService()
        if request.method == 'POST':
            payload = request.json
            response = mongo.create_record(payload=payload)
        elif request.method == 'PUT':
            payload = request.json
            response = mongo.update_record(payload=payload)
        elif request.method == 'DELETE':
            response = mongo.delete_record(id=id)
        else:
            response = mongo.fetch_record(id=id)
        return response
    except (KeyError, InvalidPayloadException) as error:
        return make_response(jsonify({'Error': str(error.args[0])}), http.HTTPStatus.BAD_REQUEST)
    except RecordInExistenceError as error:
        return make_response(jsonify({'Error': str(error)}), http.HTTPStatus.NOT_FOUND)
    except RecordExistenceError as error:
        return make_response(jsonify({'Error': str(error)}), http.HTTPStatus.CONFLICT)
    except Exception as error:
        return make_response(jsonify({'Error': str(error)}), http.HTTPStatus.INTERNAL_SERVER_ERROR)
