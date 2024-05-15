from django.core.management.base import BaseCommand, CommandError
from django.core.signing import Signer, TimestampSigner, salted_hmac
from django.utils.encoding import force_bytes
import logging
import time
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings

from core.utils.tokenizer import Tokenizer


logger = logging.getLogger("core")


class Command(BaseCommand):
    help = "Description of your command"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        logger.info("Running your command")
        # time.sleep(5)

        token = Tokenizer(sep=".").encode("test", "test2", compress=True)
        logger.info("Tokenizer Sign: " + token)

        logger.info("Tokenizer full: " +
                    Tokenizer(sep=".").encode_full("test", "test2", compress=True))
        # logger.info("Tokenizer Decode: " +
        #             urlsafe_base64_decode("eyJlbWFpbCI6InRlc3QifQ").decode())
        try:
            decoded_token = Tokenizer(sep=".").decode(
                "test", "test2",  token=token)
            logger.info("Tokenizer Decode: " + str(decoded_token))
        except Exception as e:
            logger.error("Error: " + str(e))
        # logger.info("Tokenizer Decode: " +
        #             urlsafe_base64_decode("eyJlbWFpbCI6InRlc3QifQ").decode())

        logger.info("Hmac Sign: " + salted_hmac("sdfljsop2390234.w3oufijf",
                    "test", settings.SECRET_KEY).hexdigest())
