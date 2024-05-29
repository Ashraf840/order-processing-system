from django.db import models
import uuid
from django.contrib.auth.models import User

class Address(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)    # Even after removing the user account, the address might be useful for further geo-location analytics
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    postal_code = models.CharField(max_length=50)
    country = models.CharField(max_length=150)
    is_default_shipping_address = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user}-{self.street}-{self.created_at}"
