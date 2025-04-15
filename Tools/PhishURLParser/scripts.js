function parseUrlAndDecode(url) {
    const urlObj = new URL(url);
    const params = new URLSearchParams(urlObj.search);
    const decodedParams = {};

    for (const [key, value] of params.entries()) {
        try {
            if (typeof value === 'string' && btoa(atob(value)) === value) {
                decodedParams[key] = atob(value);
            } else {
                decodedParams[key] = value;
            }
        } catch (e) {
            decodedParams[key] = value;
        }
    }

    return decodedParams;
}

function parseAndDecode() {
    const url = document.getElementById('urlInput').value;
    const result = parseUrlAndDecode(url);
    document.getElementById('output').textContent = JSON.stringify(result, null, 2);
}
