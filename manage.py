import os
import shutil
import site
import traceback

try:
    wsgi_src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wsgi.py')
    for base_dir in site.getsitepackages():
        path = os.path.join(base_dir, 'django/core/handlers/wsgi.py')
        if os.path.exists(path):
            backup_path = path[:-3] + '.bak.py'
            shutil.move(path, backup_path)
            print('mv {} {} ok'.format(path, backup_path))
            shutil.copyfile(wsgi_src_path, path)
            print('cp {} {} ok'.format(wsgi_src_path, path))
        else:
            print('{} not exists'.format(path))
except Exception as e:
    print(e)
    traceback.print_exc()
    exit(1)
