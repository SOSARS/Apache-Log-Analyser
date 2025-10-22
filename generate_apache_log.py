import random
import datetime

# --- Configuration ---
NUM_LOG_LINES = 300
OUTPUT_FILENAME = "access.log"

# --- Data for Generation ---
# A mix of known malicious IPs and some "normal" traffic for contrast
IP_ADDRESSES = [
    # Malicious Actors (weighted to appear more)
    "185.191.205.10", "185.191.205.10", "185.191.205.10",
    "45.9.148.113", "45.9.148.113",
    "103.141.17.15",
    "193.169.252.148",
    "89.248.167.171", "89.248.167.171",

    # "Normal" User Traffic
    "8.8.8.8",  # Google DNS
    "1.1.1.1",  # Cloudflare DNS
    "192.168.1.101"  # A local IP
]

# A mix of normal requests and common malicious scanning patterns
REQUEST_PATHS = [
    # Normal Paths
    "/index.html", "/about.html", "/products/item1", "/static/style.css",

    # Malicious Scanning Paths
    "/.env", "/wp-admin.php", "/phpmyadmin/", "/.git/config", "/etc/passwd",
    "/v2/api-docs", "/owa/auth/logon.aspx"
]


def generate_log_file():
    """Generates a fake but realistic Apache access.log file with malicious traffic."""
    print(f"[*] Generating {NUM_LOG_LINES} log lines into '{OUTPUT_FILENAME}'...")

    malicious_ips = ["185.191.205.10", "45.9.148.113", "103.141.17.15", "193.169.252.148", "89.248.167.171"]

    with open(OUTPUT_FILENAME, "w") as f:
        current_time = datetime.datetime.now()

        for _ in range(NUM_LOG_LINES):
            ip = random.choice(IP_ADDRESSES)

            # If the IP is a known bad guy, make it do bad things
            if ip in malicious_ips:
                path = random.choice(REQUEST_PATHS)  # They might try anything
                status = random.choice(["404", "403", "401"])  # Most scans result in errors
            else:
                # Normal users stick to normal paths and get good status codes
                path = random.choice(["/index.html", "/about.html", "/products/item1"])
                status = random.choice(["200", "302"])

            current_time += datetime.timedelta(seconds=random.randint(1, 15))
            timestamp = current_time.strftime('%d/%b/%Y:%H:%M:%S %z')

            log_line = f'{ip} - - [{timestamp}] "GET {path} HTTP/1.1" {status} {random.randint(100, 4000)}\n'

            f.write(log_line)

    print(f"[+] Done. File '{OUTPUT_FILENAME}' created with known malicious IPs.")


if __name__ == "__main__":
    generate_log_file()