import socket

def dns_lookup(target):

    try:
        hostname = socket.gethostbyaddr(target)

        return hostname[0]

    except OSError:
        return "Unknown"
