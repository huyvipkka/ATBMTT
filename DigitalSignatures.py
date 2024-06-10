from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

def RSASign(data: str, private_key: RSA.RsaKey) -> bytes:
    hash_data = SHA256.new(data.encode())
    return pkcs1_15.new(private_key).sign(hash_data)

def RSAVerify(data: str, signature: bytes, public_key: RSA.RsaKey) -> bool:
    hash_data = SHA256.new(data.encode())
    try:
        pkcs1_15.new(public_key).verify(hash_data, signature)
        return True
    except ValueError:
        return False
    
