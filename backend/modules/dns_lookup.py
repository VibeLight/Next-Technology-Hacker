import socket

def dns_lookup(domain):
    try:
        return socket.gethostbyname(domain)
    except Exception as e:
        return str(e)
