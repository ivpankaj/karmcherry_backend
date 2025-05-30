from django.db import models
from users.models import User

class Business(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='business')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
