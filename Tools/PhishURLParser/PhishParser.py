import base64
from urllib.parse import urlparse, parse_qs
import json

def parse_url_and_decode(url):
    url_obj = urlparse(url)
    params = parse_qs(url_obj.query)
    decoded_params = {}

    for key, values in params.items():
        value = values[0]
        try:
            if base64.b64encode(base64.b64decode(value)).decode() == value:
                decoded_params[key] = base64.b64decode(value).decode()
            else:
                decoded_params[key] = value
        except Exception:
            decoded_params[key] = value

    return decoded_params

url = input("Enter URL: ")
result = parse_url_and_decode(url)
print(json.dumps(result, indent=4))
