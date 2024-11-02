import token
from . import keycloak_openid, keycloak_admin
from .utils import generate_token
from .login  import extract_to_login

class AuthCredentials:
    def __init__(self, email, password, username=None):
        self.username = username
        self.email = email
        self.password = password

def login(credentials: AuthCredentials):
    token = keycloak_openid.token(credentials.email, credentials.password, scope='openid')
    userinfo = keycloak_openid.userinfo(token['access_token'])
    return  extract_to_login(userinfo).to_json()


def logout():
    keycloak_openid.logout(token['refresh_token'])
    return f"Usuário saiu."

def register(credentials: AuthCredentials):
    token_unico = generate_token()
    keycloak_admin.create_user({
        "email": credentials.email,
        "username": credentials.username,
        'attributes': {'token_unico': [token_unico]},
        "enabled": True,
        "credentials": [{"value": credentials.password, "type": "password"}]
    })
    return "Registrado com sucesso"

def update_password(credentials: AuthCredentials, token_recovery):
    user_id_dados = keycloak_admin.get_user_id(credentials.email)
    dados = keycloak_admin.get_user(user_id_dados)
    verify_token = dados.get('attributes', {}).get('token_unico', [])

    if token_recovery == verify_token[0]:
        keycloak_admin.set_user_password(user_id_dados, password=credentials.password, temporary=False)
        return "Usuário mudou de senha."
    else:
        return "Token informado está incorreto."
