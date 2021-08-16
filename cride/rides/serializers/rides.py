from rest_framework import serializers

from cride.users.serializers import UserModelSerializer

from cride.rides.models import Ride
from cride.users.models import User
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
class JoinRideSerializer(serializers.ModelSerializer):
    passenger = serializers.IntegerField()

    class Meta:
        """Meta class"""
        model = Ride
        fields = ("passenger",)

    def validate_passenger(self, data):
        try:
            user = User.objects.get(pk=data)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid passenger.')
        circle = self.context['circle']
        try:
            member = Membership.objects.get(user=user, circle=circle, is_active=True)
        except Membership.DoesNotExist:
            raise serializers.ValidationError('User is not an active member of the circle.')
        self.context['user'] = user
        self.context['member'] = member
        return data

    def validate(self, data):
        offset = timezone.now() - timedelta(minutes=15)
        ride = self.context['ride']
        if ride.departure_date <= offset:
            raise serializers.ValidationError("You can't join this ride now.")
        if ride.available_seats < 1:
            raise serializers.ValidationError("Ride is already full.")
        if Ride.objects.filter(passengers__pk=data['passenger']):
            raise serializers.ValidationError("Passenger is already in this ride.")

        return data

    def update(self, instance, data):
        ride = instance
        user = self.context['user']
        circle = self.context['circle']

        ride.passengers.add(user)
        profile = user.profile
        profile.rides_taken += 1
        profile.save()

        member = self.context['member']
        member.rides_taken += 1
        member.save()

        circle.rides_taken += 1
        circle.save()
        return ride

class EndRideSerializer(serializers.ModelSerializer):
    current_time = serializers.DateTimeField()

    class Meta:
        """Meta class"""
        model = Ride
        fields = ("is_active", "current_time")

    def validate_current_time(self, data):
        ride = self.context['view'].get_object()
        if data <= ride.departure_date:
            raise serializers.ValidationError('Ride has not started yet')
        return data



class RideModelSerializer(serializers.ModelSerializer):

    offered_by = UserModelSerializer(read_only=True)
    offered_in = serializers.StringRelatedField(read_only=True)
    passengers = UserModelSerializer(read_only=True, many=True)

    class Meta:
        model = Ride
        fields = "__all__"
        read_only_fields = ('offered_by', 'offered_in', 'rating')

    def update(self, instance, validated_data):
        now = timezone.now()
        if instance.departure_date <= now:
            raise serializers.ValidationError('Ongoing rides can not be modified.')
        return super(RideModelSerializer, self).update(instance, validated_data)