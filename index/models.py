from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db.models.signals import post_save
from django.utils import timezone
from django.conf import settings
from smartfields import fields
from django_countries.fields import CountryField
from django.contrib.auth.models import Permission, User
from django.core.urlresolvers import reverse
from django.db import models


class Patient(models.Model):
    user = models.ForeignKey(User, default=1)
    first_name = models.CharField(max_length=250)
    last_name= models.CharField(max_length=500)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + ' - ' + self.last_name

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_username = models.CharField(max_length=250)
    date = models.CharField(max_length=250)

    def __str__(self):
        return self.doctor_username

class DocManager(BaseUserManager):
    """Create and manage users."""
    def create_user(self, first_name, last_name, email,
                    username=None, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")
        if not username:
            username = email.split('@')[0]

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, first_name, last_name, email, password,
        username=None):
        user = self.create_user(
            first_name,
            last_name,
            email,
            username,
            password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class Doctor(AbstractBaseUser, PermissionsMixin):
    """User model data."""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=40, unique=True, null=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = DocManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return "@{}".format(self.username)

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return "{} {} (@{})".format(self.first_name, self.last_name,
            self.username)


class DocProfile(models.Model):
    """User profile data."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    dob = models.DateTimeField(blank=True, null=True)
    avatar = fields.ImageField(upload_to='avatar_photos/', blank=True, null=True)
    location = models.CharField(max_length=40, blank=True, null=True)


def create_doc_profile(sender, instance, created, **kwargs):
    if created:
        DocProfile.objects.create(user=instance)

post_save.connect(create_doc_profile, sender=Doctor)