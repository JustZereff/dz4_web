import os
import json
import mimetypes
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote_plus
from pathlib import Path
from datetime import datetime


class HttpHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        data = self.rfile.read(int(self.headers.get('Content-Length')))
        self.save_to_json(data)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()
    
    def do_GET(self):
        url = urlparse(self.path)
        match url.path:
            case '/':
                self.send_html_file('index.html')
            case '/message':
                self.send_html_file('message.html')
            case _:
                file_path = Path(url.path[1:])
                if file_path.exists():
                    self.send_statick(str(file_path))
                else:
                    self.send_html_file('error.html', 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as f:
            self.wfile.write(f.read())
        
    def send_statick(self, statick_filename):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header('Content-type', mt[0])
        else:
            self.send_header('Content-type', 'text/plain')
        self.end_headers()
        with open(statick_filename, 'rb') as f:
            self.wfile.write(f.read())
        
    def save_to_json(self, raw_data):
        data = unquote_plus(raw_data.decode())
        time = datetime.now()
        formatted_date_time = time.strftime("%Y-%m-%d %H:%M:%S")
        p_data = {formatted_date_time: {key: value.replace('\n', '').replace('\r', '') for key, value in [el.split('=') for el in data.split('&')]}}
        file_to_json = 'storage/data.json'
        os.makedirs(os.path.dirname(file_to_json), exist_ok=True)
        try:
            with open(file_to_json, 'a', encoding='utf-8') as file_to_json:
                json.dump(p_data, file_to_json)
                file_to_json.write('\n')
        except FileNotFoundError as fnfe:
            print(fnfe)
        
def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == '__main__':
    site_thread = Thread(target=run)
    site_thread.start()
