from entries.request import create_journal_entry, get_entries_by_search
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from entries import get_single_entry
from entries import get_all_entries
from entries import delete_entry
from moods import get_all_moods
from moods import get_single_mood
from entries import create_journal_entry
from entries import get_all_entries
from entries import get_entries_by_search


# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    def parse_url(self, path):
        
        # Just like splitting a string in JavaScript. If the
        # path is "/animals/1", the resulting list will
        # have "" at index 0, "animals" at index 1, and "1"
        # at index 2.
        path_params = path.split("/") # ['', 'animals' , 2]
        resource = path_params[1]
        
        if "?" in resource:
            #What is happening with both the param and the resource being split
            param = resource.split("?")[1]
            resource = resource.split("?")[0]
            pair = param.split("=")
            key = pair[0]
            value = pair[1]

            return (resource, key, value )
        else:
            id = None

        # Try to get the item at index 2
            try:
                # Convert the string "1" to the integer 1
                # This is the new parseInt()
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return (resource, id)  # This is a tuple
    # Here's a class function
    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        self._set_headers(200)
        response = {}  # Default response
        
        parsed = self.parse_url(self.path)
        

        if len(parsed) == 2:
            ( resource, id) = parsed

            if resource == "entries":
                if id is not None:
                    response = f"{get_single_entry(id)}"

                else:
                    response = f"{get_all_entries()}"

            elif resource == "moods":
                if id is not None:
                    response = f"{get_single_mood(id)}"

                else:
                    response = f"{get_all_moods()}"

        elif len(parsed) == 3:
            (resource, key, value ) = parsed

            if key == "q" and resource == "entries":
                response =  f"{get_entries_by_search(value)}"

        self.wfile.write(response.encode())

    def do_DELETE(self):

        self._set_headers(204)

        (resource, id) = self.parse_url(self.path)

        if resource == "entries":
            delete_entry(id)

        self.wfile.write("".encode())    

    def do_POST(self): 
        self._set_headers(201)
        content_len = int(self.headers.get('content-length' , 0))
        post_body = self.rfile.read(content_len)

# This function is not inside the class. It is the starting
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        new_resource = None
        
        if resource == "entries":
            new_resource = create_journal_entry(post_body)

        self.wfile.write(f"{new_resource}".encode())


# point of this application.
def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()
