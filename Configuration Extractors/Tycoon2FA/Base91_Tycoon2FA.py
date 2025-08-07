import base64
from Crypto.Cipher import AES
import base91

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

decoded = base91.decode(decrypted.decode('utf-8'))

print(decoded.decode('utf-8'))
