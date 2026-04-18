import os
import json
import base64
from cryptography.fernet import Fernet


class SecureStorage:
    def __init__(self):
        self.key_file = "data/key.key"
        os.makedirs("data", exist_ok=True)

        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(self.key)

        self.cipher = Fernet(self.key)

    def encrypt(self, data):
        if isinstance(data, dict):
            data = json.dumps(data, ensure_ascii=False)
        if isinstance(data, str):
            data = data.encode()
        return self.cipher.encrypt(data).decode()

    def decrypt(self, data):
        decrypted = self.cipher.decrypt(data.encode())
        try:
            return json.loads(decrypted)
        except:
            return decrypted.decode()

    def save(self, data, path):
        encrypted = self.encrypt(data)
        with open(path, "w", encoding="utf-8") as f:
            f.write(encrypted)

    def load(self, path):
        if not os.path.exists(path):
            return {}
        with open(path, "r", encoding="utf-8") as f:
            encrypted = f.read()
        return self.decrypt(encrypted)