import socket
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

def udp_scan(target, port, timeout=1):
    """Scan a single UDP port"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(timeout)
            
            # sending empty payload to common UDP services
            if port == 53:  # DNS
                s.sendto(b"\x00", (target, port))
            elif port == 161:  # SNMP
                s.sendto(b"\x00", (target, port))
            else:
                s.sendto(b"", (target, port))
                
            try:
                data, addr = s.recvfrom(1024)
                return port, "open"
            except socket.timeout:
                # UDP is connectionless, so timeout might mean open or filtered
                return port, "open|filtered"
    except Exception as e:
        return port, f"error: {str(e)}"

def udp_scan_ports(target, ports, max_threads=100):
    """Scan multiple UDP ports with threading"""
    open_ports = {}
    
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(udp_scan, target, port): port for port in ports}
        
        for future in concurrent.futures.as_completed(futures):
            port, status = future.result()
            if "open" in status:
                open_ports[port] = {"protocol": "udp", "status": status}
    
    return open_ports
