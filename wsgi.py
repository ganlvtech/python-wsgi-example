from myapp import application


class WSGIHandler(object):
    def __call__(self, environ, start_response):
        return application(environ, start_response)


def get_wsgi_application():
    return application
