from django.urls import path

from cride.users.views import UserLoginAPIView

urlpatterns = [
    path('circles/', UserLoginAPIView.as_view()),
]