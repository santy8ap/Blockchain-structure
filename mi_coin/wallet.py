# wallet.py
import ecdsa
import hashlib
import binascii

def generate_keypair():
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    private_key = binascii.hexlify(sk.to_string()).decode()
    public_key = binascii.hexlify(vk.to_string()).decode()
    return private_key, public_key

def sign_message(private_key_hex: str, message: str) -> str:
    sk_bytes = binascii.unhexlify(private_key_hex)
    sk = ecdsa.SigningKey.from_string(sk_bytes, curve=ecdsa.SECP256k1)
    sig = sk.sign(message.encode())
    return binascii.hexlify(sig).decode()

def verify_signature(public_key_hex: str, message: str, signature_hex: str) -> bool:
    try:
        vk_bytes = binascii.unhexlify(public_key_hex)
        vk = ecdsa.VerifyingKey.from_string(vk_bytes, curve=ecdsa.SECP256k1)
        sig = binascii.unhexlify(signature_hex)
        return vk.verify(sig, message.encode())
    except Exception:
        return False

def pubkey_to_address(public_key_hex: str) -> str:
    # Simple address: ripemd160(sha256(pubkey)) encoded hex
    pub_bytes = binascii.unhexlify(public_key_hex)
    sha = hashlib.sha256(pub_bytes).digest()
    rip = hashlib.new('ripemd160', sha).hexdigest()
    return rip
