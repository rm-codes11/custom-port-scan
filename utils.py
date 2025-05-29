import socket
from concurrent.futures import ThreadPoolExecutor

def resolve_hostname(target):
    """Resolve hostname to IP address if needed"""
    try:
        # check if already an IP address
        socket.inet_aton(target)
        return target
    except socket.error:
        try:
            return socket.gethostbyname(target)
        except socket.gaierror:
            raise ValueError(f"Could not resolve hostname: {target}")

def get_common_ports():
    """Return a list of commonly used ports"""
    return [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 
            993, 995, 1723, 3306, 3389, 5900, 8080]

def port_range(start, end):
    """Generate a range of ports"""
    return range(start, end + 1)
