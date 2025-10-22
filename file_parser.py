import re


def parse_apache_file(filepath):
    """Reads an Apache log file and returns a dictionary of IP data"""

    # Regex to extract IP and status code
    pattern = re.compile(r'^(\d{1,3}(?:\.\d{1,3}){3})\s.*"\s*(\d{3})\s')

    try:
        # Structure: {ip: {"total": int, "errors": int}}
        log_dict = {}
        with open(filepath, "r") as log:
            for line in log:
                match = pattern.search(line)
                if match:
                    ip = match.group(1)
                    status = match.group(2)

                    if ip not in log_dict:
                        log_dict[ip] = {"total": 0, "errors": 0}

                    log_dict[ip]["total"] += 1

                    # Check for 4xx or 5xx errors
                    if status.startswith(("4", "5")):
                        log_dict[ip]["errors"] += 1

        return log_dict

    except FileNotFoundError:
        print(f"\n[!] ERROR: The file '{filepath}' was not found.\n")
        return None