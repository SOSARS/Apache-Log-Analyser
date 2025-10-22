# PyLog Threat Analyser 🐍

A command-line utility built with Python for parsing Apache web server logs. It enriches the data by querying the AbuseIPDB API for IP reputations, using a persistent SQLite cache to minimise redundant API calls and improve performance.

The tool identifies and summarises potential threats based on HTTP error codes and known malicious IP addresses, presenting a clean, prioritised report.

---

## 📸 Demo

![PyLog Threat Analyser Demo](demo.png)

---

## 🗽 Key Features

* **Log Parsing:** Efficiently reads and processes standard Apache `access.log` files.
* **Threat Intelligence Enrichment:** Queries the AbuseIPDB API to fetch the abuse confidence score and country of origin for offending IPs.
* **Persistent SQLite Caching:** Caches API lookups in a local `ip_cache.db` file. This makes subsequent scans of overlapping IPs almost instant and respects API rate limits.
* **Prioritised Reporting:** Automatically sorts the output to display the IP addresses with the highest error counts at the top.
* **CSV Export:** Provides an optional argument to save the final, enriched report to a clean CSV file.
* **Professional CLI:** Utilises `argparse` for a clean, user-friendly command-line interface with optional flags.

---

## 🛠️ Tech Stack

* **Language:** Python 3
* **Core Libraries:**
    * `requests` for making API calls.
    * `sqlite3` (built-in) for the persistent cache database.
    * `python-dotenv` for securely managing API keys.
    * `argparse` for the command-line interface.
    * `beautifultable` for formatted console output.

---

## ⚙️ Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Sosars/Apache-Log-Analyser.git
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd Apache-Log-Analyser
    ```

3.  **Install the required packages:**
    ```bash
    py -m pip install -r requirements.txt
    ```

4.  **Set up your environment file:**
    * Create a file named `.env` in the project directory.
    * Add your AbuseIPDB API key to it like this:
        ```text
        API_KEY="your_api_key_goes_here"
        ```

---

## 🚀 Usage

Run the script from the command line, providing the path to the log file.

**Basic Usage (no enrichment):**
```bash / PowerShell
py log_analyser.py -f access.log
```

**Enrichment Run (try it out! 😁):**
```bash / PowerShell
py log_analyser.py -f access.log --enrich
```

**Enrichment w/ CSV Export:**
```bash / PowerShell
py log_analyser.py -f access.log --enrich -o threat_report.csv
```
