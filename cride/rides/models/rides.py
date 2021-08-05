from django.db import models

from cride.utils.models import CRideModel


class Ride(CRideModel):
    offered_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    offered_bin = models.ForeignKey('circles.Circle', on_delete=models.SET_NULL, null=True)

    passengers = models.ManyToManyField('users.User', related_name="passengers")

    available_seats = models.PositiveSmallIntegerField(default=1)
    comments = models.TextField(blank=True)

    deperture_location = models.CharField(max_length=255)
    deperture_date = models.DateTimeField()

    arrival_location = models.CharField(max_length=255)
    arrival_date = models.DateTimeField()

    rating = models.FloatField(null=True)

    is_active = models.BooleanField('active status', default=True, help_text='Used for disabling a ride or marking it finished.')

    def __str__(self):
        return f'{self.deperture_location} to {self.arrival_location} | {self.deperture_date.strftime("%a %d, %b")} {self.deperture_date.strftime("%I:%M %p")} - {self.arrival_date.strftime("%I:%M %p")}'



