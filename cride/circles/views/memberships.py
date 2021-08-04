from cride.circles.models import invitations
from rest_framework import viewsets, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.memberships import IsActiveCircleMember

from cride.circles.models import Circle
from cride.circles.models.memberships import Membership
from cride.circles.models.invitations import Invitation

from cride.circles.serializers import MembershipModelSerializer
from rest_framework.decorators import action

class MembershipViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin ,viewsets.GenericViewSet):
    """Circle membership viewset"""

    serializer_class = MembershipModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """Verify that circle exists"""
        slug_name = kwargs['slug_name']
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super(MembershipViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        permissions = [IsAuthenticated, IsActiveCircleMember]
        return [p() for p in permissions]

    def get_queryset(self):
        """Return circle members"""
        return Membership.objects.filter(
            circle=self.circle,
            is_active=True
        )

    def get_object(self):
        return get_object_or_404(Membership, user__username=self.kwargs['pk'], circle=self.circle, is_active=True)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    @action(detail=True, methods=['get'])
    def invitations(self, request, *args, **kwargs):
        member = self.get_object()
        invited_members = Membership.objects.filter(circle=self.circle, invited_by=request.user, is_active=True)

        unused_invitations = Invitation.objects.filter(circle=self.circle, issued_by=request.user, used=False). values_list('code')
        diff = member.remaining_invitations - len(unused_invitations)
        invitations = [x[0] for x in unused_invitations]
        for i in range(0,diff):
            invitations.append(
                Invitation.objects.create(issued_by=request.user, circle=self.circle).code
            )

        data = {
            'used_invitations': MembershipModelSerializer(invited_members, many=True).data,
            'invitations': invitations

        }
        return Response(data)
