from rest_framework import viewsets

from circles.serializers import CircleModelSerializer

from cride.circles.models import Circle

class CircleViewSet(viewsets.ModelViewSet):
    """Circle viewset"""
    serializer_class = CircleModelSerializer
    queryset = Circle.objects.all()