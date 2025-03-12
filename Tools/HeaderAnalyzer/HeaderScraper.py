import email
from email.utils import parseaddr
import sys

def parse_email_header(header):
    email_message = email.message_from_string(header)
    
    parsed_info = {
        'From': parseaddr(email_message.get('From'))[1],
        'To': parseaddr(email_message.get('To'))[1],
        'Subject': email_message.get('Subject'),
        'Date': email_message.get('Date'),
        'Message-ID': email_message.get('Message-ID'),
        'Received': email_message.get_all('Received'),
        'Authentication-Results': email_message.get('Authentication-Results'),
        'DKIM-Signature': email_message.get('DKIM-Signature'),
        'SPF': email_message.get('Received-SPF'),
        'DMARC': email_message.get('DMARC-Results')
    }
    
    return parsed_info

def display_parsed_info(parsed_info):
    print("Here’s the extracted information from the email header:\n")
    for key, value in parsed_info.items():
        if isinstance(value, list):
            print(f"{key}:")
            for v in value:
                print(f"  - {v}")
        elif value:
            print(f"{key}: {value}")

def main():
    print("Welcome to the Email Header Analyzer!")
    print("-------------------------------------")
    print("Paste the raw email header Hit Enter\nThen press Ctrl+Z (Windows) or Ctrl+D (Mac/Linux) to finish input.\n")
    
    email_header = sys.stdin.read()
    
    parsed_info = parse_email_header(email_header)
    
    display_parsed_info(parsed_info)

if __name__ == "__main__":
    main()
