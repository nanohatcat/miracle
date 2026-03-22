import socket
import os
import json

SOCK = "/tmp/miracle.sock"

def send_state(state):
    try:
        if os.path.exists(SOCK):
            s = socket.socket(socket.AF_UNIX)
            s.connect(SOCK)
            s.send(json.dumps(state).encode())
            s.close()
    except:
        pass
