from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None): # password collect is set false default
        """Create a new user profile"""
        if not email: # if email field is null
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        """ 위에서 정의한 사용자의 객체 정보대로 사용자 반환환"""
        return user
        
    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """"Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True) # True means anyother object is same
    name = models.CharField(max_length=255)\
    # for permission system
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # access permission settings

    objects = UserProfileManager() # to be made

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrive full name of user"""
        return self.name
    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of our user"""
        return self.email