from . import ConnKeycloak
from .utils import generate_token
from .login import extract_to_login, Login
import jwt
import time

class AuthCredentials:
    def __init__(self, email= None, password= None, username= None, user_token= None):
        self.username = username
        self.email = email
        self.password = password
        self.user_token = user_token

class AuthRequest:

    def __init__(self):
        self.conn_keycloak = ConnKeycloak()
        self.keycloak_openid = self.conn_keycloak.get_keycloak_openid()
        self.keycloak_admin = self.conn_keycloak.get_keycloak_admin()
        self.keycloak_secret = str(self.conn_keycloak.get_secret_keycloak())

    def ensure_token_validity(self, token_data):
        try:
            decoded_token = jwt.decode(token_data['access_token'],
                                       options={"verify_signature": False})
            exp_time = decoded_token.get('exp', 0)

            if exp_time < time.time():
                print("Token expirado, renovando...")
                new_token = (self.keycloak_openid.
                             refresh_token(refresh_token=token_data['refresh_expires_in']))
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
                new_token = (self.keycloak_admin.
                             refresh_token(refresh_token=token_data['refresh_expires_in']))
                return new_token

            return token_data
        except Exception as e:
            raise RuntimeError(f"Erro ao verificar ou renovar o token: {str(e)}")

    def login(self, auth_credentials: AuthCredentials):
        token = self.keycloak_openid.token(
            username=auth_credentials.email,
            password=auth_credentials.password,
            scope='openid'
        )
        token = self.ensure_token_validity(token)
        userinfo = (self.keycloak_openid.userinfo(token['access_token']))
        return  extract_to_login(userinfo).to_json()

    def logout(self, auth_credentials: AuthCredentials):
        token_data = self.ensure_token_validity(auth_credentials.user_token)
        self.keycloak_openid.logout(auth_credentials.user_token)
        return "Usuário saiu."

    def register(self, credentials: AuthCredentials):
        token_unico = generate_token()
        # token_admin = self.ensure_token_validity(self.keycloak_admin.token)
        result_token = self.keycloak_admin.create_user({
            "email": credentials.email,
            "username": credentials.username,
            'attributes': {'token_unico': [token_unico]},
            "enabled": True,
            "credentials": [{"value": credentials.password, "type": "password"}]
        })
        result = Login(token=result_token, username=credentials.username, email=credentials.email)
        return result.to_json()

    def update_password(self, credentials: AuthCredentials, token_recovery):
        token_admin = self.ensure_token_validity(self.keycloak_admin.token)
        user_id_dados = self.keycloak_admin.get_user_id(credentials.email)
        dados = self.keycloak_admin.get_user(user_id_dados)
        verify_token = dados.get('attributes', {}).get('token_unico', [])

        if token_recovery == verify_token[0]:
            self.keycloak_admin.set_user_password(user_id_dados,
                                                              password=credentials.password,
                                                              temporary=False)
            return "Usuário mudou de senha."
        else:
            return "Token informado está incorreto."
