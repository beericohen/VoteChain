import base64
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Util.number import getPrime, inverse

class CryptoManager:
    """
    Manages cryptographic operations: Key generation, Signing, and Hashing.
    """
    
    @staticmethod
    def generate_keys(key_size=2048):
        """Generates an RSA key pair."""
        key = RSA.generate(key_size)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        return private_key, public_key

    @staticmethod
    def sign_data(private_key_pem, data):
        """Signs data using the private key."""
        key = RSA.import_key(private_key_pem)
        h = SHA256.new(data.encode('utf-8'))
        signature = pkcs1_15.new(key).sign(h)
        return base64.b64encode(signature).decode('utf-8')

    @staticmethod
    def verify_signature(public_key_pem, data, signature_b64):
        """Verifies a signature using the public key."""
        try:
            key = RSA.import_key(public_key_pem)
            h = SHA256.new(data.encode('utf-8'))
            signature = base64.b64decode(signature_b64)
            pkcs1_15.new(key).verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def get_hash(data):
        """Returns SHA-256 hash of data."""
        h = SHA256.new(data.encode('utf-8'))
        return h.hexdigest()

class BlindSignatureDemo:
    """
    Simulates the steps of a Blind Signature for educational visualization.
    In a real blind signature (Chaum), math involves m' = m * r^e (mod n).
    Here we separate the steps logically for the UI demo flow.
    """
    
    @staticmethod
    def blind(vote_content):
        """Step 1: Blind the vote (Simulated)."""
        # In a real scenario, we would multiply by a blinding factor.
        # For the demo, we hash it to represent the 'hidden' state.
        blinded_hash = SHA256.new(vote_content.encode('utf-8')).hexdigest()
        return blinded_hash

    @staticmethod
    def sign_blinded(private_key_pem, blinded_data):
        """Step 2: Government signs the blinded hash."""
        # Using standard signing on the blinded data
        return CryptoManager.sign_data(private_key_pem, blinded_data)

    @staticmethod
    def unblind(signature, blinding_factor=None):
        """Step 3: Unblind (In this demo, the signature becomes valid)."""
        # In real RSA blind sigs, s = s' * r^-1 (mod n).
        # We return the signature meant for the blockchain.
        return signature