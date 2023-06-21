"""
create the database models

"""

from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.core.validators import MinValueValidator, MaxValueValidator


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(user=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError('User must have an email address to create')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(blank=False, max_length=255, unique=True)
    name = models.CharField(blank=False, max_length=200)
    joining_date = models.DateTimeField(auto_now_add=True)
    birthday = models.DateField(blank=True, null=True, verbose_name='Date of Birth', help_text='Enter your birthdate')
    major = models.CharField(blank=True, max_length=70)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    @classmethod
    def get_users(cls):
        return User.objects.all()

    @classmethod
    def user_birthday_greater_than_2016(cls):
        return User.objects.filter(birthday__year__gt=2016)


class Patron(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    birthday = models.DateField(blank=True, null=True, verbose_name='Date of Birth', help_text='Enter your birthdate')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    author = models.ForeignKey(Patron, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    price = models.FloatField(
        validators=[
            MinValueValidator(10),
            MaxValueValidator(200)
        ]
    )
    publication_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}, by {self.author.name}"

