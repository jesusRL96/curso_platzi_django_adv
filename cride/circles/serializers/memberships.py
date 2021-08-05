from django.utils import timezone

from typing import DefaultDict
from rest_framework import serializers
from cride.circles.models import Membership, Invitation

from cride.users.serializers import UserModelSerializer

class MembershipModelSerializer(serializers.ModelSerializer):
    """Membership model serializer"""
    user = UserModelSerializer(read_only=True)
    invited_by = serializers.StringRelatedField()
    joined_at=serializers.DateTimeField(source='created', read_only=True)

    class Meta:
        model = Membership
        fields = (
            'user', 'is_admin', 'is_active', 'userd_invitations', 'remaining_invitations', 'invited_by', 'rides_taken', 'rides_offered', 'joined_at',
        )
        read_only_fields = (
            'user', 'userd_invitations', 'rides_taken', 'rides_offered'
        )

class AddMemberSerializer(serializers.Serializer):
    invitation_code = serializers.CharField(min_length=8)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_user(self, data):
        circle = self.context['circle']
        user = data
        print(user)
        q = Membership.objects.filter(circle=circle, user=user)
        if q.exists():
            raise serializers.ValidationError('User is already member of this circle')
        return data

    def validate_invitation_code(self, data):
        try:
            invitation = Invitation.objects.get(code=data, circle=self.context['circle'], used=False)
        except Invitation.DoesNotExist:
            raise serializers.ValidationError('Invalid invitation code.')
        self.context['invitation'] = invitation
        return data

    def validate(self, data):
        circle = self.context['circle']
        if circle.is_limited and circle.members.count() >= circle.limit:
            raise serializers.ValidationError('Circle has reached its members limit')
        return data

    def create(self, data):
        circle = self.context['circle']
        invitation = self.context['invitation']
        user = data['user']
        print(data)
        print(user)
        now = timezone.now()
        #
        member = Membership.objects.create(user=user, profile=user.profile, circle=circle, invited_by=invitation.issued_by)
        #
        invitation.used_by = user
        invitation.used = True
        invitation.used_at = now
        invitation.save()
        #
        issuer = Membership.objects.get(user=invitation.issued_by, circle=circle)
        issuer.userd_invitations += 1
        issuer.remaining_invitations -= 1
        issuer.save()
        return member