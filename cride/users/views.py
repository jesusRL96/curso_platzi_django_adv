
from django.db import reset_queries
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework.permissions import AllowAny, IsAuthenticated
from cride.users.permissions import IsAccountOwner


from cride.users.serializers import UserLoginSerializer, UserModelSerializer, UserSignUpSerializer,AccountVerificationSerializer
from cride.circles.serializers import CircleModelSerializer

from cride.users.models.users import User
from cride.circles.models.circles import Circle


class UserViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """User Viewset"""
    queryset = User.objects.filter(is_active=True, is_client=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    def get_permissions(self):
        if self.action in ['login', 'signup', 'verify']:
            permissions = [AllowAny,]
        elif self.action == 'retrieve':
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permission = [IsAuthenticated]
        return [p() for p in permissions]

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User's signup"""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User's login"""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """Account verification"""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = {'message': 'Congratulations your account has been verified'}
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """Add extra data to response"""
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        circles =  Circle.objects.filter(members=request.user, membership__is_active=True)
        data = {
            'user': response.data,
            'circles': CircleModelSerializer(circles, many=True).data
        }
        response.data = data
        return response