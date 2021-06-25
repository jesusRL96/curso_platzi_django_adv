from rest_framework import serializers
from cride.circles.models import Circle

class CircleModelSerializer(serializers.ModelSerializer):
    """Circle Serializer"""

    is_limited = serializers.BooleanField(default=False)
    limit = serializers.IntegerField(
        required=False,
        min_value=10,
        max_value=32000,
    )
    class Meta:
        model = Circle
        fields = (
            'id', 'name', 'slug_name', 'about', 'picture',
            'rides_taken', 'rides_offered', 'verified', 'is_public',
            'is_limited', 'members', 'limit',
        )
        read_only_fields = (
            'is_public',
            'verified',
            'rides_taken',
            'rides_offered',
        )

    def validate(self, data):
        is_limited = data.get('is_limited', False)
        limit = data.get('limit', None)
        if is_limited ^ bool(limit):
            raise serializers.ValidationError('If members is limited, members limit must be provided')
        return data