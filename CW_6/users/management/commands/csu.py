import os

from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """
    Команда создаёт суперпользователя
    """
    def handle(self, *args, **options):
        user = User.objects.create(
            email=os.getenv('CSU_EMAIL'),
            first_name=os.getenv('CSU_FIRST_NAME'),
            last_name=os.getenv('CSU_LAST_NAME'),
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

        user.set_password(os.getenv('CSU_PASS'))
        user.save()
