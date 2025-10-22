import csv
from beautifultable import BeautifulTable


def export_to_csv(report_data, filepath):
    """Takes the enriched report data and writes it to a CSV file."""
    fields = ["IP Address", "Total Requests", "Errors", "Abuse Score", "Country"]

    try:
        with open(filepath, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(fields)  # Header row

            for row in report_data:
                writer.writerow(row)

        print(f"\n[+] Report successfully exported to {filepath}")

    except IOError:
        print(f"\n[!] ERROR: Could not write to '{filepath}'. Check permissions.\n")



def generate_report(report_data):
    """Takes enriched report data and prints a formatted report."""

    # Create the table and set the headers
    table = BeautifulTable()
    table.columns.header = ["IP Address", "Total Requests", "Errors", "Abuse Score", "Country"]
    table.columns.alignment["IP Address"] = BeautifulTable.ALIGN_LEFT

    # Loop through the sorted data and add rows to the table
    for row in report_data:
        table.rows.append(row)


    # Print the final table
    print("------------------ [!] ATTACKER REPORT ------------------")
    print(table)