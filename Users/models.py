from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.hashers import make_password, identify_hasher


class Users(AbstractBaseUser):
    username = models.CharField(max_length=20 , unique=True)
    password = models.CharField(max_length=200)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    phone = models.CharField(max_length=11 , unique=True)
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True , default='')
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'username'

    def __str__(self):
        return f"username:{self.username}, first_name:{self.first_name}, last_name:{self.last_name}"

    def save(self, *args, **kwargs):
        try:
            identify_hasher(self.password)
        except ValueError:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)