from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)  # creates new user model
        user.set_password(password)  # sets the password
        user.save(using=self._db)  # save the model

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_super_user = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):  # give us the features from django user model
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)  # when user is created, it is active
    is_staff = models.BooleanField(default=False)  # actived user is not staff

    objects = UserManager()

    USERNAME_FIELD = 'email'  # customize username field to email

