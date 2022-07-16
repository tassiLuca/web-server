import sys

from core.server import WebServerAgent

if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8080

server_agent = WebServerAgent()
server_agent.run(port)
