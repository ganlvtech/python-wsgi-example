import cgi
import mimetypes
import os
import pprint
import time
import traceback
import urlparse

import wsgi_proxy


def get_upload_dir():
    path_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'USERRES')
    if not os.path.exists(path_dir):
        os.makedirs(path_dir, mode=0755)
    return path_dir


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
        '/hello',
        '/upload',
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


def handle_upload_get(environ, start_response):
    content = u'''
<form method="post" enctype="multipart/form-data">
    <p><input type="file" name="file"></p>
    <p><button type="submit">Upload</button></p>
</form>
<ul>
'''
    for filename in os.listdir(get_upload_dir()):
        content += u'''
<li>
    <a href="/USERRES/{}">{}</a>
    <a href="/upload/delete?filename={}">Delete</a>
</li>
'''.format(filename, filename, filename)
    content += u'</ul>'
    content = content.encode()
    start_response('200 OK', [
        ('Content-Type', 'text/html; charset=UTF-8'),
        ('Content-Length', str(len(content))),
    ])
    return [content]


def handle_upload_post(environ, start_response):
    try:
        fields = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
    except Exception as e:
        traceback.print_exc()
        content = e.message
        content = content.encode()
        start_response('500 Internal Server Error', [
            ('Content-Type', 'text/plain; charset=UTF-8'),
            ('Content-Length', str(len(content))),
        ])
        return [content]

    if 'file' not in fields:
        content = u'No file provided.'
        content = content.encode()
        start_response('400 Bad Request', [
            ('Content-Type', 'text/plain; charset=UTF-8'),
            ('Content-Length', str(len(content))),
        ])
        return [content]

    file_item = fields['file']
    if not isinstance(file_item, cgi.FieldStorage):
        content = u'Field "file" is not a file or contains multiple files.'
        content = content.encode()
        start_response('400 Bad Request', [
            ('Content-Type', 'text/plain; charset=UTF-8'),
            ('Content-Length', str(len(content))),
        ])
        return [content]

    path = os.path.join(get_upload_dir(), os.path.basename(file_item.filename))
    with open(path, 'wb') as f:
        f.write(file_item.file.read())

    content = u'The file was uploaded successfully.'
    content = content.encode()
    start_response('200 OK', [
        ('Content-Type', 'text/plain; charset=UTF-8'),
        ('Content-Length', str(len(content))),
    ])
    return [content]


def handle_upload_delete(environ, start_response):
    query = urlparse.parse_qs(environ['QUERY_STRING'])
    if 'filename' in query:
        filename = query['filename'][0]
        filename = os.path.basename(filename)
        path = os.path.join(get_upload_dir(), filename)
        if os.path.exists(path) and os.path.isfile(path):
            os.unlink(path)

    content = u'The file was deleted.'
    content = content.encode()
    start_response('200 OK', [
        ('Content-Type', 'text/plain; charset=UTF-8'),
        ('Content-Length', str(len(content))),
    ])
    return [content]


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
    if method == 'GET' and path == '/upload':
        return handle_upload_get(environ, start_response)
    if method == 'POST' and path == '/upload':
        return handle_upload_post(environ, start_response)
    if method == 'GET' and path == '/upload/delete':
        return handle_upload_delete(environ, start_response)
    if method == 'GET' and path == '/hello':
        environ['HTTP_HOST'] = '127.0.0.1:8003'
        environ['wsgi.url_scheme'] = 'http'
        return wsgi_proxy.app(environ, start_response)
    return handle_file(environ, start_response)
