## A Simple WSGI Application

If you want to implement a really simple thing, you won't like to install django. A simple WSGI application is enough.

This project can be hosted on [Blue King Platform](https://bk.tencent.com/campus/)

[Online Demo](https://wsgi.qcloudapps.com/)

## Files

### myapp.py

This is the main code. You can run it with uWSGI.

```bash
uwsgi --http :9090 --wsgi-file myapp.py
```

### server.py

Only used for development. Don't need to deploy to production server.

Run

```bash
python server.py
```

And you can visit <http://127.0.0.1:8000/>

### wsgi.py

**This is a Hack**

Copy this to `site-packages/django/core/handlers/wsgi.py`, then you can run it with django project settings.

(Only used on Blue King platform)

### manage.py

Copy `wsgi.py` to `django` site packages automatically.

(Only used on Blue King platform)

### settings.py

If project start with django, it will copy `wsgi.py` hack and then let django die. `supervisord` will restart it.

(Only used on Blue King platform. Even may not be used.)

## License

The MIT License (MIT)

Copyright (c) 2018 Ganlv
