import signal
import socketserver
import sys


class WebServerAgent:
    """
    The agent, i.e. active component, which runs the web server.
    """

    def __init__(self):
        self.server = None

    def run(self, port):
        from core.request_handler import AppRequestHandler
        self.server = socketserver.ThreadingTCPServer(('', port), AppRequestHandler)
        self.server.daemon_threads = True
        self.server.allow_reuse_address = True

        def signal_handler(signal, frame):
            print("Exiting HTTP server")
            try:
                if self.server:
                    self.server.server_close()
            finally:
                sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        try:
            print("[SERVER] Web server active on port " + str(port))
            while True:
                self.server.serve_forever()
        except KeyboardInterrupt:
            pass

        self.server.server_close()

