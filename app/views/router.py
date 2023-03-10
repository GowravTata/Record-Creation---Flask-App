import http
import redis
from datetime import timedelta
from flask import Flask, request, make_response, jsonify
from app.models.record_manager import MongoService
from app.models.exceptions import RecordExistenceError, RecordInExistenceError, \
    InvalidPayloadException
from flask_httpauth import HTTPBasicAuth
from swagger_ui import api_doc
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

ACCESS_EXPIRES = timedelta(hours=1)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)

jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)

api_doc(app, config_path='app/views/swagger.yaml', url_prefix='/docs', title='API doc')

auth = HTTPBasicAuth()


# Method to check the credentials
@auth.verify_password
def verify(username, password):
    credentials = {"admin": "password"}
    if not (username and password):
        return False
    return credentials.get(username) == password


# API to get the access token
@app.route("/token", methods=["GET"])
@auth.login_required
def login():
    access_token = create_access_token(identity="example_user")
    return jsonify(access_token=access_token)


@app.route("/heartbeat")
@auth.login_required
def router():
    return "I'm Up", 200


@app.route('/record/<id>', methods=['GET', 'DELETE'])
@app.route('/record', methods=['POST', 'GET', 'PUT'])
#@jwt_required()
def route_v1(id=None):
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
    except (KeyError, InvalidPayloadException) as e:
        return make_response(jsonify({'Error': str(e.args[0])}), http.HTTPStatus.BAD_REQUEST)
    except RecordInExistenceError as e:
        return make_response(jsonify({'Error': str(e)}), http.HTTPStatus.NOT_FOUND)
    except RecordExistenceError as e:
        return make_response(jsonify({'Error': str(e)}), http.HTTPStatus.CONFLICT)
    except Exception as e:
        return make_response(jsonify({'Error': str(e)}), http.HTTPStatus.INTERNAL_SERVER_ERROR)
