import json


class LoginAuthenticator:
    """
    A simple class which encapsulates the logic of authentication.
    """

    _LOGIN_FILE = "./data/login.json"

    def __init__(self):
        with open(self._LOGIN_FILE) as login_data:
            json_data = json.load(login_data)
            self.username = json_data["user"]
            self.password = json_data["password"]

    def authenticate(self, username, password):
        return username == self.username and password == self.password
