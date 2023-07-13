import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_animals, get_single_animal, get_all_locations, get_single_location, get_all_employees, get_single_employee, get_all_customers, get_single_customer, create_animal, create_location, create_employee, create_customer, delete_animal, delete_location, delete_employee, delete_customer, update_animal, update_location, update_employee, update_customer


# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    def parse_url(self, path):
        """Controls the functionality of any GET, PUT, POST, DELETE requests to the server    """
        # Just like splitting a string in JavaScript. If the
        # path is "/animals/1", the resulting list will
        # have "" at index 0, "animals" at index 1, and "1"
        # at index 2.
        path_params = path.split("/")
        resource = path_params[1]
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

    def do_GET(self):
        """Handles GET requests to the server
        """
        self._set_headers(200)
        response = {}

        (resource, id) = self.parse_url(self.path)

        if resource == "animals":
            if id is not None:
                response = get_single_animal(id)
                if response is None:
                    self._set_headers(404)
                    response = "Not Found"
            else:
                response = get_all_animals()

            self.wfile.write(json.dumps(response).encode())

        if resource == "locations":
            if id is not None:
                response = get_single_location(id)
            else:
                response = get_all_locations()

            self.wfile.write(json.dumps(response).encode())

        if resource == "employees":
            if id is not None:
                response = get_single_employee(id)
            else:
                response = get_all_employees()

            self.wfile.write(json.dumps(response).encode())
        
        if resource == "customers":
            if id is not None:
                response = get_single_customer(id)
            else:
                response = get_all_customers()

            self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        new_animal = None

        if resource == "animals":
            if "name" in post_body and "species" in post_body and "locationId" in post_body and "customerId" in post_body and "status" in post_body:
                self._set_headers(201)
                new_animal = create_animal(post_body)
            else:
                self._set_headers(400)
                new_animal = {
                    "message": f'{"name is required" if "name" not in post_body else ""} {"species is required" if "species" not in post_body else ""} {"locationId is required" if "locationId" not in post_body else ""} {"customerId is required" if "customerId" not in post_body else ""} {"status is required" if "status" not in post_body else ""}'
                }

            self.wfile.write(json.dumps(new_animal).encode())

        new_location = None

        if resource == "locations":
            if "name" in post_body and "address" in post_body:
                self._set_headers(201)
                new_location = create_location(post_body)
            else:
                self._set_headers(400)
                new_location = {
                    "message": f'{"name is required" if "name" not in post_body else ""} {"address is required" if "address" not in post_body else ""}'
                }
            
            self.wfile.write(json.dumps(new_location).encode())

        new_employee = None

        if resource == "employees":
            if "name" in post_body:
                self._set_headers(201)
                new_employee = create_employee(post_body)
            else:
                self._set_headers(400)
                new_employee = {
                    "message": f'{"name is required" if "name" not in post_body else ""}'
                }
            self.wfile.write(json.dumps(new_employee).encode())

        new_customer = None

        if resource == "customers":
            if "name" in post_body:
                self._set_headers(201)
                new_customer = create_customer(post_body)
            else:
                self._set_headers(400)
                new_customer = {
                    "message": f'{"name is required" if "name" not in post_body else ""}'
                }
            self.wfile.write(json.dumps(new_customer).encode())

    # A method that handles any PUT request.
    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        if resource == "animals":
            update_animal(id, post_body)

            self.wfile.write("".encode())

        if resource == "locations":
            update_location(id, post_body)

            self.wfile.write("".encode())

        if resource == "employees":
            update_employee(id, post_body)

            self.wfile.write("".encode())

        if resource == "customers":
            update_customer(id, post_body)

            self.wfile.write("".encode())

    def do_DELETE(self):
    
        (resource, id) = self.parse_url(self.path)

        if resource == "customers":
            self._set_headers(405)
            response = {
            "message": "Contact us directly to delete a customer"
            }
            self.wfile.write(json.dumps(response).encode())
            return

        self._set_headers(204)

        if resource == "animals":
            delete_animal(id)
        elif resource == "locations":
            delete_location(id)  
        elif resource == "employees":
            delete_employee(id)
    
        self.wfile.write("".encode())

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
