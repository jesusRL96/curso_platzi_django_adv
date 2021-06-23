from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from cride.circles.models import Circle
from cride.circles.serializers import (
    CircleSerializer,
    CreateCircleSerializer
)

@api_view(["GET"])
def list_circles(request):
    circles = Circle.objects.all()
    circles_s = CircleSerializer(circles, many=True)
    return Response(circles_s.data)

@api_view(["POST"])
def create_circle(request):
    """Create circle"""
    serializer = CreateCircleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.data
    circle = serializer.save()
    return Response(CreateCircleSerializer(circle).data)