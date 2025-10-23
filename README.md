# PyLog Threat Analyser 🐍
### Intelligent Threat Detection from Apache Logs

---

## 🧠 Overview
**PyLog Threat Analyser** is a Python command-line utility that scans Apache access logs, identifies potentially malicious IPs, and enriches them using the [AbuseIPDB](https://www.abuseipdb.com/) reputation API.
It is designed to replicate the early stages of *threat triage* that a SOC (Security Operations Centre) analyst would perform — transforming raw logs into actionable intelligence.

---

## ⚙️ Features
- **Log Parsing:** Reads Apache access logs, counts requests, and identifies HTTP error spikes (4xx/5xx).
- **Threat Intelligence Enrichment:** Queries AbuseIPDB for IP reputation, country, and abuse confidence score.
- **Persistent Caching:** Uses SQLite to store IP reputations, reducing API calls and improving runtime efficiency.
- **Prioritised Reporting:** Sorts IPs by error volume or threat score for immediate visibility.
- **Fully Containerised:** Ships with a `Dockerfile` and `docker-compose.yml` for a consistent, one-command runtime environment.
- **Clean CLI Interface:** Built with `argparse`, supporting enrichment flags and CSV export.

---

## 🧰 Tech Stack
| Category | Tools & Libraries |
|-----------|-------------------|
| Language | Python 3 |
| Deployment | **Docker**, **Docker Compose** |
| Core | `re`, `sqlite3`, `argparse`, `requests`, `dotenv` |
| CLI & Output | `beautifultable`, `csv` |
| Threat Intel | AbuseIPDB API |
| Cache | SQLite |

---

## 🚀 Quick Start (Docker - Recommended)

This project is fully containerised, which is the easiest and most reliable way to run it.

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) must be installed and running.

### 1. Clone & Set Up
```bash
git clone https://github.com/Sosars/Apache-Log-Analyser.git
cd Apache-Log-Analyser
```
---

## Set your API key up
Create a `.env` file in the project root:
```env
API_KEY="your_abuseipdb_api_key"
```

---

## ▶️🐳 Run the Analyser
Use Docker Compose to build the image and run the analyser. This commands mounts your local `access.log` and `ip_cache.db` into the container, ensuring your cache persists between runs.

### Enriched Scan + CSV Export:
```bash
docker-compose run --rm app -f access.log --enrich -o report.csv
```

---

## 🤠 Manual Installation (Alternative)
If you prefer not to use Docker, you can run the script locally.

### 1. Setup
```bash
python3 pip install -r requirements.txt (Linux)
py -m pip install -r requirements.txt (Windows)
```
Ensure your API key is set in the `.env` file.

### 2. Usage Examples:

#### 🧑🏽‍💻 Basic Scan
```bash / PowerShell
python3 log_analyser.py -f access.log (Linux)
py log_analyser.py -f access.log (Windows)
```

#### 🕵🏽 Enriched Scan (try it out 😁)
``` bash / PowerShell
python3 log_analyser.py -f access.log --enrich (Linux)
py log_analyser.py -f access.log --enrich (Windows)
```

#### 👽 Enriched Scan + CSV Export
``` bash / PowerShell
python3 log_analyser.py -f access.log --enrich -o report.csv (Linux)
py log_analyser.py -f access.log --enrich -o report.csv (Windows)
```

## 🗃️ Example Output
```
------------------ [!] ATTACKER REPORT ------------------
+-----------------+-----------------+--------+--------------+----------+
| IP Address      | Total Requests  | Errors | Abuse Score  | Country  |
+-----------------+-----------------+--------+--------------+----------+
| 45.155.205.12   | 84              | 60     | 95           | RU       |
| 102.45.19.56    | 10              | 8      | 0            | ZA       |
| 173.248.16.77   | 4               | 3      | 70           | US       |
+-----------------+-----------------+--------+--------------+----------+
```

---


## 🏗️ Architecture
```
access.log
   │
   ▼
file_parser.py       → Parses log & counts IP activity
enrichment.py        → Checks cache → queries AbuseIPDB → updates DB
reporting.py         → Displays CLI table / exports CSV
log_analyser.py      → Orchestrates CLI, enrichment, and reporting
ip_cache.db          → Stores persistent threat intelligence
Dockerfile           → Defines the recipe for the container image
docker-compose.yml   → Configures the container runtime environment
```

---

## 🙋🏽‍♂️ SOSARS' Note
I'm building this as a security enthusiast on a journey to making the world a safer place to roam, one step at a time.

---

## 📜 License
MIT Licence © 2025 SOSARS

---

## 👨🏽‍🔬 Recruiter Note
This project demonstrates practical skills in log analysis, threat intelligence, and containerisation — key techniques used by SOC analysts and security engineers to detect and deploy security tooling in production environments.



