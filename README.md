# PyLog Threat Analyser 🐍
### Intelligent Threat Detection from Apache Logs

---

## 🧠 Overview
**PyLog Threat Analyser** is a Python command-line utility that scans Apache access logs and identifies threats using a dual-engine approach:
1.  **Threat Intelligence:** Enriches IPs using the [AbuseIPDB](https://www.abuseipdb.com/) reputation API.
2.  **Machine Learning:** Uses an Isolation Forest model to detect anomalous behaviour that might indicate unknown threats.

It is designed to replicate the *threat triage* process of a SOC (Security Operations Centre) — transforming raw logs into actionable intelligence.

---

## 🏷️ Features
- **Log Parsing:** Reads Apache logs, counts requests, and identifies HTTP error spikes.
- **ML-Powered Anomaly Detection:** Uses a `scikit-learn` Isolation Forest model to find statistically unusual IP behaviour.
- **Threat Intelligence Enrichment:** Queries AbuseIPDB for IP reputation and country of origin.
- **Persistent Caching:** Uses SQLite to store API lookups, improving performance on subsequent runs.
- **Fully Containerised:** Ships with a `Dockerfile` and is distributed via **Docker Hub**.
- **Automated CI/CD:** Includes a GitHub Actions workflow to automatically run `pytest` unit tests on every commit.

---

## 🧰 Tech Stack
| Category | Tools & Libraries |
|-----------|-------------------|
| Language | Python 3 |
| Deployment | **Docker**, **Docker Compose**, **Docker Hub** |
| Machine Learning | **scikit-learn**, **pandas** |
| Testing & CI/CD | **pytest**, **GitHub Actions** |
| Core | `re`, `sqlite3`, `argparse`, `requests`, `dotenv` |
| CLI & Output | `beautifultable`, `csv` |

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

## 🌐🐳🧰 Run Directly from Docker Hub (For End-Users)
This method allows you to run the application without cloning the source code, as long as you have Docker installed and an `access.log` file.
```bash
docker run -v "C:\path\to\your\access.log:/app/access.log" sosars/log-analyser:1.1 -f access.log --enrich -o report.csv
```

* Remember to replace `C:\path\to\your\access.log` with the actual path to your log file.
* The command will automatically find and download the `sosars/log-analyser:1.1` image from Docker Hub.

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
---------------------- [!] ATTACKER REPORT ----------------------
+-----------------+----------------+--------+-------------+---------+------------+
| IP Address      | Total Requests | Errors | Abuse Score | Country | Is Anomaly |
+-----------------+----------------+--------+-------------+---------+------------+
| 45.155.205.12   | 84             | 60     | 95          | RU      | Yes        |
| 102.45.19.56    | 10             | 8      | 0           | ZA      | No         |
| 173.248.16.77   | 4              | 3      | 70          | US      | Yes        |
+-----------------+----------------+--------+-------------+---------+------------+
```

---


## 🏗️ Architecture
```
access.log
   │
   ▼
file_parser.py       → Parses log & counts IP activity
anomaly_detector.py  → Uses scikit-learn model to find outlier IPs
enrichment.py        → Checks cache → queries AbuseIPDB → updates DB
reporting.py         → Displays CLI table / exports CSV
log_analyser.py      → Orchestrates CLI, enrichment, and reporting
ip_cache.db          → Stores persistent threat intelligence
Dockerfile           → Defines the recipe for the container image
docker-compose.yml   → Configures the container runtime environment
.github/workflows/   → Contains the automated CI/CD test workflow
```

---

## 🙋🏽‍♂️ SOSARS' Note
I'm just another security analyst playing my part in making the digital world a safer place for you & me. One commit at a time.

---

## 📜 License
MIT Licence © 2025 SOSARS

---

## 👨🏽‍🔬 Recruiter Note
This project demonstrates practical skills in log analysis, threat intelligence, and containerisation — key techniques used by SOC analysts and security engineers to detect and deploy security tooling in production environments.



