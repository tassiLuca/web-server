import sys

from core.server import WebServerAgent

"""
Usage:
    python3 ./app.py [port_number]

Options:
    port_number     The port number on which http server is listening [default: 8080].
"""

_DEFAULT_PORT = 8080

if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = _DEFAULT_PORT

server_agent = WebServerAgent()
server_agent.run(port)
