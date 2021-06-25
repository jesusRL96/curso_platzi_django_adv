from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from circles.serializers import CircleModelSerializer

from cride.circles.models import Circle, Membership, circles

class CircleViewSet(viewsets.ModelViewSet):
    """Circle viewset"""
    serializer_class = CircleModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Circle.objects.all()
        if self.action == 'list':
            queryset = Circle.objects.filter(is_public=True)
        return queryset

    def perform_create(self, serializer):
        """Assign circle admin"""
        circle = serializer.save()
        user = self.request.user
        profile = user.profile
        Membership.objects.create(
            user = user,
            profile = profile,
            circle = circle,
            is_admin = True,
            remaining_invitations = 10
        )