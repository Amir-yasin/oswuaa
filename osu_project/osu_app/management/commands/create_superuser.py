# osu_app/management/commands/create_superuser.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model  # Import to get the user model

class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **kwargs):
        User = get_user_model()  # Get the custom user model
        username = "amiryasin"
        email = "amiryasin3262@gmail.com"
        password = "a1b2c3d4e5"

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS('Superuser created successfully.'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists.'))
