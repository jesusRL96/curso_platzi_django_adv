from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from cride.circles.models import Circle

@api_view(["GET"])
def list_circles(request):
    circles = Circle.objects.all()
    circles = [{'name':x.name} for x in circles]
    return Response(circles)

@api_view(["POST"])
def create_circle(request):
    """Create circle"""
    name = request.data["name"]
    about = request.data.get("about")
    slug_name = request.data["slug_name"]
    circle = Circle.objects.create(name=name, slug_name=slug_name, about=about)
    data = {'name':name,'about':about, 'slug_name':slug_name}
    return Response(data)