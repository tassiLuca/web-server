import json


class LoginAuthenticator:

    def __init__(self):
        with open("./data/login.json") as login_data:
            json_data = json.load(login_data)
            self.username = json_data["user"]
            self.password = json_data["password"]

    def authenticate(self, username, passowrd):
        return username == self.username and passowrd == self.password
