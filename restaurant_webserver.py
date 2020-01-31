from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi

from database_setup import Base, Restaurant, MenuItem, engine
from sqlalchemy.orm import sessionmaker


def get_DBSession():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


def add_new_restaurant_name(restaurant_name):
    session = get_DBSession()
    new_restaurant = Restaurant(name=restaurant_name)
    session.add(new_restaurant)
    session.commit()
    return


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

            elif self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                session = get_DBSession()
                restaurants = session.query(Restaurant)

                message = ""
                message += "<html><body>"
                message += "<div><h1><a href='/restaurants/new'>Make A New Restaurant Here</a></h1></div>"
                for restaurant in restaurants:
                    message += "<div>"
                    message += f"<h1>{restaurant.name}</h1>"
                    message += f"<h1><a href='/restaurants/{restaurant.id}/edit'>Edit</a></h1>"
                    message += f"<h1><a href='/restaurants/{restaurant.id}/delete'>Delete</a></h1>"
                    message += "<h1></h1>"
                    message += "</div>"

                message += "</body></html>"
                self.wfile.write(message.encode(encoding='utf-8'))
                print(message)

                return

            elif self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                message = ""
                message += "<html><body>"

                message += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h1>Make a New Restaurant</h1><input name='new_restaurant_name' type='text'><input type='submit' value='Create'></form>"

                message += "</body></html>"
                self.wfile.write(message.encode(encoding='utf-8'))
                print(message)

                return

            elif self.path.endswith("/edit"):
                url = self.path
                url_folders = url.split('/')
                restaurant_id = url_folders[-2]

                session = get_DBSession()
                restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

                if restaurant:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    message = ""
                    message += "<html><body>"

                    message += f"<form method='POST' enctype='multipart/form-data' action='/restaurants/{restaurant.id}/edit'><h1>{restaurant.name}</h1><input name='new_restaurant_name' type='text'><input type='submit' value='Rename'></form>"

                    message += "</body></html>"
                    self.wfile.write(message.encode(encoding='utf-8'))
                    print(message)

                return

            elif self.path.endswith("/delete"):
                url = self.path
                url_folders = url.split('/')
                restaurant_id = url_folders[-2]

                session = get_DBSession()
                restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

                if restaurant:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    message = ""
                    message += "<html><body>"

                    message += f"<form method='POST' enctype='multipart/form-data' action='/restaurants/{restaurant.id}/delete'><h1>Are you sure you want to delete {restaurant.name}</h1><input type='submit' value='Delete'></form>"

                    message += "</body></html>"
                    self.wfile.write(message.encode(encoding='utf-8'))
                    print(message)

                return

        except IOError:
            self.send_error(404, f"File Not Found {self.path}")

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                if ctype == 'multipart/form-data':
                    pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_restaurant_name = fields.get('new_restaurant_name')[0].decode('utf-8')
                    add_new_restaurant_name(new_restaurant_name)

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

                return

            if self.path.endswith("/edit"):
                url = self.path
                url_folders = url.split('/')
                restaurant_id = url_folders[-2]

                session = get_DBSession()
                restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

                if restaurant:

                    ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                    if ctype == 'multipart/form-data':
                        pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
                        fields = cgi.parse_multipart(self.rfile, pdict)
                        new_restaurant_name = fields.get('new_restaurant_name')[0].decode('utf-8')

                        restaurant.name = new_restaurant_name
                        session.add(restaurant)
                        session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

                return

            if self.path.endswith("/delete"):
                url = self.path
                url_folders = url.split('/')
                restaurant_id = url_folders[-2]

                session = get_DBSession()
                restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

                if restaurant:

                    ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                    if ctype == 'multipart/form-data':
                        session.delete(restaurant)
                        session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

                return

            elif self.path.endswith("/hello"):
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

                return

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