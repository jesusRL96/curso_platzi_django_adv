from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from cride.users.models import User, Profile
from cride.rides.models import Ride

import jwt
import time
# Celery
from celery.decorators import task, periodic_task


def gen_verification_token(user):
    """Create JWT"""
    exp_date = timezone.now() + timedelta(days=3)
    payload = {
        'user': user.username,
        'exp': int(exp_date.timestamp()),
        'type': 'email_confirmation'
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token.decode()

@task(name='send_confirmation_email', max_retries=3)
def send_confirmation_email(user_pk):
    """Send account verifiacion email"""
    for i in range(7):
        time.sleep(1)
        print(f'1 second delay i:{i+1}')
    user = User.objects.get(pk=user_pk)
    verification_token = gen_verification_token(user)
    subject = f"Welcome {user.username}! Verify your account to start using the app"
    from_email = 'Comparte Ride <noreply@comparteride.com>'
    to = user.email
    content = render_to_string('email/users/account_verification.html', {'token': verification_token, 'user': user})

    msg = EmailMultiAlternatives(subject, content, from_email, [to])
    msg.attach_alternative(content, "text/html")
    msg.send()
    pass

@periodic_task(name='disable_finished_rides', run_every=timedelta(seconds=5))
def disable_finished_rides():
    now = timezone.now()
    offset = now + timedelta(seconds=5)
    rides = Ride.objects.filter(arrival_date__gte=now, arrival_date__lte=offset, is_active=True)
    rides.update(is_active=False)
