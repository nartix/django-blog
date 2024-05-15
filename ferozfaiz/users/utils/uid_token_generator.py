from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str


def create_signed_user_token(user):
    uid = urlsafe_base64_encode(force_bytes(f"{user.pk}_"))
    signer = TimestampSigner()
    signed_token = signer.sign(uid)
    return signed_token


def get_user_id_from_token(token, max_age=None):
    signer = TimestampSigner()
    try:
        uid = signer.unsign(token, max_age=max_age)
    except BadSignature:
        raise ValueError("Invalid token")
    except SignatureExpired:
        raise ValueError("Expired token")

    try:
        decoded_uid = force_str(urlsafe_base64_decode(uid))
        user_id = int(decoded_uid.split("_")[0])
        return user_id
    except IndexError:
        raise ValueError("Invalid user id")
