import csv
import requests
import time
import math

# Prompt the user for the reason the domains are being flagged
reason = input("Enter your reasoning for flagging domains (e.g., phishing activity, malware links, etc.): ").strip()

# Your VirusTotal API key
api_key = ""

# Common headers for API calls
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-apikey": api_key
}

# CSV file containing the list of domains to process
csv_file = "domains.csv"

# Read domains from the CSV file and calculate the total number of rows
with open(csv_file, newline='') as file:
    reader = csv.reader(file)
    rows = list(reader)  # Convert reader object to list for easy manipulation
    total_domains = len(rows) - 1  # Exclude header row

    # Display the total number of domains to process
    print(f"\nTotal domains to process: {total_domains}")

    # Skip the header row and loop over the domains
    for i, row in enumerate(rows[1:], start=1):  # Start from 1 to skip header row
        if len(row) < 2 or not row[1].strip():
            break  # Stop if the domain field is missing or blank

        domain = row[1].strip()
        print(f"\n--- Processing domain {i} of {total_domains}: {domain} ---")

        # Submit a new analysis request for the domain
        rescan_url = f"https://www.virustotal.com/api/v3/domains/{domain}/analyse"
        rescan_headers = {
            "accept": "application/json",
            "x-apikey": api_key
        }
        rescan_response = requests.post(rescan_url, headers=rescan_headers)
        print("Rescan requested:", rescan_response.status_code)

        # Submit a vote marking the domain as malicious
        vote_url = f"https://www.virustotal.com/api/v3/domains/{domain}/votes"
        vote_payload = {
            "data": {
                "type": "vote",
                "attributes": {
                    "verdict": "malicious"
                }
            }
        }
        vote_response = requests.post(vote_url, json=vote_payload, headers=headers)
        print("Vote submitted:", vote_response.status_code)

        # Leave a comment with the user's input
        comment_url = f"https://www.virustotal.com/api/v3/domains/{domain}/comments"
        comment_payload = {
            "data": {
                "type": "comment",
                "attributes": {
                    "text": f"""Automated Comment
Domain: {domain} - {reason}"""
                }
            }
        }
        comment_response = requests.post(comment_url, json=comment_payload, headers=headers)
        print("Comment posted:", comment_response.status_code)

        # Calculate and display progress and ETA
        progress = i / total_domains * 100
        remaining_time = (total_domains - i) * 60  #each domain takes around 1 minute
        minutes_left = math.ceil(remaining_time / 60)

        # Display progress and estimated time left
        print(f"Progress: {i}/{total_domains} ({progress:.2f}%)")
        print(f"Estimated time left: {minutes_left} minute(s)")

        # Wait to stay within API call limits (4 calls per minute)
        print("Waiting 60 seconds before continuing...")
        time.sleep(60)
