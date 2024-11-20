from flask import Flask
from flask_cors import CORS
from keycloak import KeycloakAdmin, KeycloakOpenID
from .config import Config

# Configuração do Keycloak
keycloak_openid = KeycloakOpenID(
    server_url=Config.KEYCLOAK_SERVER_URL,
    client_id=Config.KEYCLOAK_CLIENT_ID,
    realm_name=Config.KEYCLOAK_REALM,
    client_secret_key=Config.KEYCLOAK_SECRET
)

keycloak_admin = KeycloakAdmin(
    server_url=Config.KEYCLOAK_SERVER_URL,
    client_id=Config.KEYCLOAK_CLIENT_ID,
    username='admin',
    password='admin',
    realm_name="master-custom",
    verify=True,
    client_secret_key=Config.KEYCLOAK_SECRET
)

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    from .routes import init_routes
    init_routes(app)

    return app
