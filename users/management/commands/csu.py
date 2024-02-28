from django.core.management import BaseCommand
from django.db import IntegrityError

from users.models import User


class Command(BaseCommand):
    """
    Cозданиe суперпользователя
    """

    def handle(self, *args, **options):
        try:
            user = User.objects.create(
                phone="89221234567",
                first_name="Admin",
                last_name="SkyPro",
                username="admin",
                is_staff=True,
                is_superuser=True,
            )

            user.set_password("123")
            user.save()
        except IntegrityError:
            pass
