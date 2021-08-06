import uuid
import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.conf import settings


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/recipe/', filename)


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
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):  # give us the features from django user model
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)  # columns in database
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)  # when user is created, it is active
    is_staff = models.BooleanField(default=False)  # actived user is not staff

    objects = UserManager()

    USERNAME_FIELD = 'email'  # customize username field to email


class Tag(models.Model):
    """Tag to be used for a recipe"""
    name = models.CharField(max_length=255)  # columns in database
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # if you delete user, delete models as well
    )

    def __str__(self):
        return self.name  # add string representation of the model


class Ingredient(models.Model):
    """Ingredient to be used in a recipe"""
    name = models.CharField(max_length=255)  # columns in database
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Foreign key to AUTH_USER_MODEL
        on_delete=models.CASCADE
    )  # columns in database
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')
    # not required and pass reference to function (no parentheses)
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title  # why?
