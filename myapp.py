import mimetypes
import os
import pprint
import time


def guess_type(path):
    content_type, encoding = mimetypes.guess_type(path)
    if not content_type:
        content_type = 'application/octet-stream'
        with open(path, 'rb') as f:
            data = f.read(4096)
        for i in range(0, 4):
            try:
                if i == 0:
                    data.decode('utf-8')
                else:
                    data[:-i].decode('utf-8')
            except UnicodeDecodeError:
                pass
            else:
                content_type = 'text/plain; charset=utf-8'
                break
    return content_type, encoding


def serve_file(environ, start_response, path):
    if not os.path.exists(path) or not os.path.isfile(path):
        start_response('404 Not Found', [])
        return []

    content_type, encoding = guess_type(path)
    statobj = os.stat(path)
    start_response('200 OK', [
        ('Content-Type', content_type),
        ('Content-Length', str(statobj.st_size)),
    ])
    filelike = open(path, 'rb')
    block_size = 4096
    if 'wsgi.file_wrapper' in environ:
        return environ['wsgi.file_wrapper'](filelike, block_size)
    else:
        return iter(lambda: filelike.read(block_size), '')


def handle_home(environ, start_response):
    links = (
        '/',
        '/environ',
        '/stream',
        '/manage.py',
        '/myapp.py',
        '/server.py',
        '/wsgi.py',
        '/favicon.ico',
        '/static/favicon.ico',
        '/static/favicon.png',
    )
    content = u'<link rel="icon" type="image/png" sizes="16x16" href="/static/favicon.png"><h1>Hello, WSGI!</h1>'
    content += u'<ul>'
    for link in links:
        content += u'<li><a href="{}">{}</a></li>'.format(link, link)
    content += u'</ul>'
    start_response('200 OK', [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(content))),
    ])
    return [content.encode()]


def handle_environ(environ, start_response):
    content = pprint.pformat(environ)
    start_response('200 OK', [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(content))),
    ])
    return [content.encode()]


def handle_stream(environ, start_response):
    start_response('200 OK', [
        ('Content-Type', 'text/event-stream')
    ])
    t0 = time.time()
    while True:
        elapsed = time.time() - t0
        if elapsed > 5:
            break
        yield b'data: {}\n\n'.format(elapsed)
        time.sleep(0.1)


def handle_file(environ, start_response):
    path = environ['PATH_INFO']
    path = path.strip('/')
    path = path.strip('\\')
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    return serve_file(environ, start_response, path)


def application(environ, start_response):
    method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']
    if method == 'GET' and path == '/':
        return handle_home(environ, start_response)
    if method == 'GET' and path == '/environ':
        return handle_environ(environ, start_response)
    if method == 'GET' and path == '/stream':
        return handle_stream(environ, start_response)
    if method == 'GET' and path == '/favicon.ico':
        return serve_file(environ, start_response, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/favicon.ico'))
    return handle_file(environ, start_response)
