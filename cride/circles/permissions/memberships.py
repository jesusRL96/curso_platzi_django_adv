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

class IsSelfMember(BasePermission):
    def has_permission(self, request, view):
        obj =view.get_object()
        return self.has_object_permission(request, view, obj)

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
