from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create a default admin user for the VAYU BRAHMAN project.'

    def handle(self, *args, **options):
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@example.com'}
        )
        user.set_password('1234')
        user.save()

        self.stdout.write(self.style.SUCCESS(
            f"Admin user ready: username={user.username}, password=1234, created={created}"
        ))
