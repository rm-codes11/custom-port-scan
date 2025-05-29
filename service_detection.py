import socket

def detect_service(target, port, protocol="tcp", timeout=1):
    """Attempt to identify service running on a port"""
    try:
        if protocol == "tcp":
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                s.connect((target, port))
                
                # banner
                try:
                    if port == 80 or port == 443:  # HTTP/HTTPS
                        s.send(b"GET / HTTP/1.0\r\n\r\n")
                        banner = s.recv(1024).decode().strip()
                        return parse_http_banner(banner)
                    else:
                        banner = s.recv(1024).decode().strip()
                        return banner.split('\n')[0] if banner else "No banner"
                except:
                    return guess_service_by_port(port)
        
        elif protocol == "udp":
            # UDP service detection less reliable
            return guess_service_by_port(port)
            
    except Exception as e:
        return f"Error: {str(e)}"

def guess_service_by_port(port):
    """Guess service based on common port numbers"""
    common_services = {
        20: "FTP Data Transfer",
        21: "FTP Control",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        3306: "MySQL",
        3389: "RDP"
    }
    return common_services.get(port, "Unknown service")

def parse_http_banner(banner):
    """Extract server information from HTTP banner"""
    server_info = "HTTP Server"
    for line in banner.split('\n'):
        if line.lower().startswith('server:'):
            server_info = line.split(':', 1)[1].strip()
            break
    return server_info
