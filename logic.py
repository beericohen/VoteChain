import hashlib
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

def generate_keys():
    """Generates an RSA key pair (Private and Public)."""
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def generate_file_signature(uploaded_file, private_key_bytes):
    """Signs the file hash using an RSA private key."""
    # Read file and create hash
    file_bytes = uploaded_file.read()
    h = SHA256.new(file_bytes)
    uploaded_file.seek(0) # Reset pointer
    
    # Sign the hash
    key = RSA.import_key(private_key_bytes)
    signature = pkcs1_15.new(key).sign(h)
    return signature

def verify_signature(original_file, signature_bytes, public_key_bytes):
    """Verifies the signature against the file using an RSA public key."""
    # Re-calculate hash of the uploaded file
    file_bytes = original_file.read()
    h = SHA256.new(file_bytes)
    original_file.seek(0)
    
    # Import the public key
    key = RSA.import_key(public_key_bytes)
    
    try:
        pkcs1_15.new(key).verify(h, signature_bytes)
        return True
    except (ValueError, TypeError):
        return False