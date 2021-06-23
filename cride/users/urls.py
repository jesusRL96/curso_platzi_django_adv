from django.urls import path

from cride.users.views import UserLoginAPIView, UserSignUpAPIView

urlpatterns = [
    path('users/login/', UserLoginAPIView.as_view()),
    path('users/signup/', UserSignUpAPIView.as_view()),
]