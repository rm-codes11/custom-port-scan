import socket
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

def tcp_scan(target, port, timeout=1):
    """Scan a single TCP port"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((target, port))
            if result == 0:
                return port, "open"
            return port, "closed"
    except Exception as e:
        return port, f"error: {str(e)}"

def tcp_scan_ports(target, ports, max_threads=100):
    """Scan multiple TCP ports with threading"""
    open_ports = {}
    
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(tcp_scan, target, port): port for port in ports}
        
        for future in concurrent.futures.as_completed(futures):
            port, status = future.result()
            if status == "open":
                open_ports[port] = {"protocol": "tcp", "status": status}
    
    return open_ports
