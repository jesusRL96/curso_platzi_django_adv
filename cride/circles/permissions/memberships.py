from rest_framework.permissions import BasePermission

from  cride.circles.models import Membership

class IsActiveCircleMember(BasePermission):
    def has_permission(self, request, view):
        circle = view.circle
        try:
            Membership.objects.get(
                user = request.user,
                circle = circle,
                is_active = True
            )
        except Membership.DoesNotExist:
            return False
        return True
