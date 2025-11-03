import random
import datetime
import csv


# --- CONFIGURATION ---
OUTPUT_FILE = "test_access.log"
GROUND_TRUTH_FILE = "ground_truth_labels.csv"

# Attack IPs
ATTACKER_IPS = [
    "203.45.12.78",   # Credential stuffer
    "198.51.100.42",  # Credential stuffer (slower)
    "185.199.108.15", # Recon scanner
]

# Legitimate IPs
LEGIT_IPS = [
    "192.168.1.50", "10.0.0.15", "172.16.0.20", "192.168.1.100", "10.0.0.25",
    "172.16.10.30", "192.168.0.12", "10.0.5.88", "172.17.0.101", "192.168.1.204",
    "10.1.1.5", "172.18.50.2", "192.168.100.10", "10.50.20.30", "172.19.1.1",
    "192.168.2.111", "10.10.10.10", "172.20.15.5", "192.168.0.75", "10.0.0.199"
]


def generate_credential_stuffing(attacker_ip, start_time):
    """Generate a credential stuffing attack pattern"""
    logs = []
    paths = ["/login", "/signin", "/auth/login"]

    current_time = start_time

    for index in range(1000):
        # Choose a random path
        path = random.choice(paths)

        if random.random() < 0.95:
            status = random.choice(["401", "403"])
        else:
            status = "200"

        # Generate requests that are 1-3 seconds apart
        current_time += datetime.timedelta(seconds=random.randint(1, 3))
        timestamp = current_time.strftime("%d/%b/%Y:%H:%M:%S ")

        # Build the log line
        bytes_sent = random.randint(100, 500)
        log_line = f'{attacker_ip} - - [{timestamp}] "POST {path} HTTP/1.1" {status} {bytes_sent}'

        logs.append(log_line)

    return logs


def generate_recon_scan(attacker_ip, start_time):
    """Generate a reconnaissance scan pattern"""
    scan_paths = [
        "/.env", "/.git/config", "/.aws/credentials", "/.htpasswd", "/.bash_history", "/.ssh/id_rsa",
        "/admin", "/administrator/", "/phpmyadmin/", "/cpanel", "/dashboard/", "/manage/", "/portal/",
        "/wp-admin/", "/wp-login.php", "/wp-config.php", "/xmlrpc.php", "/config.php", "/web.config",
        "/appsettings.json", "/database.yml", "/local.xml", "/secrets.yml", "/credentials.json",
        "/backup.sql", "/dump.sql", "/db.sql", "/data.sql", "/backup.zip", "/site.zip", "/backup.tar.gz",
        "/access.log", "/error.log", "/debug.log", "/app.log", "/old/", "/temp/", "/tmp/", "/test/",
        "/.svn/entries", "/Jenkinsfile", "/.gitlab-ci.yml", "/.travis.yml", "/Dockerfile",
        "/api/", "/api/v1/", "/swagger-ui.html", "/api-docs/", "/graphql", "/swagger.json", "/redoc",
        "/info.php", "/phpinfo.php", "/test.php", "/shell.php", "/crossdomain.xml", "/robots.txt",
        "/server-status", "/actuator/env", "/actuator/health", "/WEB-INF/web.xml", "/etc/passwd",
        "/uploads/", "/images/", "/assets/", "/files/", "/docs/", "/public/", "/static/", "/media/",
    ]

    logs = []
    current_time = start_time
    random.shuffle(scan_paths)
    num_requests = random.randint(100, 150)

    for index in range(num_requests):
        # Choose unique paths (no repeats cycling through all
        path = scan_paths[index % len(scan_paths)]

        # 98% errors (scanning produces close to nothing)
        if random.random() < 0.98:
            status = "404"  # Most scans hit non-existent pages
        else:
            status = "200"

        # Generate requests that are 1-3 seconds apart
        current_time += datetime.timedelta(seconds=random.randint(1, 3))
        timestamp = current_time.strftime("%d/%b/%Y:%H:%M:%S ")

        # Build the log line
        bytes_sent = random.randint(100, 500)
        log_line = f'{attacker_ip} - - [{timestamp}] "GET {path} HTTP/1.1" {status} {bytes_sent}'

        logs.append(log_line)

    return logs



def generate_normal_user(user_ip, start_time, volume="normal"):
    """Generate a normal browsing behaviour"""
    normal_paths = [
        "/", "/index.html", "/home", "/about", "/about-us", "/contact", "/contact.html", "/services",
        "/products", "/products/laptops", "/products/phones", "/products/item-123", "/category/electronics",
        "/blog", "/blog/post-1", "/blog/category/lifestyle", "/blog/archive/2023", "/author/jane-doe",
        "/pricing", "/faq", "/help", "/support/ticket/54321", "/privacy-policy", "/terms-of-service",
        "/login", "/logout", "/register", "/forgot-password", "/account", "/profile", "/account/settings",
        "/account/orders", "/account/orders/9876", "/cart", "/checkout", "/checkout/success", "/wishlist",
        "/search?q=gaming+mouse", "/portfolio", "/gallery", "/forum", "/forum/thread/101", "/careers",
        "/static/style.css", "/assets/js/vendor.js", "/images/logo.png", "/favicon.ico",
        "/downloads/whitepaper.pdf", "/api/products?id=123", "/api/user/profile",
    ]

    logs = []
    current_time = start_time

    if volume == "high":
        num_request = random.randint(150, 200)
        error_rate = random.uniform(0.0, 0.05)
        num_unique_paths = random.randint(30, 50)

    else:  # normal
        num_request = random.randint(15, 50)
        error_rate = random.uniform(0.0, 0.05)
        num_unique_paths = random.randint(12, 25)

    # Select a subset of paths the user is likely to visit
    user_paths = random.sample(normal_paths, min(num_unique_paths, len(normal_paths)))

    for index in range(num_request):
        path = random.choice(user_paths)

        if random.random() < error_rate:
            status = random.choice(["401", "403"])
        else:
            status = random.choice(["200", "302", "304"])

        # Normal users browse at human speed (10-60 seconds between requests)
        current_time += datetime.timedelta(seconds=random.randint(10, 60))
        timestamp = current_time.strftime("%d/%b/%Y:%H:%M:%S ")

        bytes_sent = random.randint(500, 5000)  # Larger than attacks (real pages)
        log_line = f'{user_ip} - - [{timestamp}] "GET {path} HTTP/1.1" {status} {bytes_sent}'

        logs.append(log_line)

    return logs


def generate_labeled_dataset():
    """Creates a test dataset with known ground truth labels"""
    logs = []
    ground_truth = {}  # {ip: "ATTACK" or "BENIGN"}
    pass


def main():
    all_logs = []
    ground_truth = {}
    legit_user_count = 0

    base_time = datetime.datetime.now()

    # Generate credential stuffing attacks
    print(f"[*] Generating credential stuffing attacks...")

    # First attacker logs
    logs = generate_credential_stuffing(ATTACKER_IPS[0], base_time)
    all_logs.extend(logs)
    ground_truth[ATTACKER_IPS[0]] = "ATTACK"

    # Second attacker logs
    logs = generate_credential_stuffing(ATTACKER_IPS[1], base_time + datetime.timedelta(minutes=10))
    all_logs.extend(logs)
    ground_truth[ATTACKER_IPS[1]] = "ATTACK"

    # Recon Scan log
    print(f"[*] Generating reconnaissance scan from {ATTACKER_IPS[2]}")
    logs = generate_recon_scan(ATTACKER_IPS[2], base_time + datetime.timedelta(minutes=20))
    print(f" Generated {len(logs)} logs")
    all_logs.extend(logs)
    ground_truth[ATTACKER_IPS[2]] = "ATTACK"

    # Generate 2 high-volume users
    for index in range(2):
        user_ip = LEGIT_IPS[legit_user_count]
        print(f"[*] Generating high-volume legitimate user {user_ip}...")
        logs = generate_normal_user(user_ip, base_time + datetime.timedelta(minutes=10+index*10), volume="high")
        print(f" Generated {len(logs)} logs")
        all_logs.extend(logs)
        ground_truth[user_ip] = "BENIGN"
        legit_user_count += 1

    # 8-13 normal users
    for index in range(random.randint(8, 13)):
        user_ip = LEGIT_IPS[legit_user_count]
        print(f"[*] Generating normal user {user_ip}...")
        logs = generate_normal_user(user_ip, base_time + datetime.timedelta(minutes=40+index*5), volume="normal")
        print(f" Generated {len(logs)} logs")
        all_logs.extend(logs)
        ground_truth[user_ip] = "BENIGN"
        legit_user_count += 1

    random.shuffle(all_logs)

    with open(OUTPUT_FILE, "w") as f:
        for log in all_logs:
            f.write(log + "\n")

    with open(GROUND_TRUTH_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["IP Address", "Label"])
        for ip, label in ground_truth.items():
            writer.writerow([ip, label])


    print(f"[+] Generated {len(all_logs)} log entries")
    print(f"[+] Logs written to {OUTPUT_FILE}")
    print(f"[+] Ground truth written to {GROUND_TRUTH_FILE}")


if __name__ == "__main__":
    main()




