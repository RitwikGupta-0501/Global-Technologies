from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    company_name = models.CharField(max_length=300, blank=True, null=True)
