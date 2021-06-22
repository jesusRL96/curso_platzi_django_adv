from django.db import models

# Utilities
from cride.utils.models import CRideModel

class Profile(CRideModel, models.Model):
    """ Profile models
    holds user's public data"""

    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    picture = models.ImageField('profile picture', upload_to='users/pictures/', blank=True, null=True)
    biography = models.TextField(max_length=500, blank=True)
    # stats
    rides_taken = models.PositiveIntegerField(default=0)
    rides_offered = models.PositiveIntegerField(default=0)
    reputation = models.FloatField(
        default=0,
        help_text="User's reputation"
    )
    def __str__(self):
        """Return user's string representation"""
        return str(self.user)

