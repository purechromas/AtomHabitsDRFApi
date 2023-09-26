from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(_('Email address'), unique=True)

    telephone = models.CharField(_('Telephone'), unique=True, max_length=50, **NULLABLE)
    town = models.CharField(_('Town'), max_length=50, **NULLABLE)
    is_verified = models.BooleanField(_('Is verified'), default=False)
    verification_number = models.PositiveIntegerField(_('Verification number'), **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
