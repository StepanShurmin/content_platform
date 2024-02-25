from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Cозданиe суперпользователя
    """

    def handle(self, *args, **options):
        user = User.objects.create(
            phone="89221234567", first_name="Admin", last_name="SkyPro", is_staff=True, is_superuser=True
        )

        user.set_password("123")
        user.save()
