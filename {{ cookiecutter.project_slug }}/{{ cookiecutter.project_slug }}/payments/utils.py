import logging
import collections
import base64
from decimal import Decimal
from functools import cached_property

import phpserialize
from django.conf import settings
from django.contrib.auth import get_user_model

from Crypto.PublicKey import RSA

from {{ cookiecutter.project_slug }}.payments.models import Payment

try:
    from Crypto.Hash import SHA1
except ImportError:
    from Crypto.Hash import SHA as SHA1
try:
    from Crypto.Signature import PKCS1_v1_5
except ImportError:
    from Crypto.Signature import pkcs1_15 as PKCS1_v1_5

User = get_user_model()

log = logging.getLogger(__name__)


class Paddle:
    def __init__(self, data):
        self.data = data.copy()
        self.signature = data["p_signature"]
        del self.data["p_signature"]

        self.currency = data["p_currency"]
        self.product_id = int(data["p_product_id"])
        self.order_id = data["p_order_id"]
        self.total = Decimal(data["p_price"])
        self.qty = int(data["p_quantity"])
        email = data["email"]
        self.email = email
        self.user = User.objects.get(email=email)

    @cached_property
    def is_valid(self):
        """
        Verify the signature.
        """
        # Convert key from PEM to DER - Strip the first and last lines and newlines, and decode
        public_key_encoded = settings.PADDLE_PUBLIC_KEY[26:-25].replace("\n", "")
        public_key_der = base64.b64decode(public_key_encoded)

        # input_data represents all of the POST fields sent with the request
        # Get the p_signature parameter & base64 decode it.

        # Remove the p_signature parameter

        # Ensure all the data fields are strings
        for field in self.data:
            self.data[field] = str(self.data[field])

        # Sort the data
        sorted_data = collections.OrderedDict(sorted(self.data.items()))

        # and serialize the fields
        serialized_data = phpserialize.dumps(sorted_data)

        # verify the data
        key = RSA.importKey(public_key_der)
        digest = SHA1.new()
        digest.update(serialized_data)
        verifier = PKCS1_v1_5.new(key)
        signature = base64.b64decode(self.signature)
        if verifier.verify(digest, signature):
            return True
        return False

    def record_payment(self, product_code):
        payment = Payment(
            user=self.user,
            source="paddle",
            reference=self.order_id,
            product_code=product_code,
            total=self.total,
        )
        payment.full_clean()
        payment.save()
        log.info(f"Recorded a payment of {self.currency} {self.total} by {self.email}.")

    def add_credits(self):
        total_credits = self.qty * settings.PADDLE_CREDITS_PER_PACK
        self.user.credit_wallet.credits += total_credits
        self.user.credit_wallet.save()
        log.info(f"Added {total_credits} credits to {self.user.credit_wallet}")

    def process_webhook(self):
        if self.product_id == settings.PADDLE_CREDIT_PACK_PRODUCT_ID:
            self.record_payment(settings.CREDIT_PRODUCT_CODE)
            self.add_credits()
