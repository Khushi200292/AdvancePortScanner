import socket

def scan_port(target, port):

    try:
        s = socket.socket()

        s.settimeout(1)

        result = s.connect_ex((target, port))

        s.close()

        return result == 0

    except OSError:
        return False
