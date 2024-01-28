import urllib.parse
import os
import json
import mimetypes
import datetime
import socket
import logging
from threading import Thread
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler


BASE_DIR = Path()
FILE_STORAGE = f'{BASE_DIR}/storage/data.json'
SOCKET_HOST = '0.0.0.0'
SOCKET_PORT = 5000


class GoitFramework(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        route = urllib.parse.urlparse(self.path)
        print(route)
        match route.path:
            case '/':
                self.send_html('index.html')
            case '/message':
                self.send_html('message.html')
            case _:
                file = BASE_DIR.joinpath(route.path[1:])
                if file.exists():
                    self.send_static(file)
                else:
                    self.send_html(filename='error.html', status_code=404)

    def do_POST(self):
        size = self.headers.get('Content-Length')
        data = self.rfile.read(int(size))
        print(data)        #b'username=Alona7777&message=ffffff'
        self.send_data_to_socket(data)
        self.send_response(302)
        self.send_header(keyword='Location', value='/')
        self.end_headers()

    def send_data_to_socket(self, data: bytes):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.sendto(data, (SOCKET_HOST, SOCKET_PORT))
        client_socket.close()

    def send_html(self, filename, status_code=200):
        self.send_response(status_code)
        self.send_header(keyword='Content-Tupe', value='text/html')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())

    def send_static(self, filename, status_code=200):
        self.send_response(status_code)
        mime_type, *_ = mimetypes.guess_type(filename)
        if mime_type:
            self.send_header(keyword='Content-Tupe', value=mime_type)
        else:
            self.send_header(keyword='Content-Tupe', value='text/plain')  
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())


def run_server():
    address = ('0.0.0.0', 3000)
    http_server = HTTPServer(address, GoitFramework)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()

def run_socket_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = SOCKET_HOST, SOCKET_PORT
    sock.bind(server)
    try:
        while True:
            data, address = sock.recvfrom(1024)
            print(f'Received data: {data.decode()} from: {address}')
            username, message = data.decode().split('&')
            username = username.split('=')[1]
            message = message.split('=')[1]
            date = str(datetime.datetime.now())   #.strftime('%d/%m/%Y %H:%M:%S')
            print(username, message, date)
            data_dict = {date: {'username': username, 'message': message}}
            save_data_to_json(data_dict)

    except KeyboardInterrupt:
        print(f'Destroy server')
    finally:
        sock.close()


def save_data_to_json(data_dict: dict):
    if os.path.exists(FILE_STORAGE):
        with open(FILE_STORAGE, 'r') as file:
            history = json.load(file)
            history.update(data_dict)
        with open(FILE_STORAGE, 'w') as writer:
            json.dump(history, writer, ensure_ascii=False, indent=4)
    else:
        with open(FILE_STORAGE, 'w') as writer:
            json.dump(data_dict, writer, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')

    server = Thread(target=run_server)
    server.start()

    server_socket = Thread(target=run_socket_server)
    server_socket.start()
