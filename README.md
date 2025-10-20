# Python Log Analyser 🐍

A command-line tool built with Python to parse Apache access logs, identify errors, and generate a summary report of suspicious IP addresses.

## Features

- Parses Apache log files to extract IP addresses and status codes.
- Identifies client-side (4xx) and server-side (5xx) errors.
- Generates a clean, sorted summary table of the top offenders.
- Professional command-line interface using `argparse`.

## Installation

1. Clone the repository: `git clone <your-repo-url-here>`
2. Install the required packages:
   ```bash
   py -m pip install beautifultable
   ```
