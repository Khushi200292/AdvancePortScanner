import ssl
import socket

def get_tls_info(host, port=443):

    try:

        context = ssl.create_default_context()

        with socket.create_connection((host, port), timeout=5) as sock:

            with context.wrap_socket(
                sock,
                server_hostname=host
            ) as ssock:

                cert = ssock.getpeercert()

                return cert

    except OSError:
        return None
