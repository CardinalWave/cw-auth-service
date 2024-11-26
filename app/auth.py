import token
from . import ConnKeycloack
from .utils import generate_token
from .login  import extract_to_login
import jwt
import time

class AuthCredentials:
    def __init__(self, email, password, username):
        self.username = username
        self.email = email
        self.password = password
        self.keycloak_openid = None
        self.keycloak_admin = None
        self.start_conn()

    def start_conn(self):
        connKeycloak = ConnKeycloack()
        time.sleep(5)
        connKeycloak.config_keycloak()
        connKeycloak.get_keycloak_openid = self.keycloak_openid
        connKeycloak.get_keycloak_admin = self.keycloak_admin


def ensure_token_validity(self, token_data):
    try:
        decoded_token = jwt.decode(token_data['access_token'], options={"verify_signature": False})
        exp_time = decoded_token.get('exp', 0)

        if exp_time < time.time():
            print("Token expirado, renovando...")
            new_token = self.keycloak_openid.refresh_token(refresh_token=token_data['refresh_token'])
            return new_token

        return token_data
    except Exception as e:
        raise RuntimeError(f"Erro ao verificar ou renovar o token: {str(e)}")

def ensure_token_validity_admin(self, token_data):
    try:
        decoded_token = jwt.decode(token_data['access_token'], options={"verify_signature": False})
        exp_time = decoded_token.get('exp', 0)

        if exp_time < time.time():
            print("Token expirado, renovando...")
            new_token = self.keycloak_admin.refresh_token(refresh_token=token_data['refresh_token'])
            return new_token

        return token_data
    except Exception as e:
        raise RuntimeError(f"Erro ao verificar ou renovar o token: {str(e)}")
def login(self, credentials: AuthCredentials):
    token = self.keycloak_openid.token(
        username=credentials.email,
        password=credentials.password,
        scope='openid'
    )
    token = ensure_token_validity(token)
    userinfo = self.keycloak_openid.userinfo(token['access_token'])
    return  extract_to_login(userinfo).to_json()


def logout(self, token_data):
    token_data = ensure_token_validity(token_data)
    self.keycloak_openid.logout(token_data['refresh_token'])
    return "Usuário saiu."

def register(self, credentials: AuthCredentials):
    token_unico = generate_token()
    print(token_unico)
    token_admin = ensure_token_validity(self.keycloak_admin.token)
    self.keycloak_admin.create_user({
        "email": credentials.email,
        "username": credentials.username,
        'attributes': {'token_unico': [token_unico]},
        "enabled": True,
        "credentials": [{"value": credentials.password, "type": "password"}]
    })
    return "Registrado com sucesso"

def update_password(self, credentials: AuthCredentials, token_recovery):
    token_admin = ensure_token_validity(self.keycloak_admin.token)
    user_id_dados = self.keycloak_admin.get_user_id(credentials.email)
    dados = self.keycloak_admin.get_user(user_id_dados)
    verify_token = dados.get('attributes', {}).get('token_unico', [])

    if token_recovery == verify_token[0]:
        self.keycloak_admin.set_user_password(user_id_dados, password=credentials.password, temporary=False)
        return "Usuário mudou de senha."
    else:
        return "Token informado está incorreto."
