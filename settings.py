import subprocess
import sys

print('Django found!')
print('Migrate to pure WSGI.')
subprocess.call([sys.executable, '/app/manage.py'])
print('Finished.')
print('Force exit to restart uWSGI.')
exit(1)
