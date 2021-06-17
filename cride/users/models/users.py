"""User Model"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

# Utilities
from cride.utils.models import CRideModel

class User(CRideModel, AbstractUser):
    """ User Model.
    Extends from django's Abstract user, change from username field to email and add some extra fields
    """
    email = models.EmailField('email address', unique=True, error_messages={
        'unique': 'A user with that email already exists.'
    })
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +99999999. Up to 15 digits allowed."
    )
    phone_number = models.CharField(max_length=17, blank=True, validators=[phone_regex,])
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    is_client = models.BooleanField('client status', default=True, help_text=(
        'Helps easily distinguish users and perform queries. '
        'Clients are the main type of user.'
    ))

    is_verified = models.BooleanField('veridied', default=False, help_text='Set to true whe user verifies its email.')

    def __str__(self):
        """Returns username."""
        return self.username