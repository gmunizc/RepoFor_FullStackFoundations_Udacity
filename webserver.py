from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi


class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                message = b""
                message += b"<html><body>Hello!"
                message += b"<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
                message += b"</body></html>"
                self.wfile.write(message)
                print(message)

                return

            elif self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                message = b""
                message += b"<html><body>&#161Hola! <a href='/hello'>Back to Hello</a>"
                message += b"<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
                message += b"</body></html>"
                self.wfile.write(message)
                print(message)

                return

        except IOError:
            self.send_error(404, f"File Not Found {self.path}")

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            if ctype == 'multipart/form-data':
                pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')[0].decode('utf-8')

            output = ""
            output += "<html><body>"
            output += "<h2> Okay, how about this: </h2>"
            output += f"<h1> {messagecontent} </h1>"
            output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
            output += "</body></html>"
            self.wfile.write(output.encode(encoding='utf-8'))
            print(output)

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print(f"Web server running on port {port}")
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()


if __name__ == '__main__':
    main()