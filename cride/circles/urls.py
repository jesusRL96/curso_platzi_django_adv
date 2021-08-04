from django.urls import path

from django.urls import path, include

from cride.circles.views import circles as circles_views
from cride.circles.views import memberships as membership_views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'circles', circles_views.CircleViewSet, basename='circle')
router.register(
    r'circles/(?P<slug_name>[-a-zA-Z0-9_]+)/members',
    membership_views.MembershipViewSet,
    basename='membership'
    )

urlpatterns = [
    path('', include(router.urls)),
]