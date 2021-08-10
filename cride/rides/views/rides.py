# django rest framework
from datetime import timedelta
from django.utils import timezone
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404

from cride.rides.serializers import CreateRideSerializer, RideModelSerializer

from cride.circles.models import Circle

from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.memberships import IsActiveCircleMember
from cride.rides.permissions.rides import IsRideOwner

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter


class RideViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """Ride User"""
    permission_classes = (IsAuthenticated, IsActiveCircleMember)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("departure_location", "arrival_location")
    ordering_fields = ("departure_date", "arrival_date", "available_seats",)
    ordering = ('departure_date', 'arrival_date', 'available_seats')


    def dispatch(self, request, *args, **kwargs):
        """Verify that circle exists"""
        slug_name = kwargs['slug_name']
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super(RideViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        permissions = [IsAuthenticated, IsActiveCircleMember]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsRideOwner)
        return [p() for p in permissions]


    def get_serializer_context(self):
        context = super(RideViewSet, self).get_serializer_context()
        context['circle'] = self.circle
        return context

    def get_serializer_class(self):
        if self.action=='create':
            return CreateRideSerializer
        return RideModelSerializer

    def get_queryset(self):
        offset = timezone.now() - timedelta(minutes=15)
        return self.circle.ride_set.filter(departure_date__gte=offset, is_active=True, available_seats__gte=1)