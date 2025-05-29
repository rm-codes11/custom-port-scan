import socket
from scapy.all import IP, TCP, sr1

def os_fingerprint(target):
    """Attempt to determine remote OS using TCP/IP stack fingerprinting"""
    try:
        # TCP SYN packet
        syn_pkt = IP(dst=target)/TCP(dport=80, flags="S")
        syn_ack = sr1(syn_pkt, timeout=1, verbose=0)
        
        if not syn_ack:
            return "Unknown (no response to SYN)"
        
        # TCP window Size analysis
        window_size = syn_ack[TCP].window
        
        # TCP options analysis
        options = syn_ack[TCP].options
        
        # initial TTL analysis
        ttl = syn_ack[IP].ttl
        
        # OS detection based on common values [needs to be updated~]
        if ttl == 64:
            if window_size == 5840:
                return "Linux (kernel 2.4 or 2.6)"
            elif window_size == 5720:
                return "Google's customized Linux"
        elif ttl == 128:
            if window_size == 65535:
                return "Windows XP/7/8/10"
            elif window_size == 8192:
                return "Windows 95/98"
        elif ttl == 255:
            if window_size == 4128:
                return "Cisco IOS"
        
        return f"Unknown (TTL: {ttl}, Window: {window_size})"
        
    except Exception as e:
        return f"Error in fingerprinting: {str(e)}"
