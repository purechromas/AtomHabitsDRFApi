from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='superuser@gmail.com',
            is_verified=True,
            is_staff=True,
            is_superuser=True
        )
        user.set_password('superuser')
        user.save()