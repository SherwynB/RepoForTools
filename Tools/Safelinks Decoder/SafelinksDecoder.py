
import urllib.parse

def extract_safelinks_components(safelinks_url):
    #Parse the SafeLinks URL
    parsed_url = urllib.parse.urlparse(safelinks_url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    
    #Extract url
    original_url = query_params.get('url', [None])[0]
    if original_url:
        original_url = urllib.parse.unquote(original_url)
    
    #Extract other components
    data = query_params.get('data', [None])[0]
    sdata = query_params.get('sdata', [None])[0]
    reserved = query_params.get('reserved', [None])[0]
    
    return {
        'original_url': original_url,
        'data': data,
        'sdata': sdata,
        'reserved': reserved
    }

#user input
safelinks_url = input("SafeLinks URL: ")
components = extract_safelinks_components(safelinks_url)

print("\nExtracted SafeLinks Components:")
print(f"{'Original URL:':<15} {components['original_url']}")
print(f"{'Data:':<15} {components['data']}")
print(f"{'Sdata:':<15} {components['sdata']}")
print(f"{'Reserved:':<15} {components['reserved']}")