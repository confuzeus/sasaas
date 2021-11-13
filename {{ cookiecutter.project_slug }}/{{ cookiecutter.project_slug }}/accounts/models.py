from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class MembershipType(models.Model):
    name = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    code = models.CharField(max_length=40, unique=True, db_index=True)
    group = models.OneToOneField(
        "auth.Group",
        verbose_name="Permissions group",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="membership_type",
    )

    def __str__(self):
        return self.name


class Membership(models.Model):
    membership_type = models.ForeignKey(
        MembershipType, on_delete=models.CASCADE, related_name="memberships"
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="membership", unique=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.membership_type.name}"
