import csv
import requests
import time
import math

# Prompt the user for the reason the IPs are being flagged
reason = input("Enter your reasoning for flagging IPs (e.g., phishing activity, malware links, etc.): ").strip()

# Your VirusTotal API key
api_key = ""

# Common headers for API calls
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-apikey": api_key
}

# CSV file containing the list of IPs to process
csv_file = "ips.csv"

# Read IP addresses from the CSV file and calculate the total number of rows
with open(csv_file, newline='') as file:
    reader = csv.reader(file)
    rows = list(reader)  # Convert reader object to list for easy manipulation
    total_ips = len(rows) - 1  # Exclude header row

    # Display the total number of IPs to process
    print(f"\nTotal IPs to process: {total_ips}")

    # Skip the header row and loop over the IPs
    for i, row in enumerate(rows[1:], start=1):  # Start from 1 to skip header row
        if len(row) < 2 or not row[1].strip():
            break  # Stop if the IP field is missing or blank

        ip_address = row[1].strip()
        print(f"\n--- Processing IP {i} of {total_ips}: {ip_address} ---")

        # Submit a new analysis request for the IP address
        rescan_url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip_address}/analyse"
        rescan_headers = {
            "accept": "application/json",
            "x-apikey": api_key
        }
        rescan_response = requests.post(rescan_url, headers=rescan_headers)
        print("Rescan requested:", rescan_response.status_code)

        # Submit a vote marking the IP address as malicious
        vote_url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip_address}/votes"
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
        comment_url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip_address}/comments"
        comment_payload = {
            "data": {
                "type": "comment",
                "attributes": {
                    "text": f"""Automated Comment
IP: {ip_address} - {reason}"""
                }
            }
        }
        comment_response = requests.post(comment_url, json=comment_payload, headers=headers)
        print("Comment posted:", comment_response.status_code)

        # Calculate and display progress and ETA
        progress = i / total_ips * 100
        remaining_time = (total_ips - i) * 60  #Each IP takes around 1 minute
        minutes_left = math.ceil(remaining_time / 60)

        # Display progress and estimated time left
        print(f"Progress: {i}/{total_ips} ({progress:.2f}%)")
        print(f"Estimated time left: {minutes_left} minute(s)")

        # Wait to stay within API call limits (4 calls per minute)
        print("Waiting 60 seconds before continuing...")
        time.sleep(60)
