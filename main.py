import re
import argparse
from beautifultable import BeautifulTable


def parse_apache_file(filepath):
    """Reads an Apache log file and returns a dictionary of IP data"""

    # Regex to extract IP and status code
    pattern = re.compile(r'^(\d{1,3}(?:\.\d{1,3}){3})\s.*"\s*(\d{3})\s')

    # Structure: {ip: {"total": int, "errors": int}}
    log_dict = {}
    with open(filepath, "r") as log:
        for line in log:
            match = pattern.search(line)
            if match:
                ip = match.group(1)
                status = match.group(2)

                if ip not in log_dict:
                    log_dict[ip] = {"total": 0, "errors": 0}

                log_dict[ip]["total"] += 1

                # Check for 4xx or 5xx errors
                if status.startswith(("4", "5")):
                    log_dict[ip]["errors"] += 1

    return log_dict


def generate_report(log_dict):
    """Takes IP data and prints a formatted report."""
    sorted_ips = sorted(log_dict.items(), key=lambda item: item[1]["errors"], reverse=True)

    # Create the table and set the headers
    table = BeautifulTable()
    table.columns.header = ["IP Address", "Total Requests", "Errors"]
    table.columns.alignment["IP Address"] = BeautifulTable.ALIGN_LEFT

    # Loop through the sorted data and add rows to the table
    for ip, data in sorted_ips:
        table.rows.append([ip, data["total"], data["errors"]])

    # Print the final table
    print("------------------ [!] ATTACKER REPORT ------------------")
    print(table)


def main():
    """The main log parser function"""

    # Create the parser
    parser = argparse.ArgumentParser(description="A script to parse Apache log files for errors.")

    # Add the --file argument
    parser.add_argument("-f", "--file", required=True, help="Path to the Apache access log file.")
    args = parser.parse_args()

    # Prompt for log file path
    log_file = args.file
    print(f"[*] Processing log file: {log_file}...")
    print()

    # 1. Call the engine to retrieve the data
    final_data = parse_apache_file(log_file)

    # 2. Call the presenter to print the report
    generate_report(final_data)
    print()

    print("[*] Analysis complete!")


if __name__ == "__main__":
    main()














