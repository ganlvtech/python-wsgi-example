from wsgiref.simple_server import make_server

from wsgi import WSGIHandler

application = WSGIHandler()

httpd = make_server('', 8000, application)
print('Serving HTTP on port 8000...')

httpd.serve_forever()
