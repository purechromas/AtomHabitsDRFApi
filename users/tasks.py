import random

from celery import shared_task
from django.core.mail import send_mail

from config import settings


@shared_task
def email_user_verify(email, verification_number):
    """
    Sends a verification email to the user.
    """
    verification_url = f'http://localhost:8000/api/verification/?verification_number={verification_number}'
    send_mail(
        subject='You were successfully registered.',
        message=f"""
        If you did the registration in our site click here
        {verification_url} to activate your profile!
        """,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email]
    )


def generate_verification_number() -> str:
    """
    Generate a specific number, witch we use to verified specific user.
    """
    return ''.join(str(random.randint(1, 9)) for _ in range(8))
