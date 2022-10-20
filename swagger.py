from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/documentation/swagger'
API_URL = '/static/docs/openapi.yaml'

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "meal-wallet Organization"
    }
)