
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature
import os

KEY_DIR = "keys"

class DigitalSignature:
    def __init__(self):
        if not os.path.exists(KEY_DIR):
            os.makedirs(KEY_DIR)
        self.private_key = None
        self.public_key = None

    def generate_keys(self):
        self.private_key = ec.generate_private_key(ec.SECP256R1())
        self.public_key = self.private_key.public_key()
        self.save_keys()

    def save_keys(self):
        with open(f"{KEY_DIR}/private_key.pem", "wb") as f:
            f.write(self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        with open(f"{KEY_DIR}/public_key.pem", "wb") as f:
            f.write(self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

    def load_keys(self):
        with open(f"{KEY_DIR}/private_key.pem", "rb") as f:
            self.private_key = serialization.load_pem_private_key(f.read(), password=None)
        with open(f"{KEY_DIR}/public_key.pem", "rb") as f:
            self.public_key = serialization.load_pem_public_key(f.read())

    def sign_message(self, message: str) -> bytes:
        return self.private_key.sign(message.encode(), ec.ECDSA(hashes.SHA256()))

    def verify_signature(self, message: str, signature: bytes) -> str:
        try:
            self.public_key.verify(signature, message.encode(), ec.ECDSA(hashes.SHA256()))
            return " VALID SIGNATURE"
        except InvalidSignature:
            return " INVALID SIGNATURE"
