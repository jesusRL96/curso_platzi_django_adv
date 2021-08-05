from rest_framework import serializers

from cride.rides.models import Ride
from cride.circles.models import Membership, memberships

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

    def validate(self, data):
        user = data['offered_by']
        circle = self.context['circle']
        if self.context['request'].user != user:
            raise serializers.ValidationError('Rides offered on behalf of others are not allowed.')
        try:
            membership = Membership.objects.get(user=user, circle=circle, is_active=True)
        except Membership.DoesNotExist:
            raise serializers.ValidationError('User is not an active member of the circle.')

        if data['arrival_date'] <= data['departure_date']:
            raise serializers.ValidationError('Departure date must happen after arrival date.')
        self.context['membership'] = membership
        return data

    def create(self, data):
        circle = self.context['circle']
        ride = Ride.objects.create(**data, offered_in=circle)

        # Circle
        circle.rides_offered += 1
        circle.save()
        # Membership
        membership = self.context['membership']
        membership.rides_offered += 1
        membership.save()
        # profile
        profile = data['offered_by'].profile
        profile.rides_offered += 1
        profile.save()

        return ride

class RideModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = "__all__"
        read_only_fields = ('offered_by', 'offered_in', 'rating')