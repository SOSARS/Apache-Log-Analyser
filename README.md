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

## 📊 Performance Metrics

### Detection Accuracy
- **True Positive Rate:** 100% (3/3 attacks detected)
- **False Positive Rate:** 0% (after threshold optimization)
- **Processing Speed:** 22,560 entries/second
- **Analysis Time:** 0.13 seconds for 2,867 log entries

### Threshold Optimisation
Initial testing at `threshold=0.0` achieved 100% TPR but 25% FPR (3 false alarms from high-volume legitimate users). Through systematic threshold tuning, optimal performance was achieved at `threshold=-0.05`:
```
| Threshold | TPR   | FPR  | Attacks Detected | False Alarms |
|-----------|-------|------|------------------|--------------|
| 0.00      | 100%  | 25%  | 3/3              | 3/12         |
| -0.05     | 100%  | 0%   | 3/3              | 0/12         |
```
See [CASE_STUDY.md](CASE_STUDY.md) for complete validation methodology and results analysis.

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

### CLI Table Output
```
------------------ [!] ATTACKER REPORT ------------------
+-----------------+----------------+--------+-------------+---------+------------+-------------+
| IP Address      | Total Requests | Errors | Abuse Score | Country | Is Anomaly | Confidence  |
+-----------------+----------------+--------+-------------+---------+------------+-------------+
| 185.191.205.10  |      79        |   79   |     11      |   IL    |    Yes     |   -0.116    |
+-----------------+----------------+--------+-------------+---------+------------+-------------+
| 45.9.148.113    |      49        |   49   |      0      |   NL    |     No     |    0.041    |
+-----------------+----------------+--------+-------------+---------+------------+-------------+
| 103.141.17.15   |      18        |   18   |      0      |   HK    |    Yes     |   -0.034    |
+-----------------+----------------+--------+-------------+---------+------------+-------------+
| 8.8.8.8         |      31        |    0   |      0      |   US    |    Yes     |   -0.065    |
+-----------------+----------------+--------+-------------+---------+------------+-------------+
```

**Confidence Score Interpretation:**
- **Negative scores** (e.g., -0.116): Anomalous behavior detected
- **Positive scores** (e.g., +0.041): Normal behavior
- **Threshold**: -0.05 (IPs below this are flagged as anomalies)

### CSV Export
When using `-o report.csv`, the data is exported in structured format for further analysis or SIEM integration.

---


## 🏗️ Architecture
### Core Application
```
access.log
   │
   ▼
file_parser.py       → Parses log & extracts IP activity, paths, and status codes
anomaly_detector.py  → Feature engineering + Isolation Forest with confidence scoring
enrichment.py        → Checks cache → queries AbuseIPDB → updates DB
reporting.py         → Displays CLI table / exports CSV with anomaly scores
log_analyser.py      → Orchestrates CLI, enrichment, and reporting
ip_cache.db          → Stores persistent threat intelligence
```

### Validation & Testing Infrastructure
```
generate_test_dataset.py  → Generates labeled attack scenarios and benign traffic
measure_performance.py    → Calculates TPR/FPR against ground truth labels
tune_threshold.py         → Systematic threshold optimisation analysis
ground_truth_labels.csv   → Known attack/benign labels for validation
test_dataset.log          → Synthetic Apache logs with realistic patterns
```

## 🎯 Sigma Detection Rules

The `/sigma` directory contains detection rules for common attack patterns in Sigma format, compatible with major SIEM platforms (Splunk, ELK, QRadar).

**Rules included:**
- **Credential Stuffing:** 100+ failed logins in 5 minutes
- **Vulnerability Scanning:** 50+ probes to admin/config paths
- **Excessive Errors:** 80+ HTTP errors with >85% error rate

These signature-based rules complement the ML-based anomaly detection, providing both fast detection of known attacks and discovery of novel threats.

See [sigma/README.md](sigma/README.md) for usage instructions.

### Deployment & CI/CD
```
Dockerfile           → Container image definition
docker-compose.yml   → Container runtime configuration
.github/workflows/   → Automated CI/CD test workflow (pytest)
```

### Documentation
```
README.md            → Quick start and usage guide
CASE_STUDY.md        → Complete technical analysis with performance metrics
```
---

## 🙋🏽‍♂️ SOSARS' Note
"No one cares what you did **yesterday.** What have you done **today** to better yourself? What will your story be **tomorrow?**
**Every day** is day one. Let's get it.

---

## 📜 License
MIT Licence © 2025 SOSARS

---

## 👨🏽‍🔬 Recruiter Note
This project demonstrates practical skills in log analysis, threat intelligence, and containerisation — key techniques used by SOC analysts and security engineers to detect and deploy security tooling in production environments.



