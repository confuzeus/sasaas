from django.conf import settings
from django.db import models


class Payment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="payments",
        null=True,
        blank=True,
    )
    source = models.CharField(max_length=40)
    reference = models.CharField(max_length=255)
    product_code = models.CharField(
        max_length=40, choices=settings.PRODUCT_CODE_CHOICES
    )
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment by {self.user.email} using {self.source} on {self.date}"
