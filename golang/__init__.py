import os
import subprocess


def get_go_program_path():
    if os.name == 'nt':
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'go/bin/main.exe')
    elif os.name == 'posix':
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'go/bin/main')
    else:
        path = None
    return path


def run_go_server():
    path = get_go_program_path()
    proc = subprocess.Popen([path], close_fds=True)
    print("Go server running on PID {}".format(proc.pid))
    return proc
