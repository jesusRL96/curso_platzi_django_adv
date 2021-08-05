from rest_framework import viewsets, mixins

# Permissions
from cride.circles.permissions.circles import IsCircleAdmin
from rest_framework.permissions import IsAuthenticated

from cride.circles.serializers import CircleModelSerializer

from cride.circles.models import Circle, Membership, circles

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class CircleViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """Circle viewset"""
    serializer_class = CircleModelSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'slug_name'

    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ("slug_name", "name")
    ordering_fields = ("rides_taken", "rides_offered", "name", "created")
    ordering = ('-members', 'rides_offered', 'rides_taken')
    filter_fields = ('verified', 'is_limited')

    def get_queryset(self):
        queryset = Circle.objects.all()
        if self.action == 'list':
            queryset = Circle.objects.filter(is_public=True)
        return queryset

    def get_permissions(self):
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsCircleAdmin)
        return [p() for p in permissions]

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