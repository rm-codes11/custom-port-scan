import json
from datetime import datetime

def export_to_json(scan_results, filename=None):
    """Export scan results to JSON file"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scan_results_{timestamp}.json"
    
    try:
        with open(filename, 'w') as f:
            json.dump(scan_results, f, indent=4)
        return True, filename
    except Exception as e:
        return False, str(e)

def create_results_structure(target, ports, scan_type):
    """Create a structured dictionary for scan results"""
    return {
        "metadata": {
            "target": target,
            "scan_type": scan_type,
            "timestamp": datetime.now().isoformat(),
            "ports_scanned": ports
        },
        "results": {}
    }
