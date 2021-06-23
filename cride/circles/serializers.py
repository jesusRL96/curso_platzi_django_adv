from rest_framework import serializers
from cride.circles.models import Circle
from rest_framework.validators import UniqueValidator

class CircleSerializer(serializers.Serializer):
    """Circle Serializer"""
    name = serializers.CharField()
    slug_name = serializers.SlugField()
    rides_taken = serializers.IntegerField()
    limit = serializers.IntegerField()

class CreateCircleSerializer(serializers.Serializer):
    """Create circle Serializer"""
    name = serializers.CharField(max_length=140)
    slug_name = serializers.SlugField(max_length=40,validators=[UniqueValidator(Circle.objects.all())])
    about = serializers.CharField(max_length=255, required=False)

    def create(self, data):
        """Create method for circle"""
        return Circle.objects.create(**data)