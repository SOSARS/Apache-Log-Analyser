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
