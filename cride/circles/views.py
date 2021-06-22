from django.http import HttpResponse, JsonResponse
from cride.circles.models import Circle

def list_circles(request):
    circles = Circle.objects.filter(is_public=True)
    circles = [{x.name} for x in circles]
    return JsonResponse(circles,safe=False)