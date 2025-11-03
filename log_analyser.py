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
from anomaly_detector import detect_anomalies


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

    log_dict = parse_apache_file(args.file)

    if log_dict:
        # Run anomaly detection first to get the set of weird IPs
        anomalous_ips, score_dict = detect_anomalies(log_dict, threshold=-0.05)

        # Sort the data after running the model
        sorted_ips = sorted(log_dict.items(), key=lambda item: item[1]["errors"], reverse=True)

        report_data = []
        print("[*] Processing IP data...")


        for ip, data in sorted_ips:
            score, country = "N/A", "N/A"  # Default values

            # Check for enrichment if the flag is set
            if args.enrich and api_key:
                cached_result = check_cache(ip, db_connection)
                if cached_result:
                    score, country = cached_result
                else:
                    score, country = get_ip_reputation(ip, api_key)
                    update_cache(ip, score, country, db_connection)
                    time.sleep(1)

            # Check if the IP was flagged by the model
            is_anomaly = ip in anomalous_ips
            anomaly_score = score_dict.get(ip, 0.0)

            # Append the final, fully-enriched data point for THIS IP
            report_data.append((ip, data["total"], data["errors"], score, country, is_anomaly, anomaly_score))

        # --- END OF LOOP ---

        # Pass the complete report_data to the functions
        generate_report(report_data)
        if args.output:
            export_to_csv(report_data, args.output)

        print("\n[*] Analysis complete!")

    else:
        print(f"\n[*] Analysis aborted due to error.")

    db_connection.close()


if __name__ == "__main__":
    main()