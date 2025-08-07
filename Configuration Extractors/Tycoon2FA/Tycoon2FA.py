import base64
from Crypto.Cipher import AES
import re

data_b64 = ""
key_b64 = ""

key = base64.b64decode(key_b64)
data = base64.b64decode(data_b64)

iv = data[:16]
ciphertext = data[16:]

cipher = AES.new(key, AES.MODE_CBC, iv)

decrypted = cipher.decrypt(ciphertext)
padding_len = decrypted[-1]
decrypted = decrypted[:-padding_len]

decoded_str = decrypted.decode('utf-8')

#Output still has atob
match = re.search(r'atob\("([^"]+)"\)', decoded_str)
if match:
    inner_b64 = match.group(1)
    inner_decoded = base64.b64decode(inner_b64)
    print(inner_decoded.decode('utf-8'))
else:
    print(decoded_str)

#final output is encoded by javascript obfuscator