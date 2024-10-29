# osu_app/management/commands/create_superuser.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **kwargs):
        username = "amiryasin"  # Remove the comma
        email = "amiryasin3262@gmail.com"  # Remove the comma
        password = "a1b2c3d4e5"  # Remove the comma

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS('Superuser created successfully.'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists.'))
