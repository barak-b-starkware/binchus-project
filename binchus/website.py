from http.server import HTTPServer, BaseHTTPRequestHandler
import re


def create_handler(handlers_dic):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            print(handlers_dic)
            path_pattern = ''
            curr = None
            next = handlers_dic
            partitioned_path = ('root' + self.path).strip('/').split('/')
            for dir in partitioned_path:
                for pattern in next:
                    if re.search(pattern, dir):
                        curr, next = next, next[pattern][1]
                        path_pattern += '/' + pattern
                        break
                else:
                    not_found(self)

            if curr[pattern][0] is None:
                not_found(self)

            get_response_body = curr[pattern][0]
            args = re.search(path_pattern, '/root' + self.path).groups()

            response, body = get_response_body(*args)
            self.send_response(response)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(body, "utf-8"))
    return Handler


def not_found(handler):
    handler.send_response(404)
    handler.send_header("Content-type", "text/html")
    handler.end_headers()


class Website:
    def __init__(self):
        self.handlers_dic = {'root': [None, dict()]}

    def route(self, path):
        partitioned_path = ('root' + path).strip('/').split('/')

        def decorator(f):
            curr = None
            next = self.handlers_dic
            for dir in partitioned_path:
                if dir not in next:
                    next[dir] = [None, dict()]
                curr, next = next, next[dir][1]
            curr[dir][0] = f
            # @functools.wraps(f)
            # def wrapper(*args, **kwargs):
            #     return f(*args, **kwargs)
            # return wrapper
            return f
        return decorator

    def run(self, address):
        with HTTPServer(address, create_handler(self.handlers_dic)) as httpd:
            httpd.serve_forever()


# website = Website()


# @website.route('/')
# def index():
#     return 200, '<html>users list</html>'


# @website.route('/users/([0-9]+)')
# def user(user_id):
#     if user_id not in ['1', '2']:
#         return 404, ''
#     return 200, f'<html>user {user_id}</html>'

# @website.route('/favicon.ico')
# def favicon():
#     return 404, ''

# if __name__ == '__main__':
#     website.run(('127.0.0.1', 8000))
