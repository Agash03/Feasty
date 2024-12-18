from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    age = models.IntegerField(default=0)
    phone = models.CharField(null=True, max_length=50)