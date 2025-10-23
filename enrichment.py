import sqlite3
import requests
import datetime


def check_cache(ip_address: str, db_connection) -> tuple | None:
    """Looks inside the local database to see if the IP has been investigated"""
    cursor = db_connection.cursor()

    # Executes the query and passes the IP Address as a paramter
    cursor.execute("SELECT ABUSE_SCORE, COUNTRY FROM REPUTATION WHERE IP_ADDRESS = ?", (ip_address,))
    result = cursor.fetchone()

    if result:
        # If found, returns a result (e.g., (100, RU))
        return result
    else:
        return None


def get_ip_reputation(ip_address: str, api_key: str) -> tuple[int, str]:
    """Contacts the external AbuseIPDB API"""
    url = "https://api.abuseipdb.com/api/v2/check"

    # Headers that include API key for authentication
    headers = {
        "Accept": "application/json",
        "Key": api_key
    }

    # Parameters for the request
    params = {
        "ipAddress": ip_address,
        "maxAgeInDays": "90"
    }

    try:
        # Make the API request
        response = requests.get(url, headers=headers, params=params)

        # Check if the request is successful
        if response.status_code == 200:
            data = response.json()["data"]
            score = data["abuseConfidenceScore"]
            country = data["countryCode"]
            return (score, country)

        else:
            # If the API produces an error (bad key or invalid IP)
            print(f"[!] API Error: Received status code {response.status_code}")
            return (0, "N/A")

    except requests.exceptions.RequestException as e:
        print(f"[!] Network Error: Could not connect to the API.")
        return (0, "N/A")



def update_cache(ip_address: str, abuse_score: int, country_code: str, db_connection) -> None:
    """Saves the new intelligence retrieved from the API into the local database."""

    # Get the current time in a standard format
    timestamp = datetime.datetime.now().isoformat()

    cursor = db_connection.cursor()

    # INSERT a new row if the IP does not exist, or REPLACE if it does
    cursor.execute('''
    INSERT OR REPLACE INTO REPUTATION (IP_ADDRESS, ABUSE_SCORE, COUNTRY, LAST_CHECKED)
    VALUES (?, ?, ?, ?)
    ''', (ip_address, abuse_score, country_code, timestamp))

    # Saves the changes to the database
    db_connection.commit()





