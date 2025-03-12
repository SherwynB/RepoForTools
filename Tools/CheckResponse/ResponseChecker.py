import requests
import random
from bs4 import BeautifulSoup, Comment

def get_robust_headers():
    headers = {
        'User-Agent': random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
        ]),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.google.com/',
        'TE': 'Trailers'
    }
    return headers

def check_domain_status(domain):
    try:
        if not domain.startswith(('http://', 'https://')):
            if domain.startswith('www.'):
                domain = 'https://' + domain
            else:
                domain = 'https://' + domain

        headers = get_robust_headers()
        response = requests.get(domain, headers=headers, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Search for the comment <!-- Food Section -->
            food_section_comment = soup.find_all(string=lambda text: isinstance(text, Comment) and "Food Section" in text)

            if food_section_comment:
                return f"{domain}: OK - 'Food Section' comment found"
            else:
                # Debugging: Checking the HTML when 'Food Section' comment is not found
                # print(f"DEBUGGING: {domain} - 'Food Section' comment not found. HTML snippet: {response.text}")
                return f"{domain}: OK - 'Food Section' comment not found"
        else:
            return f"{domain}: Status Code {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"{domain}: Error - {str(e)}"

def check_domains_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            domains = file.readlines()
        
        # Separate the results into different categories
        ok_domains = []
        other_domains = []

        for domain in domains:
            domain = domain.strip()
            if domain:
                result = check_domain_status(domain)
                if "OK" in result:
                    ok_domains.append(result)
                else:
                    other_domains.append(result)

        # Print other domains first
        for result in other_domains:
            print(result)

        # Print all the OK domains at the bottom for ease of reading
        if ok_domains:
            print("\n--- HTTP 200 OK Domains ---")
            for result in ok_domains:
                print(result)

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    file_path = input("Enter the path to the text file with domains: ").strip()
    check_domains_from_file(file_path)
