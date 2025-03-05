#Attempt to pull the HTML if the page is detecting URLScan or other tools as a proxy and refusing to load or redirecting too fast.
import requests

url = ""

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("HTML content retrieved successfully!")
    
    if 'gzip' in response.headers.get('Content-Encoding', ''):
        content = response.content
        try:
            print(content.decode('utf-8'))
        except UnicodeDecodeError:
            print("The content is not UTF-8 encoded.")
            print(content)
    else:
        print(response.text)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
