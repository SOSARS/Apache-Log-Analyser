# --- Core Libraries ---
import argparse
import os
import time
import sqlite3
from dotenv import load_dotenv

# --- Local Modules ---
from file_parser import parse_apache_file
from reporting import generate_report, export_to_csv
from enrichment import check_cache, get_ip_reputation, update_cache


def setup_database():
    """Connects to the SQLite DB and creates the necessary table if it doesn't exist."""
    conn = sqlite3.connect('ip_cache.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reputation (
            ip_address TEXT PRIMARY KEY,
            abuse_score INTEGER,
            country TEXT,
            last_checked TEXT
        )
    ''')
    conn.commit()
    return conn


def main():
    """The main log analyser function"""
    parser = argparse.ArgumentParser(description="A script to parse Apache log files for errors.")
    parser.add_argument("-f", "--file", required=True, help="Path to the Apache access log file.")
    parser.add_argument("-o", "--output", help="Optional: Path to save the report as a CSV file.")
    parser.add_argument("--enrich", action='store_true', help="Enable IP reputation enrichment via AbuseIPDB.")
    parser.add_argument("--apikey", help="Your AbuseIPDB API key. (Can also be set in .env)")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.getenv("API_KEY")

    if args.apikey:
        api_key = args.apikey

    db_connection = setup_database()

    print(f"[*] Processing log file: {args.file}...")
    final_data = parse_apache_file(args.file)

    if final_data:
        sorted_ips = sorted(final_data.items(), key=lambda item: item[1]["errors"], reverse=True)

        # --- Enrichment Logic ---
        report_data = []
        if args.enrich:
            if not api_key:
                print("[!] Enrichment enabled, but no API key found. Skipping.")

                # Default to non-enriched data
                report_data = [(ip, data["total"], data["errors"], "N/A", "N/A") for ip, data in sorted_ips]
            else:
                print("[*] Starting IP reputation enrichment...")
                for ip, data in sorted_ips:

                    # 1. Check local cache first
                    cached_result = check_cache(ip, db_connection)
                    if cached_result:
                        score, country = cached_result
                        print(f"  [CACHE] Found {ip} in local DB.")

                    else:
                        # 2. If not in cache, call API
                        print(f"  [API] Querying AbuseIPDB for {ip}...")
                        score, country = get_ip_reputation(ip, api_key)

                        # 3. Save new result to cache
                        update_cache(ip, score, country, db_connection)

                        # 4. Avoid abusing the API
                        time.sleep(1)

                    report_data.append((ip, data["total"], data["errors"], score, country))
        else:
            # If enrichment is off, create a simple list
            report_data = [(ip, data["total"], data["errors"], "N/A", "N/A") for ip, data in sorted_ips]

        # --- End of Enrichment Logic ---

        # Pass the final report_data to the reporting functions
        generate_report(report_data)
        if args.output:
            export_to_csv(report_data, args.output)

        print("\n[*] Analysis complete!")

    else:
        print(f"\n[*] Analysis aborted due to error.")

    db_connection.close()


if __name__ == "__main__":
    main()