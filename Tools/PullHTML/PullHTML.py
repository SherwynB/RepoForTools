import requests

url = input("Enter a URL to fetch HTML content: ")

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

except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
