from flask import Blueprint
from flask import jsonify
import jsonschema

error_handler = Blueprint('error_handler', __name__)


@error_handler.errorhandler(jsonschema.ValidationError)
def on_validation_error(e):
    return jsonify(
        {"status": "error", "statusCode": "6000", "statusDescription": e.message}), 400


@error_handler.errorhandler(Exception)
def global_error():
    return jsonify(
        {"status": "error", "statusCode": "6050", "statusDescription": 'System Error'}), 500
