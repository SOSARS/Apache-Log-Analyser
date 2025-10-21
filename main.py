import re
import csv
import argparse
from beautifultable import BeautifulTable


def parse_apache_file(filepath):
    """Reads an Apache log file and returns a dictionary of IP data"""

    # Regex to extract IP and status code
    pattern = re.compile(r'^(\d{1,3}(?:\.\d{1,3}){3})\s.*"\s*(\d{3})\s')

    try:
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

    except FileNotFoundError:
        print(f"\n[!] ERROR: The file '{filepath}' was not found.\n")
        return None


def export_to_csv(sorted_data, filepath):
    """Takes the sorted data and a filename
    and writes the content to a csv file."""
    fields = ["IP Address", "Total Requests", "Errors"]

    try:
        with open(filepath, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(fields)  # Header row

            for ip, stats in sorted_data:  # Loops through the sorted list
                writer.writerow([ip, stats["total"], stats["errors"]])

        print(f"\n[+] Report successfully exported to {filepath}")

    except IOError:
        print(f"\n[!] ERROR: Could not write to '{filepath}'. Check permissions.\n")



def generate_report(sorted_data):
    """Takes IP data and prints a formatted report."""

    # Create the table and set the headers
    table = BeautifulTable()
    table.columns.header = ["IP Address", "Total Requests", "Errors"]
    table.columns.alignment["IP Address"] = BeautifulTable.ALIGN_LEFT

    # Loop through the sorted data and add rows to the table
    for ip, data in sorted_data:
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
    parser.add_argument("-o", "--output", required=False, help="Path to the output file.")
    args = parser.parse_args()

    # Get the log file path from the arguments
    log_file = args.file

    print(f"[*] Processing log file: {log_file}...")
    print()

    # Call the engine to retrieve the data
    final_data = parse_apache_file(log_file)

    # Proceed only if the data was successfully returned
    if final_data:
        sorted_ips = sorted(final_data.items(), key=lambda item: item[1]["errors"], reverse=True)
        generate_report(sorted_ips)

        if args.output:
            export_to_csv(sorted_ips, args.output)
        print("\n[*] Analysis complete!")

    else:
        print(f"[*] Analysis aborted due to error.")


# ----------- Main ------------------ #
if __name__ == "__main__":
    main()

