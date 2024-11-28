from flask import Flask
from flask_cors import CORS
from keycloak import KeycloakAdmin, KeycloakOpenID
from .config import Config


class ConnKeycloak:
    def __init__(self) -> None:
        self.__keycloak_openid = None
        self.__keycloak_admin = None
        self.config_keycloak()

    def config_keycloak(self):
        # Configuração do Keycloak
        self.__keycloak_openid = KeycloakOpenID(
            server_url=Config.KEYCLOAK_SERVER_URL,
            client_id=Config.KEYCLOAK_CLIENT_ID,
            realm_name=Config.KEYCLOAK_REALM,
            client_secret_key=Config.KEYCLOAK_SECRET
        )

        self.__keycloak_admin = KeycloakAdmin(
            server_url=Config.KEYCLOAK_SERVER_URL,
            client_id=Config.KEYCLOAK_CLIENT_ID,
            username='admin',
            password='admin',
            realm_name=Config.KEYCLOAK_REALM,
            verify=False,
            client_secret_key=Config.KEYCLOAK_SECRET
        )
    def get_keycloak_openid(self) -> KeycloakOpenID:
        return self.__keycloak_openid

    def get_keycloak_admin(self) -> KeycloakAdmin:
        return self.__keycloak_admin

    def get_secret_keycloak(self):
        return Config.KEYCLOAK_SECRET

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    from .routes import init_routes
    init_routes(app)

    return app
