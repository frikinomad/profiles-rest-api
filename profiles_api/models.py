#building a cusotm model rather than using the default django model, and saving it in profiles_project/settings.py file, and
#after changing the setting we'll make the migration which will create a migrations folder and 0001_initial.py file which will have tne model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager     #default userManger by django


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, name, email, password=None):
        if not email:
            raise ValueError('User must provide an Email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)     #in this way the password will be encrypted & stored in hash form
        user.save(using=self.db)        #here we can use any db of our choice to save the data

        return user

    def create_superuser(self, name, email, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(name, email, password)

        user.is_superuser=True  #this superuesr is created by the PermissionsMixin that we have imported
        user.is_staff=True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database Models for user in the system"""    #doc string to define about the class
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)   #setting default use as actice
    is_staff = models.BooleanField(default=False)   #to set admin privilages

    #to tell django how to use this custom model in the command line, allows admin user to make changes
    objects = UserProfileManager()    #the deafult django model requires a password and a name field but we have changes it to name and email


    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = ['name']

    def get_full_name(self):
        """Retreive name of the User"""
        return self.name

    def get_full_name(self):
        """Retreive name of the User"""
        return self.name

    def __str__(self):      #not required but recommended
        """Return string representation of the user"""
        return self.email
