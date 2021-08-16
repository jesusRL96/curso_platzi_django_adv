from cride.circles.models.memberships import Membership
from django.test import TestCase

from cride.circles.models import Invitation, Circle
from cride.users.models import User, Profile

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken import Token

class InvitationsManagerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name="Juan",
            last_name="López",
            email="juan.lopez@gmail.com",
            username="juan1",
            password="admin1",
        )
        self.circle = Circle.objects.create(
            name="circulo 1",
            last_name="circle_1",
            about="grupo circulo 1",
            verified=True,
        )

    def test_code_generation(self):
        invitation = Invitation.objects.create(issued_by=self.user, circle=self.circle)
        # print(invitation.code)
        self.assertIsNone(invitation.code)

    def test_code_usage(self):
        code = 'holamundo'
        invitation = Invitation.objects.create(issued_by=self.user, circle=self.circle, code=code)
        self.assertEqual(code, invitation.code)

    def test_code_generation_if_duplicated(self):
        code = Invitation.objects.create(issued_by=self.user, circle=self.circle).code
        invitation = Invitation.objects.create(issued_by=self.user, circle=self.circle, code=code)
        self.assertNotEqual(code, invitation.code)
class MemberInvitationsAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name="Juan",
            last_name="López",
            email="juan.lopez@gmail.com",
            username="juan1",
            password="admin1",
        )
        self.profile = Profile.objects.create(user=self.user)
        self.circle = Circle.objects.create(
            name="circulo 1",
            last_name="circle_1",
            about="grupo circulo 1",
            verified=True,
        )
        self.membership = Membership.objects.create(user=self.user, profile=self.profile, circle=self.circle)
        self.token = Token.objects.create(user=self.user).key

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        self.url = f"/circles/{self.circle.slugname}/members/{self.user.username}/invitations/"

    def test_response_success(self):
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def self_invitation_creation(self):
        self.assertEqual(Invitation.objects.all().count(), 0)

        request = self.client.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(Invitation.objects.all().count(), 10)