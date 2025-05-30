from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_business_owner = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)

    def __str__(self):
        return self.email
