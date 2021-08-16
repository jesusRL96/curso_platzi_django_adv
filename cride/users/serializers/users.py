from cride.users.serializers.profiles import ProfileModelSerializer
from django.contrib.auth import authenticate, password_validation
from django.core.validators import RegexValidator

from django.conf import settings

import jwt
from jwt.exceptions import PyJWTError

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from cride.users.models import User, Profile
from cride.users.serializers.profiles import ProfileModelSerializer


# tasks
from cride.taskapp.tasks import send_confirmation_email



class UserModelSerializer(serializers.ModelSerializer):
    profile = ProfileModelSerializer(read_only=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'profile')

class UserSignUpSerializer(serializers.Serializer):
    """User signup serializer"""
    email = serializers.EmailField(validators=[UniqueValidator(User.objects.all())])
    username = serializers.CharField(min_length=4, max_length=20, validators=[UniqueValidator(User.objects.all())])
    # password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)
    #  phone number
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +99999999. Up to 15 digits allowed."
    )
    phone_number = serializers.CharField(max_length=17, required=False, validators=[phone_regex,])
    # Name
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    def validate(self, data):
        """Check password match"""
        password = data['password']
        password_confirm = data['password_confirmation']
        if password != password_confirm:
            raise serializers.ValidationError('Password does not match')
        password_validation.validate_password(password)
        return data

    def create(self, data):
        data.pop('password_confirmation')
        user = User.objects.create_user(**data, is_active=True, is_client=True)
        profile = Profile.objects.create(user=user)
        send_confirmation_email.delay(user_pk=user.pk )
        return user


class UserLoginSerializer(serializers.Serializer):
    """User login serializer"""
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check credentials"""
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_verified:
            raise serializers.ValidationError('Your account is not valid yet')

        self.context['user'] = user
        return data

    def create(self, data):
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key

class AccountVerificationSerializer(serializers.Serializer):
    """Account verification serializer"""
    token = serializers.CharField()

    def validate_token(self, data):
        """Verify token valid"""
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired')
        except PyJWTError:
            raise serializers.ValidationError('Invalid token')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid token')
        self.context['payload'] = payload
        return data
    def save(self):
        """Update usere's verified status."""
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified=True
        user.save()