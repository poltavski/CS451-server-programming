"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from sys import argv
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging


class ServerPictureHandler(BaseHTTPRequestHandler):
    def _set_response(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'image')
        self.end_headers()

    def do_GET(self):
        try:
            # Always read in binary mode. Opening files in text mode may cause
            # newline translations, making the actual size of the content
            # transmitted *less* than the content-length!
            status_code = 202
            path = self.path.split("path=")[-1]
            f = open(f'./public/{path}', 'rb')
            self._set_response(status_code)
            self.wfile.write(f.read())
        except IOError:
            status_code = 404
            f = open(f'./public/{status_code}.png', 'rb')
            self._set_response(status_code)
            self.wfile.write(f.read())
        logging.info(f"Request: GET, Response: {status_code} Path: {self.path} IP client:{self.client_address[0]}")



    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=ServerPictureHandler, port=8000):
    logging.basicConfig(
        filename="logs.txt",
        filemode='a',
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S',
        level=logging.INFO
    )
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info(f'Server listens on port {port}\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping server\n')


if __name__ == '__main__':
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()