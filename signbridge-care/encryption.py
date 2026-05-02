import os
import json
from cryptography.fernet import Fernet

class SecureStorage:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        key_path = "data/key.key"
        if os.path.exists(key_path):
            with open(key_path, "rb") as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            with open(key_path, "wb") as f:
                f.write(self.key)
        self.cipher = Fernet(self.key)

    def encrypt(self, data):
        if isinstance(data, dict):
            data = json.dumps(data, ensure_ascii=False)
        if isinstance(data, str):
            data = data.encode()
        return self.cipher.encrypt(data).decode()

    def decrypt(self, data):
        dec = self.cipher.decrypt(data.encode())
        try:
            return json.loads(dec)
        except:
            return dec.decode()

    def save(self, data, path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.encrypt(data))

    def load(self, path):
        if not os.path.exists(path):
            return {}
        with open(path, "r", encoding="utf-8") as f:
            enc = f.read()
        return self.decrypt(enc)