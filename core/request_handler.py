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

    _DEFAULT_PAGE = "index.html"
    _ADMIN_PAGE = "admin.html"
    _PAGES_DIR = "./static/"
    _NOT_FOUND_DIR = "./static/not-found.html"

    def __init__(self, request: bytes, client_address: Tuple[str, int], server: socketserver.BaseServer):
        self.login = LoginAuthenticator()
        super().__init__(request, client_address, server)

    def load_html(self):
        sub_path = self.path[1:]
        if sub_path == "":
            sub_path = self._DEFAULT_PAGE
        path = self._PAGES_DIR + sub_path
        if not exists(path):
            path = self._NOT_FOUND_DIR
        self.responde(path)

    def do_GET(self):
        request = self.path
        print("[GET REQUEST] " + request)
        self.load_html()

    def do_POST(self):
        sub_path = self.path[1:]
        post_vars = self.parse_data()
        if sub_path == self._ADMIN_PAGE and post_vars:
            res = self.login.authenticate(post_vars['username'][0], post_vars['password'][0])
            self.responde(self._PAGES_DIR + self._ADMIN_PAGE if res else self._NOT_FOUND_DIR)

    def responde(self, page_path):
        self.send_response(200)
        self.end_headers()
        with open(page_path, 'rb') as file:
            self.wfile.write(file.read())

    def parse_data(self):
        request_type, pdict = parse_header(self.headers['content-type'])
        if request_type == 'multipart/form-data':
            pdict['boundary'] = pdict['boundary'].encode()
            post_data = parse_multipart(self.rfile, pdict)
        elif request_type == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            post_data = parse_qs(self.rfile.read(length).decode())
        else:
            post_data = {}
        return post_data
