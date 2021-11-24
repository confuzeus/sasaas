from django.conf import settings
from django import template

register = template.Library()


@register.simple_tag()
def get_paddle_data():
    return {
        "vendor_id": settings.PADDLE_VENDOR_ID,
        "credit_pack_product_id": settings.PADDLE_CREDIT_PACK_PRODUCT_ID,
    }
