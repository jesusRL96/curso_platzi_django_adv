from django.db import models
from cride.utils.models import CRideModel

class Rating(CRideModel):
    ride = models.ForeignKey('rides.Ride', on_delete=models.CASCADE, related_name='rated_ride')
    circle = models.ForeignKey('circles.Circle', on_delete=models.CASCADE)
    rating_user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, help_text='User that rates', related_name='raiting_user')
    rated_user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, help_text='User rated', related_name='rated_user')
    comments = models.TextField(blank=True)
    rating = models.IntegerField(default=1)

    def __str__(self):
        return f'ride# {self.ride.pk} rating: {self.rating}'