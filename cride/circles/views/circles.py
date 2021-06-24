from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from circles.serializers import CircleModelSerializer

from cride.circles.models import Circle

class CircleViewSet(viewsets.ModelViewSet):
    """Circle viewset"""
    serializer_class = CircleModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Circle.objects.all()
        if self.action == 'list':
            queryset = Circle.objects.filter(is_public=True)
        return queryset