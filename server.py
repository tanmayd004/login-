from http.server import BaseHTTPRequestHandler, HTTPServer

from urllib.parse import parse_qs

import os

import cgi

import cgitb

import urllib

cgitb.enable()

# Set up session store

SESSION_STORE = {}

class MyRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path.startswith("/home"):

            self._home_page()

        else:

            self._login_page()

    def do_POST(self):

        if self.path.startswith("/login"):

            form = cgi.FieldStorage(

                fp=self.rfile,

                headers=self.headers,

                environ={

                    "REQUEST_METHOD": "POST",

                    "CONTENT_TYPE": self.headers['Content-Type'],

                }

            )

            username = form.getvalue("username")

            password = form.getvalue("password")

            if username == "user" and password == "password":

                session_id = os.urandom(16).hex()

                SESSION_STORE[session_id] = username

                self.send_response(303)

                self.send_header('Location', '/home')

                self.send_header('Set-Cookie', f'session_id={session_id}')

                self.end_headers()

            else:

                self._login_page()

    def _login_page(self):

        self.send_response(200)

        self.send_header("Content-type", "text/html")

        self.end_headers()

        with open("login.html", "rb") as file:

            self.wfile.write(file.read())

    def _home_page(self):

        cookie_header = self.headers.get('Cookie')

        if cookie_header is None:

            self.send_response(303)

            self.send_header('Location', '/login')

            self.end_headers()

            return

        cookie = parse_qs(cookie_header)

        session_id = cookie.get('session_id', [None])[0]

        username = SESSION_STORE.get(session_id, None)

        if username is None:

            self.send_response(303)

            self.send_header('Location', '/login')

            self.end_headers()

            return

        self.send_response(200)

        self.send_header("Content-type", "text/html")

        self.end_headers()

        self.wfile.write(f"<h2>Welcome, {username}!</h2>".encode())

if __name__ == '__main__':

    server_address = ('', 8000)

    httpd = HTTPServer(server_address, MyRequestHandler)

    print('Starting server...')

    httpd.serve_forever()

