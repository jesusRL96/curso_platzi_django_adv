# django rest framework
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404

from cride.rides.serializers import CreateRideSerializer

from cride.circles.models import Circle

from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.memberships import IsActiveCircleMember



class RideViewSet(mixins.CreateModelMixin, mixins.GenericModelMixin):
    """Ride User"""
    serializer_class = CreateRideSerializer
    permission_classes = (IsAuthenticated, IsActiveCircleMember)


    def dispatch(self, request, *args, **kwargs):
        """Verify that circle exists"""
        slug_name = kwargs['slug_name']
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super(RideViewSet, self).dispatch(request, *args, **kwargs)
