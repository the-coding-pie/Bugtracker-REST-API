from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class UserManager(BaseUserManager):
    def create_user(self, email, username, is_active=True, is_admin=False, password=None):
        if not email:
            raise ValueError('Email is required!')
        if not username:
            raise ValueError('Username is required!')
        
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        user.set_password(password)
        user.is_active = is_active
        user.is_admin = is_admin 
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
            is_active=True,
            is_admin=True
        )
        return user

class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png')
   
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

@receiver(post_save, sender=User)
def create_token(sender, instance=None, created=False, **kwargs):
    # first time user is created, create will be True
    if created:
        Token.objects.create(user=instance) 