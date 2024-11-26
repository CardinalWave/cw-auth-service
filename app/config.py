import os
from dotenv import load_dotenv

# configs .env
load_dotenv()


class Config:
    # config Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')

    # config do Keycloak
    KEYCLOAK_SERVER_URL = os.getenv('KEYCLOAK_SERVER_URL', 'http://172.17.0.1:5010/auth/')
    KEYCLOAK_REALM = os.getenv('KEYCLOAK_REALM', 'master-custom')
    KEYCLOAK_CLIENT_ID = os.getenv('KEYCLOAK_CLIENT_ID', 'PythonClient')
    KEYCLOAK_SECRET = os.getenv('KEYCLOAK_SECRET', 'zHi88ski3ur7hDgWQaaRS9jB2UMi0rOt')

    # admin Keycloak
    KEYCLOAK_ADMIN_USERNAME = os.getenv('KEYCLOAK_ADMIN_USERNAME', 'admin')
    KEYCLOAK_ADMIN_PASSWORD = os.getenv('KEYCLOAK_ADMIN_PASSWORD', 'admin')
