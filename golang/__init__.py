import os
import subprocess

import portpicker

GO_SERVER_PORT = None


def get_go_program_path():
    if os.name == 'nt':
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'go/bin/main.exe')
    elif os.name == 'posix':
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'go/bin/main')
    else:
        path = None
    return path


def get_go_port():
    global GO_SERVER_PORT
    if not GO_SERVER_PORT:
        GO_SERVER_PORT = portpicker.pick_unused_port()
    return GO_SERVER_PORT


def run_go_server():
    path = get_go_program_path()
    proc = subprocess.Popen([path, str(get_go_port())], close_fds=True)
    print("Go server running on PID {}".format(proc.pid))
    return proc
