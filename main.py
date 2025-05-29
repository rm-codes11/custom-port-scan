import argparse
from scanner.tcp_scanner import tcp_scan_ports
from scanner.udp_scanner import udp_scan_ports
from scanner.fingerprint import os_fingerprint
from scanner.service_detection import detect_service
from scanner.utils import resolve_hostname, get_common_ports, port_range
from results.json_exporter import export_to_json, create_results_structure

def main():
    parser = argparse.ArgumentParser(description="Advanced Python Port Scanner")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("-p", "--ports", help="Port range (e.g., 1-100) or 'common'", default="common")
    parser.add_argument("-t", "--type", help="Scan type (tcp, udp, all)", choices=["tcp", "udp", "all"], default="tcp")
    parser.add_argument("-o", "--output", help="Output JSON file name")
    parser.add_argument("--threads", help="Number of threads", type=int, default=100)
    args = parser.parse_args()

    try:
        # Resolve target and prepare ports
        target = resolve_hostname(args.target)
        
        if args.ports == "common":
            ports = get_common_ports()
        elif "-" in args.ports:
            start, end = map(int, args.ports.split("-"))
            ports = port_range(start, end)
        else:
            ports = [int(args.ports)]
        
        # Create results structure
        results = create_results_structure(target, list(ports), args.type)
        
        # Perform OS fingerprinting
        results["metadata"]["os_guess"] = os_fingerprint(target)
        print(f"\n[+] OS Guess: {results['metadata']['os_guess']}")
        
        # Perform scanning based on type
        if args.type in ["tcp", "all"]:
            print("\n[+] Starting TCP scan...")
            tcp_results = tcp_scan_ports(target, ports, args.threads)
            for port, data in tcp_results.items():
                data["service"] = detect_service(target, port, "tcp")
                results["results"][port] = data
                print(f"TCP Port {port}: {data['status']} - Service: {data['service']}")
        
        if args.type in ["udp", "all"]:
            print("\n[+] Starting UDP scan...")
            udp_results = udp_scan_ports(target, ports, args.threads)
            for port, data in udp_results.items():
                data["service"] = detect_service(target, port, "udp")
                results["results"][port] = data
                print(f"UDP Port {port}: {data['status']} - Service: {data['service']}")
        
        # Export results
        success, export_info = export_to_json(results, args.output)
        if success:
            print(f"\n[+] Results exported to {export_info}")
        else:
            print(f"\n[-] Failed to export results: {export_info}")
            
    except Exception as e:
        print(f"\n[-] Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
