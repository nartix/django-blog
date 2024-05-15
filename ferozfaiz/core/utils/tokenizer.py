from django.core.signing import TimestampSigner, b64_encode, b64_decode, JSONSerializer
from django.utils.encoding import force_bytes
import zlib
import logging

logger = logging.getLogger("core")


class BaseTokenizer:
    def __init__(self, salt=None, sep='.', key=None):
        self.salt = salt
        self.sep = sep
        self.key = key
        self.signer = TimestampSigner(
            salt=self.salt, sep=self.sep, key=self.key)

    def _build_object(self, *args, **kwargs):
        token = kwargs.pop("token", None)
        max_age = kwargs.pop("max_age", None)
        compress = kwargs.pop("compress", False)
        data = self._handle_args_and_kwargs(args, kwargs)
        return data, token, max_age, compress

    def _handle_args_and_kwargs(self, args, kwargs):
        if len(args) == 1 and isinstance(args[0], (dict, list)):
            return args[0]
        if kwargs:
            return kwargs
        if len(args) == 1:
            return args[0]
        return list(args)

    def _unsign(self, token, max_age):
        return self.signer.unsign_object(token, max_age=max_age)

    def _sign(self, data, compress):
        return self.signer.sign_object(data, compress=compress)

    def encode(self, *args, **kwargs):
        data, _, __, compress = self._build_object(*args, **kwargs)
        return self._sign(data, compress)

    # Will raise a SignatureExpired or BadSignature exception if the token is invalid
    def decode(self, *args, **kwargs):
        data, token, max_age, compress = self._build_object(*args, **kwargs)
        return self._unsign(token, max_age=max_age)


class Tokenizer(BaseTokenizer):
    def __init__(self, salt=None, sep='.', key=None):
        super().__init__(salt=salt, sep=sep, key=key)

    def _encode_base64(self, data):
        return b64_encode(data).decode()

    def encode_full(self, *args, **kwargs):
        data, _, __, compress = self._build_object(*args, **kwargs)
        return self._sign(data, compress)

    def encode(self, *args, **kwargs):
        return self.remove_data(self.encode_full(*args, **kwargs))

    def decode(self, *args, **kwargs):
        data, token, max_age, compress = self._build_object(*args, **kwargs)

        data = JSONSerializer().dumps(data)
        is_compressed = False

        if compress:
            # Avoid zlib dependency unless compress is being used.
            compressed = zlib.compress(data)
            if len(compressed) < (len(data) - 1):
                data = compressed
                is_compressed = True
                logger.info("Compressed: " + str(data))

        base64d = self._encode_base64(data)
        if is_compressed:
            base64d = "." + base64d

        token = f"{base64d}{self.sep}{token}"
        return self._unsign(token, max_age=max_age)

    def remove_data(self, token):
        return token.split(self.sep, 1)[1]


class Base64Tokenizer(BaseTokenizer):
    def __init__(self, salt=None, sep='.', key=None):
        super().__init__(salt=salt, sep=sep, key=key)

    def _encode_base64(self, data):
        return b64_encode(force_bytes(data)).decode()

    def _encode_data(self, data):
        return self.signer.sign(self._encode_base64(data))

    def encode_full(self, *args, **kwargs):
        data, _, __, compress = self._build_object(*args, **kwargs)
        return self._encode_data(data)

    def encode(self, *args, **kwargs):
        return self.remove_data(self.encode_full(*args, **kwargs))

    def _decode_base64(self, token):
        return b64_decode(force_bytes(token)).decode()

    def _decode_data(self, token, max_age):
        return self._decode_base64(self.signer.unsign(token, max_age=max_age))

    # Will raise a SignatureExpired or BadSignature exception if the token is invalid
    def decode(self, *args, **kwargs):
        data, token, max_age, _ = self._build_object(*args, **kwargs)
        encoded_data = self._encode_base64(data)
        token = f"{encoded_data}{self.sep}{token}"
        return self._decode_data(token, max_age=max_age)

    def remove_data(self, token):
        return token.split(self.sep, 1)[1]
