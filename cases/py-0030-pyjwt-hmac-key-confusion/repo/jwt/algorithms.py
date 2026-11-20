import hashlib
import hmac
import json

from .exceptions import InvalidKeyError
from .utils import (
    base64url_decode,
    base64url_encode,
    der_to_raw_signature,
    force_bytes,
    from_base64url_uint,
    is_pem_format,
    is_ssh_key,
    raw_to_der_signature,
    to_base64url_uint,
)

try:
    import cryptography.exceptions
    from cryptography.exceptions import InvalidSignature
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import ec, padding
    from cryptography.hazmat.primitives.asymmetric.ec import (
        EllipticCurvePrivateKey,
        EllipticCurvePublicKey,
    )
    from cryptography.hazmat.primitives.asymmetric.ed448 import (
        Ed448PrivateKey,
        Ed448PublicKey,
    )
# [... lines 31-171 of the upstream file omitted ...]
class HMACAlgorithm(Algorithm):
    """
    Performs signing and verification operations using HMAC
    and the specified hash function.
    """

    SHA256 = hashlib.sha256
    SHA384 = hashlib.sha384
    SHA512 = hashlib.sha512

    def __init__(self, hash_alg):
        self.hash_alg = hash_alg

    def prepare_key(self, key):
        key = force_bytes(key)

        if is_pem_format(key) or is_ssh_key(key):
            raise InvalidKeyError(
                "The specified key is an asymmetric key or x509 certificate and"
                " should not be used as an HMAC secret."
            )

        return key

    @staticmethod
    def to_jwk(key_obj):
        return json.dumps(
            {
                "k": base64url_encode(force_bytes(key_obj)).decode(),
                "kty": "oct",
            }
        )

    @staticmethod
    def from_jwk(jwk):
        try:
            if isinstance(jwk, str):
                obj = json.loads(jwk)
            elif isinstance(jwk, dict):
                obj = jwk
            else:
                raise ValueError
        except ValueError:
            raise InvalidKeyError("Key is not valid JSON")

        if obj.get("kty") != "oct":
            raise InvalidKeyError("Not an HMAC key")

        return base64url_decode(obj["k"])

    def sign(self, msg, key):
        return hmac.new(key, msg, self.hash_alg).digest()

    def verify(self, msg, key, sig):
        return hmac.compare_digest(sig, self.sign(msg, key))


# [... lines 229-537 of the upstream file omitted ...]
    class OKPAlgorithm(Algorithm):
        """
        Performs signing and verification operations using EdDSA

        This class requires ``cryptography>=2.6`` to be installed.
        """

        def __init__(self, **kwargs):
            pass

        def prepare_key(self, key):
            if isinstance(key, (bytes, str)):
                if isinstance(key, str):
                    key = key.encode("utf-8")
                str_key = key.decode("utf-8")

                if "-----BEGIN PUBLIC" in str_key:
                    key = load_pem_public_key(key)
                elif "-----BEGIN PRIVATE" in str_key:
                    key = load_pem_private_key(key, password=None)
                elif str_key[0:4] == "ssh-":
                    key = load_ssh_public_key(key)

            # Explicit check the key to prevent confusing errors from cryptography
            if not isinstance(
                key,
                (Ed25519PrivateKey, Ed25519PublicKey, Ed448PrivateKey, Ed448PublicKey),
            ):
                raise InvalidKeyError(
                    "Expecting a EllipticCurvePrivateKey/EllipticCurvePublicKey. Wrong key provided for EdDSA algorithms"
                )

            return key

        def sign(self, msg, key):
            """
            Sign a message ``msg`` using the EdDSA private key ``key``
            :param str|bytes msg: Message to sign
# [... lines 576-677 of the upstream file omitted ...]
