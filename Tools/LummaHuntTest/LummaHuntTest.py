import dns.resolver
import requests
import pandas as pd
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

def resolve_domain(domain):
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ['8.8.8.8', '8.8.4.4']
        result = resolver.resolve(domain, 'A')
        return result[0].to_text()
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return None

# Generate headers to mimic a browser
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


def get_http_response(url):
    try:
        headers = get_robust_headers()
        response = requests.get(url, headers=headers, timeout=10)
        return response.status_code
    except requests.exceptions.RequestException:
        return None

# Check reachability of domain and IP
# Lumma looks to be using a /1337/ directory on their domain
def check_domain_reachability(domain, reachable_domains, status_code_results):
    ip_address = resolve_domain(domain)
    
    if ip_address:
        http_status = get_http_response(f'http://{domain}/1337/')
        https_status = get_http_response(f'https://{domain}/1337/')
        http_ip_status = get_http_response(f'http://{ip_address}/1337/')
        https_ip_status = get_http_response(f'https://{ip_address}/1337/')
        
        reachable_domains.append({
            'domain': domain,
            'ip': ip_address,
            'http_domain': http_status,
            'https_domain': https_status,
            'http_ip': http_ip_status,
            'https_ip': https_ip_status
        })

        if any(status is not None for status in [http_status, https_status, http_ip_status, https_ip_status]):
            status_code_results.append({
                'domain': domain,
                'ip': ip_address,
                'http_domain': http_status,
                'https_domain': https_status,
                'http_ip': http_ip_status,
                'https_ip': https_ip_status
            })

# Read CSV and check domains
def check_domains_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    
    reachable_domains = []
    status_code_results = []

    tasks = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        for index, row in df.iterrows():
            domain = row.iloc[0]  # Use iloc to access the first column by position
            tasks.append(executor.submit(check_domain_reachability, domain, reachable_domains, status_code_results))
        
        for future in as_completed(tasks):
            pass

    #Read Domains
    print("\nSummary of All Domains and Their URLs:")
    if reachable_domains:
        for entry in reachable_domains:
            print(f"- Domain: {entry['domain']}, IP: {entry['ip']}")
            if entry['http_domain'] is not None:
                print(f"  HTTP URL (Domain): http://{entry['domain']}/1337/ - Status Code: {entry['http_domain']}")
            if entry['https_domain'] is not None:
                print(f"  HTTPS URL (Domain): https://{entry['domain']}/1337/ - Status Code: {entry['https_domain']}")
            if entry['http_ip'] is not None:
                print(f"  HTTP URL (IP): http://{entry['ip']}/1337/ - Status Code: {entry['http_ip']}")
            if entry['https_ip'] is not None:
                print(f"  HTTPS URL (IP): https://{entry['ip']}/1337/ - Status Code: {entry['https_ip']}")
    
    #Print Domains
    print("\nReachable Domains with Status Codes:")
    if status_code_results:
        for entry in status_code_results:
            print(f"- Domain: {entry['domain']}, IP: {entry['ip']}")
            if entry['http_domain'] is not None:
                print(f"  HTTP URL (Domain): http://{entry['domain']}/1337/ - Status Code: {entry['http_domain']}")
            if entry['https_domain'] is not None:
                print(f"  HTTPS URL (Domain): https://{entry['domain']}/1337/ - Status Code: {entry['https_domain']}")
            if entry['http_ip'] is not None:
                print(f"  HTTP URL (IP): http://{entry['ip']}/1337/ - Status Code: {entry['http_ip']}")
            if entry['https_ip'] is not None:
                print(f"  HTTPS URL (IP): https://{entry['ip']}/1337/ - Status Code: {entry['https_ip']}")


def main():
    csv_file = 'results.csv'  # Path to CSV
    check_domains_from_csv(csv_file)

if __name__ == '__main__':
    main()
