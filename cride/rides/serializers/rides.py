from rest_framework import serializers

from cride.rides.models import Ride

from datetime import timedelta
from django.utils import timezone

class CreateRideSerializer(serializers.ModelSerializer):
    offered_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    available_seats = serializers.IntegerField(min_value=1, max_value=15)

    class Meta:
        """Meta class"""
        model = Ride
        exclude = ("passengers", "rating", "is_active", "offered_in")

    def validate_departure_date(self,data):
        """Verify date is not in the pass"""
        min_date = timezone.now() - timedelta(minutes=15)
        if data < min_date:
            serializers.ValidationError('Departure time must be at least passing the next 20 minutes window.')
        return data

