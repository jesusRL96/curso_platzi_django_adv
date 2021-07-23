from django.contrib.auth import authenticate, password_validation
from django.core.validators import RegexValidator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings

from datetime import timedelta
import jwt
from jwt.exceptions import PyJWTError

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from cride.users.models import Profile

class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile model serializer"""
    class Meta:
        model = Profile
        fields = ('picture', 'biography', 'rides_taken', 'rides_offered', 'reputation')
        read_only_fields = ('rides_taken', 'rides_offered', 'reputation')