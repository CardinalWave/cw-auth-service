#pylint: disable=redefined-builtin
import json

class Login:
    def __init__(self, token: any, email: any, username: any) -> None:
        self.token = token
        self.email = email
        self.username = username

    def to_dict(self):
        return {
            "token": self.token,
            "email": self.email,
            "username": self.username
        }

    def to_json(self):
        return json.dumps(self.to_dict())


def extract_to_login(response) -> Login:

    email = response.get("email")
    token = response.get("sub")
    username = response.get("preferred_username")

    login = Login(token=token, email=email, username=username)
    return login