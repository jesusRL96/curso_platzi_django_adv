from django.urls import path

from django.urls import path, include

from cride.circles.views import circles as circles_views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'circles', circles_views.CircleViewSet, basename='circle')

urlpatterns = [
    path('', include(router.urls)),
]