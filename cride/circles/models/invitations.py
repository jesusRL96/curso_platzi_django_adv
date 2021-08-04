from cride.circles.models.circles import Circle
from django.db import models

from cride.utils.models import CRideModel
# Managers
from cride.circles.managers.invitations import InvitationManager


class Invitation(CRideModel):
    """Circle invitation model"""
    code = models.CharField(max_length=50, unique=True)
    issued_by = models.ForeignKey('users.User', on_delete=models.CASCADE, help_text="Circle member that is providing the invitation", related_name="issued_by")
    used_by = models.ForeignKey('users.User', on_delete=models.CASCADE, help_text="User that uses the code to enter the circle", blank=True, null=True)
    circle = models.ForeignKey('circles.Circle', on_delete=models.CASCADE)
    used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)

    objects = InvitationManager()

    def __str__(self):
        return f'#{self.circle.slug_name}:{self.code}'

    class Meta(CRideModel.Meta):
        ordering = ['used_at']