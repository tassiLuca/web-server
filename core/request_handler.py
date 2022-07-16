import http.server
import socketserver
from os.path import exists
from cgi import parse_header, parse_multipart
from urllib.parse import parse_qs

from typing import Tuple

from core.login import LoginAuthenticator


class AppRequestHandler(http.server.BaseHTTPRequestHandler):
    """
    App HTTP Request Handler
    @see https://docs.python.org/3/library/http.server.html#http.server.BaseHTTPRequestHandler
    """

    def __init__(self, request: bytes, client_address: Tuple[str, int], server: socketserver.BaseServer):
        self.login = LoginAuthenticator()
        super().__init__(request, client_address, server)

    def load_html(self):
        sub_path = self.path[1:]
        if sub_path == "":
            sub_path = "index.html"
        path = "./static/" + sub_path
        if not exists(path):
            path = "./static/not-found.html"
        self.responde(path)

    def do_GET(self):
        request = self.path
        print("[GET REQUEST] " + request)
        self.load_html()

    def do_POST(self):
        sub_path = self.path[1:]
        post_vars = self.parse_data()
        if sub_path == "admin.html" and post_vars:
            res = self.login.authenticate(post_vars['username'][0], post_vars['password'][0])
            self.responde("./static/admin.html" if res else "./static/not-found.html")

    def responde(self, page_path):
        self.send_response(200)
        self.end_headers()
        with open(page_path, 'rb') as file:
            self.wfile.write(file.read())

    def parse_data(self):
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = parse_qs(self.rfile.read(length).decode())
        else:
            postvars = {}
        return postvars
