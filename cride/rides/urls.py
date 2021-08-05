from django.urls import path

from django.urls import path, include

from cride.rides.views import rides as rides_views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    r'circles/(?P<slug_name>[-a-zA-Z0-9_]+)/rides',
    rides_views.RideViewSet,
    basename='ride'
    )

urlpatterns = [
    path('', include(router.urls)),
]