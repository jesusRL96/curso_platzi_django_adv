from django.db import models

from cride.utils.models import CRideModel

class Circle(CRideModel):
    """Cirle model
    private group"""
    name = models.CharField('circle name', max_length=140)
    slug_name = models.SlugField('slug name', max_length=140, unique=True)

    about = models.CharField('circle description', max_length=255)
    picture = models.ImageField('circle picture', upload_to='circles/pictures/', blank=True, null=True)
    # stats
    rides_offered = models.PositiveIntegerField(default=0)
    rides_taken = models.PositiveIntegerField(default=0)

    verified = models.BooleanField('verified circle', default=False, help_text="verified circles are officials communities")
    is_public = models.BooleanField(default=False, help_text="public circle")

    is_limited = models.BooleanField(default=False, help_text="limited circles")
    limit = models.PositiveIntegerField(default=0, help_text="limit")

    members = models.ManyToManyField('users.User', through='circles.Membership', through_fields=('circle', 'user'))

    def __str__(self):
        return self.name

    class Meta(CRideModel.Meta):
        """Class meta"""
        ordering = ['-rides_taken', '-rides_offered']