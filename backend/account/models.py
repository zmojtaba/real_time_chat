from django.db import models
from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractBaseUser

import sys
# sys.path.append('../../')

from utilss.user_message import io




class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            io._error("This Field is requred!")
        username = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            io._error("Superuser must have is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            io._error("Superuser must have is_superuser=True")
        return self.create_user(username, password, **extra_fields)
    


class UserType(models.TextChoices):
    EMPLOYEE = 'ee', 'Employee'
    EMPLOYER = 'er', 'Employer'



class User(AbstractBaseUser, PermissionsMixin):
    username        = models.CharField(max_length=255, unique=True)
    email           = models.EmailField(max_length=255, blank=True, null=True)
    phone           = models.CharField(max_length=13, blank=True, null=True)
    type            = models.CharField( max_length=2, choices=UserType.choices, default=UserType.EMPLOYEE )
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_verified     = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    objects = UserManager()

    def __str__(self):
        return self.username