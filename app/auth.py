import token
from . import keycloak_openid, keycloak_admin
from .utils import generate_token
from .login  import extract_to_login
import jwt
import time

class AuthCredentials:
    def __init__(self, email, password, username):
        self.username = username
        self.email = email
        self.password = password


def ensure_token_validity(token_data):
    try:
        decoded_token = jwt.decode(token_data['access_token'], options={"verify_signature": False})
        exp_time = decoded_token.get('exp', 0)

        if exp_time < time.time():
            print("Token expirado, renovando...")
            new_token = keycloak_openid.refresh_token(refresh_token=token_data['refresh_token'])
            return new_token

        return token_data
    except Exception as e:
        raise RuntimeError(f"Erro ao verificar ou renovar o token: {str(e)}")

def ensure_token_validity_admin(token_data):
    try:
        decoded_token = jwt.decode(token_data['access_token'], options={"verify_signature": False})
        exp_time = decoded_token.get('exp', 0)

        if exp_time < time.time():
            print("Token expirado, renovando...")
            new_token = keycloak_admin.refresh_token(refresh_token=token_data['refresh_token'])
            return new_token

        return token_data
    except Exception as e:
        raise RuntimeError(f"Erro ao verificar ou renovar o token: {str(e)}")
def login(credentials: AuthCredentials):
    token = keycloak_openid.token(
        username=credentials.email,
        password=credentials.password,
        scope='openid'
    )
    token = ensure_token_validity(token)
    userinfo = keycloak_openid.userinfo(token['access_token'])
    return  extract_to_login(userinfo).to_json()


def logout(token_data):
    token_data = ensure_token_validity(token_data)
    keycloak_openid.logout(token_data['refresh_token'])
    return "Usuário saiu."

def register(credentials: AuthCredentials):
    token_unico = generate_token()
    print(token_unico)
    token_admin = ensure_token_validity(keycloak_admin.token)
    keycloak_admin.create_user({
        "email": credentials.email,
        "username": credentials.username,
        'attributes': {'token_unico': [token_unico]},
        "enabled": True,
        "credentials": [{"value": credentials.password, "type": "password"}]
    })
    return "Registrado com sucesso"

def update_password(credentials: AuthCredentials, token_recovery):
    token_admin = ensure_token_validity(keycloak_admin.token)
    user_id_dados = keycloak_admin.get_user_id(credentials.email)
    dados = keycloak_admin.get_user(user_id_dados)
    verify_token = dados.get('attributes', {}).get('token_unico', [])

    if token_recovery == verify_token[0]:
        keycloak_admin.set_user_password(user_id_dados, password=credentials.password, temporary=False)
        return "Usuário mudou de senha."
    else:
        return "Token informado está incorreto."
