import json
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer
from core.storage import Storage


class GSIServer(HTTPServer):
    def __init__(self, server_address, token, RequestHandler):
        self.auth_token = token
        super(GSIServer, self).__init__(server_address, RequestHandler)


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length).decode('utf-8')

        payload = json.loads(body)
        if not self.authenticate_payload(payload):
            return None

        Storage()['gsi_data'] = payload

        self.send_header('Content-type', 'text/html')
        self.send_response(200)
        self.end_headers()

    def authenticate_payload(self, payload):
        if 'auth' in payload and 'token' in payload['auth']:
            return payload['auth']['token'] == self.server.auth_token
        return False

    def get_round_phase(self, payload):
        if 'round' in payload and 'phase' in payload['round']:
            return payload['round']['phase']
        else:
            return None


class GSIServerManager:
    def __init__(self, server_address, token):
        self.server = GSIServer(server_address, token, RequestHandler)
        self._thread = None

    def start(self):
        self._thread = Thread(target=self.server.serve_forever)
        self._thread.start()

    def stop(self):
        self.server.server_close()
        self._thread.join()
