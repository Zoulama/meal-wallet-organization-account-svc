from flask_jsonschema_validator import JSONSchemaValidator
from flask import Flask, jsonify, request, redirect
import swagger
import jsonschema

from src.domain.organization.organization_entity import OrganizationEntity
from src.domain.organization.organization_repository import OrganizationRepository
from src.domain.organization.organization_service import OrganizationService, OrganizationNotFoundException

from src.domain.account.account_entity import AccountEntity
from src.domain.account.account_repository import AccountRepository
from src.domain.account.account_service import AccountService, AccountNotFoundException
from src.infrastructure.storage.database.mongo_db.mongo_client import MongodbClient
import config

from error_handler import error_handler

app = Flask(__name__, static_url_path='/static')
app.register_blueprint(error_handler)

JSONSchemaValidator(app=app, root="schemas")
app.register_blueprint(swagger.swagger_ui_blueprint, url_prefix=swagger.SWAGGER_URL)

mongodb_client = MongodbClient()
mongodb_organization_collection = mongodb_client.organizations
organization_repository = OrganizationRepository(mongodb_organization_collection)
organization_service = OrganizationService(organization_repository)

mongodb_account_collection = mongodb_client.accounts
account_repository = AccountRepository(mongodb_account_collection)
account_service = AccountService(account_repository)


@app.route('/')
def root_url():
    return redirect('/static/docs/redoc.html')


@app.route('/v1/organizations', methods=['POST'])
@app.validate('organization', 'organization_schema')
def create():
    organization_entity = OrganizationEntity.from_json_request(json_request=request.get_json())
    create_organization_response = organization_service.create(organization_entity)
    return jsonify(status='success', data={'meal-walletOrganization': create_organization_response.to_dict()})


@app.route('/v1/organizations', methods=['GET'])
def fetch_all():
    fetch_all_response = organization_service.fetch_all(request.args)
    return jsonify(status='success', data={'meal-walletOrganizations': fetch_all_response.to_dict()})


@app.route('/v1/organizations/<string:organization_id>', methods=['GET'])
def fetch(organization_id: str):
    try:
        fetch_response = organization_service.fetch(organization_id)
        return jsonify(status='success', data={'meal-walletOrganization': fetch_response.to_dict()})
    except OrganizationNotFoundException:
        return jsonify(
            {"status": "fail", "statusCode": "4020", "statusDescription": "meal-wallet organization not found"}), 404

@app.route('/v1/organizations/<string:organization_id>', methods=['PATCH'])
def update(organization_id: str):
    update_response = organization_service.update(organization_id,
                                                  OrganizationEntity.from_json_request(json_request=request.get_json()))
    return jsonify(status='success', data={'meal-walletOrganization': update_response.to_dict()})


@app.route('/v1/accounts', methods=['POST'])
@app.validate('account', 'account_schema')
def create_account():
    account_entity = AccountEntity.from_json_request(json_request=request.get_json())
    create_account_response = account_service.create(account_entity)
    return jsonify(status='success', data={'meal-walletAccount': create_account_response.to_dict()})


@app.route('/v1/accounts', methods=['GET'])
def fetch_all_accounts():
    fetch_all_response = account_service.fetch_all(request.args)
    return jsonify(status='success', data={'meal-walletAccounts': fetch_all_response.to_dict()})


@app.route('/v1/accounts/<string:account_id>', methods=['GET'])
def fetch_account(account_id: str):
    try:
        fetch_response = account_service.fetch(account_id)
        return jsonify(status='success', data={'meal-walletAccount': fetch_response.to_dict()})
    except AccountNotFoundException:
        return jsonify(
            {"status": "fail", "statusCode": "4020", "statusDescription": "meal-wallet account not found"}), 404

@app.route('/v1/accounts/organizations/<string:organization_id>', methods=['GET'])
def fetch_account_by_organization_id(organization_id: str):
    fetch_all_response = account_service.fetch_account_by_organization_id(organization_id)
    return jsonify(status='success', data={'meal-walletAccounts': fetch_all_response.to_dict()})

@app.route('/v1/accounts/<string:account_id>', methods=['PATCH'])
def update_account(account_id: str):
    update_response = account_service.update(account_id,
                                             AccountEntity.from_json_request(json_request=request.get_json()))
    return jsonify(status='success', data={'meal-walletAccount': update_response.to_dict()})


@app.errorhandler(jsonschema.ValidationError)
def on_validation_error(e):
    return jsonify(
        {"status": "error", "statusCode": "6000", "statusDescription": e.message}), 400


@app.errorhandler(Exception)
def global_error(e):
    return jsonify(
        {"status": "error", "statusCode": "6050", "statusDescription": 'System Error'}), 500


if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG_MODE)
