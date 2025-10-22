# PyLog Threat Analyser 🐍  
### Intelligent Threat Detection from Apache Logs

---

## 🧠 Overview
**PyLog Threat Analyser** is a Python command-line utility that scans Apache access logs, identifies potentially malicious IPs, and enriches them using the [AbuseIPDB](https://www.abuseipdb.com/) reputation API.  
It’s designed to replicate the early stages of *threat triage* that a SOC (Security Operations Centre) analyst would perform — transforming raw logs into actionable intelligence.

---

## ⚙️ Features
- **Log Parsing:** Reads Apache access logs, counts requests, and identifies HTTP error spikes (4xx/5xx).  
- **Threat Intelligence Enrichment:** Queries AbuseIPDB for IP reputation, country, and abuse confidence score.  
- **Persistent Caching:** Uses SQLite to store IP reputations, reducing API calls and improving runtime efficiency.  
- **Prioritised Reporting:** Sorts IPs by error volume or threat score for immediate visibility.  
- **Clean CLI Interface:** Built with `argparse`, supporting enrichment flags and CSV export.  
- **Security-Conscious Design:** `.env` file for API keys, safe parameterised SQL, and rate-limit handling.

---

## 🧰 Tech Stack
| Category | Tools & Libraries |
|-----------|-------------------|
| Language | Python 3 |
| Core | `re`, `sqlite3`, `argparse`, `requests`, `dotenv` |
| CLI & Output | `beautifultable`, `csv` |
| Threat Intel | AbuseIPDB API |
| Cache | SQLite |

---

## 🚀 Quick Start
```bash
git clone https://github.com/Sosars/Apache-Log-Analyser.git
cd Apache-Log-Analyser
pip install -r requirements.txt
```

---

## Set your API key up
Create a `.env` file in the project root:
```env
API_KEY="your_abuseipdb_api_key"
```

## 🧑🏽‍💻 Basic Scan
```bash / PowerShell
py log_analyser.py -f access.log
```

## 🕵🏽 Enriched Scan (try it out 😁)
``` bash / PowerShell
py log_analyser.py -f access.log --enrich
```

## 👽 Enriched Scan + CSV Export
``` bash / PowerShell
py log_analyser.py -f access.log --enrich -o report.csv
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
```

---

## 🙋🏽‍♂️ SOSARS' Note
I'm building this as a security enthusiast on a journey to making the world a safer place to roam, one step at a time.

---

## 📜 License
MIT Licence © 2025 SOSARS

---

## 👨🏽‍🔬 Recruiter Note
This project demonstrates practical skills in log analysis, threat intelligence, and automation — the same techniques used by SOC analysts and security engineers to detect and prioritise malicious activity in production environments.



