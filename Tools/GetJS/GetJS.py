import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = input("Enter a URL to fetch HTML content and JavaScript: ")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}

try:
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
        print("HTML content retrieved successfully!")

        soup = BeautifulSoup(response.text, 'html.parser')
        script_tags = soup.find_all('script', src=True)

        js_urls = [urljoin(url, script['src']) for script in script_tags]

        if not js_urls:
            print("No external JavaScript files found.")
        else:
            for js_url in js_urls:
                try:
                    js_response = requests.get(js_url, headers=headers, timeout=10)
                    if js_response.status_code == 200:
                        print(f"\nJavaScript from {js_url}:\n")
                        print(js_response.text)
                    else:
                        print(f"Failed to fetch JS file: {js_url} (Status code: {js_response.status_code})")
                except requests.RequestException as js_e:
                    print(f"Error fetching JavaScript file {js_url}: {js_e}")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
