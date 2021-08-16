from django.test import TestCase

from cride.circles.models import Invitation, Circle
from cride.users.models import User

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
