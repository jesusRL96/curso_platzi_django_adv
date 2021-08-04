from rest_framework import viewsets, mixins
from rest_framework.generics import get_object_or_404

from cride.circles.models import Circle
from cride.circles.models.memberships import Membership

from cride.circles.serializers import MembershipModelSerializer

class MembershipViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Circle membership viewset"""

    serializer_class = MembershipModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """Verify that circle exists"""
        slug_name = kwargs['slug_name']
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super(MembershipViewSet, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Return circle members"""
        return Membership.objects.filter(
            circle=self.circle,
            is_active=True
        )
