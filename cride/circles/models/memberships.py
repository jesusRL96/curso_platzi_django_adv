from django.db import models

from cride.utils.models import CRideModel

class Membership(CRideModel):
    """Membership model
    a membership is a table that holds the relatioship
    between a circle and a user"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
    circle = models.ForeignKey('circles.Circle', on_delete=models.CASCADE)

    is_admin = models.BooleanField(
        default=False,
        help_text="Circle admins can update the circle's data and manage its members."
        )

    # Invitations
    invited_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='invited_by')
    userd_invitations = models.PositiveSmallIntegerField(default=0)
    remaining_invitations = models.PositiveSmallIntegerField(default=0)

    # stats
    rides_taken = models.PositiveIntegerField(default=0)
    rides_offered = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(
        default=True,
        help_text="Onli active users can interact in the circle."
        )
    def __str__(self):
        return f'@{self.user.username} at #{self.circle.slug_name}'

    class Meta(CRideModel.Meta):
        """Class meta"""
        ordering = ['-rides_taken', '-rides_offered']