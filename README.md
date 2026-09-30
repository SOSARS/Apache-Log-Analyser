# PyLog Threat Analyser 🐍

A Python command-line tool for reviewing Apache access logs, identifying unusual IP behaviour and enriching results with AbuseIPDB reputation data.

This portfolio project combines log parsing, Isolation Forest anomaly detection and threat intelligence to support initial security triage. A flagged IP is a candidate for investigation, not a confirmed attacker.

## 🏷️ Features

- Aggregate requests, HTTP errors and requested paths by IP address.
- Identify unusual IP activity using scikit-learn's Isolation Forest.
- Enrich IP addresses with AbuseIPDB reputation scores and country information.
- Cache reputation lookups in SQLite.
- Display results in the terminal and export CSV reports.
- Run locally or in Docker.
- Run automated pytest tests through GitHub Actions continuous integration.

## 🧠 How detection works

The accompanying [case study](CASE_STUDY.md) describes three features: request volume, error rate and path diversity. The model scores IP-level activity summaries, rather than classifying every individual log entry.

An anomaly score measures unusual behaviour relative to the model's reference data. It is not a calibrated probability that an IP is malicious, and a score alone does not explain the cause of the anomaly. Investigate the underlying requests, errors and paths before reaching a conclusion.

AbuseIPDB supplies additional context. A high reputation score supports further investigation; a zero score does not establish that an IP is safe. Country information describes IP geolocation, not an attacker's identity or physical location.

## 🧰 Requirements

For local use, install Python 3 with pip and virtual environment support. For container use, install Docker Engine with the Compose plugin, or Docker Desktop.

Have an Apache access log available as `access.log`. The parser's supported log format should be checked against your input before analysing a large file.

An AbuseIPDB API key is needed for `--enrich`. Basic scans can be run without enrichment.

## 🚀 Get the source

```bash
git clone https://github.com/SOSARS/Apache-Log-Analyser.git
cd Apache-Log-Analyser
```

Run the following commands from the project root.

## 🤠 Local installation

### Linux or macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The Windows examples call the virtual environment directly and do not require activation.

### 🕵🏽 Optional enrichment setup

Create a `.env` file in the project root:

```dotenv
API_KEY=your_abuseipdb_api_key
```

Keep this file out of version control. Enrichment requires network access and is subject to the API provider's limits.

## 🧑🏽‍💻 Local usage

### Linux or macOS

With the virtual environment activated:

```bash
# 🧑🏽‍💻 Basic scan
python log_analyser.py -f access.log

# 🕵🏽 Enriched scan (try it out 😁)
python log_analyser.py -f access.log --enrich

# 👽 Enriched scan with CSV export
python log_analyser.py -f access.log --enrich -o report.csv
```

### Windows PowerShell

```powershell
# 🧑🏽‍💻 Basic scan
.\.venv\Scripts\python.exe log_analyser.py -f access.log

# 🕵🏽 Enriched scan (try it out 😁)
.\.venv\Scripts\python.exe log_analyser.py -f access.log --enrich

# 👽 Enriched scan with CSV export
.\.venv\Scripts\python.exe log_analyser.py -f access.log --enrich -o report.csv
```

## ▶️🐳 Run with Docker Compose

The repository provides a Dockerfile and `docker-compose.yml` with an `app` service. Start with a basic scan:

```bash
docker compose run --rm --build app -f access.log
```

For enrichment and CSV export:

```bash
docker compose run --rm --build app -f access.log --enrich -o report.csv
```

Before using these commands, check that the Compose configuration:

- Mounts the input log at the path the application reads.
- Passes `API_KEY` into the container or mounts the application's `.env` file.
- Mounts the CSV output location and SQLite cache to persistent host storage.

A project-root `.env` file can supply Compose interpolation values; it does not automatically pass every value to the application container. Files written only inside a container are not retained after that container is removed with `--rm`.

## 🌐🐳🧰 Run from Docker Hub

The original project documentation identifies `sosars/log-analyser:1.1` as the published image.

**Layout assumption:** the examples below assume the image runs the analyser from `/app`, accepts the documented CLI arguments, uses `API_KEY` from its environment and stores its cache at `/app/ip_cache.db`. Confirm these paths and behaviours against the Dockerfile, enrichment code and published image before using this as the recommended installation route.

Create an `output` directory and an empty `ip_cache.db` file if it does not already exist. Do not overwrite an existing cache. Keep `access.log` and `.env` in the current directory.

### Linux or macOS

```bash
mkdir -p output
touch ip_cache.db

docker run --rm \
  --env-file .env \
  --mount "type=bind,source=$(pwd)/access.log,target=/app/access.log,readonly" \
  --mount "type=bind,source=$(pwd)/output,target=/app/output" \
  --mount "type=bind,source=$(pwd)/ip_cache.db,target=/app/ip_cache.db" \
  sosars/log-analyser:1.1 \
  -f /app/access.log --enrich -o /app/output/report.csv
```

### Windows PowerShell

```powershell
New-Item -ItemType Directory -Path output -Force | Out-Null
if (-not (Test-Path ip_cache.db)) {
    New-Item -ItemType File -Path ip_cache.db | Out-Null
}
$projectPath = (Get-Location).Path

docker run --rm `
  --env-file .env `
  --mount "type=bind,source=$projectPath/access.log,target=/app/access.log,readonly" `
  --mount "type=bind,source=$projectPath/output,target=/app/output" `
  --mount "type=bind,source=$projectPath/ip_cache.db,target=/app/ip_cache.db" `
  sosars/log-analyser:1.1 `
  -f /app/access.log --enrich -o /app/output/report.csv
```

With the assumed layout, the CSV is written to `output/report.csv` on your computer and the cache remains in the current directory. Verify both after the first run. An empty cache file is suitable only if the application initialises the SQLite schema automatically.

## 🗃️ Example output

The following illustrative values show the report fields. They are not validation results or claims about the listed IP addresses.

| IP address | Total requests | Errors | Abuse score | Country | Is anomaly |
|---|---:|---:|---:|---|---|
| 45.155.205.12 | 84 | 60 | 95 | RU | Yes |
| 102.45.19.56 | 10 | 8 | 0 | ZA | No |
| 173.248.16.77 | 4 | 3 | 70 | US | Yes |

Read this as an **IP triage report**. A high error count can result from legitimate application or access problems. Combine the output with request details, application context and other evidence.

The application may still display the original heading `ATTACKER REPORT`; changing that heading requires an update to the reporting code as well as this documentation.

## 🏗️ Project structure

| Component | Purpose |
|---|---|
| `log_analyser.py` | Command-line entry point and orchestration |
| `file_parser.py` | Parse log entries and aggregate IP activity |
| `anomaly_detector.py` | Build features and score unusual activity |
| `enrichment.py` | Query AbuseIPDB and cache responses |
| `reporting.py` | Terminal output and CSV reports |
| `ip_cache.db` | SQLite reputation cache |
| `generate_test_dataset.py` | Generate synthetic traffic and labels |
| `measure_performance.py` | Compare detections with ground truth |
| `tune_threshold.py` | Explore detection thresholds |
| `Dockerfile` and `docker-compose.yml` | Container build and runtime configuration |
| `.github/workflows/` | Automated test workflows |
| [CASE_STUDY.md](CASE_STUDY.md) | Technical approach and exploratory evaluation |

## 👨🏽‍🔬 Testing and evaluation

Run the automated tests from the project root after installing the dependencies:

```bash
python -m pytest
```

On Windows, use `.\.venv\Scripts\python.exe -m pytest`.

The case study reports experiments on synthetic traffic. Those experiments demonstrate a testing approach, but the documented IP counts and threshold results need reconciliation before quoting a definitive detection rate. Threshold tuning results should be separated from evaluation on independent data.

No production detection accuracy, sustained throughput or real-time capability is established by the current documentation. A small batch-processing measurement should not be presented as a production benchmark.

## Limitations

- Anomalies and reputation scores are investigation signals, not proof of malicious activity.
- IP aggregation can combine several users behind a shared address or split one campaign across several addresses.
- The described model features do not use request timing, even if synthetic traffic includes timestamps.
- Synthetic scenarios may be easier to separate than real traffic, including benign scanners, broken applications and low-volume attacks.
- Reputation caching needs an appropriate refresh policy; old results may no longer reflect current reputation.
- This is a batch-analysis portfolio project, not a replacement for a SIEM or a validated production detection service.

## 📜 Licence

MIT Licence © 2025 SOSARS. See the repository's licence file for the full terms.

## 🙋🏽‍♂️ SOSARS’ Note

"No one cares what you did **yesterday.** What have you done **today** to better yourself? What will your story be **tomorrow?**
**Every day** is day one. Let's get it.
