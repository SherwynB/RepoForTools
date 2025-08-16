import hashlib
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

# PureLogs Stealer Sample - Build: test120922139213
def decrypt_purelogs(ciphertext: bytes) -> bytes:
    password = "1Z11wTrtsFc2ElgroUCsBHiSCgDJR10wV8SZ0IiP53cFzgsdKYIDGMdEHsogfICrEG6vsh"
    key_material = hashlib.sha512(password.encode("utf-8")).digest()
    salt = bytes([
        0x75, 0x2D, 0x9E, 0xFD, 0xB8, 0xAC, 0x60, 0x9E,
        0xEF, 0x7D, 0x1E, 0x46, 0x91, 0xE1, 0x03, 0xA1
    ])
    derived = PBKDF2(key_material, salt, dkLen=48, count=1000)
    key, iv = derived[:32], derived[32:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext_padded = cipher.decrypt(ciphertext)
    pad_len = plaintext_padded[-1]
    return plaintext_padded[:-pad_len]

if __name__ == "__main__":
    encrypted_data = b"..."
    decrypted = decrypt_purelogs(encrypted_data)
    print("Decrypted output:\n", decrypted.decode(errors="ignore"))
