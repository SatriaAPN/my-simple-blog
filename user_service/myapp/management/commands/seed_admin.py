from django.core.management.base import BaseCommand
from myapp.models import User
from myapp.utils import hashPassword


class Command(BaseCommand):
    help = 'Seed the database with initial admin'

    def handle(self, *args, **kwargs):
        users = [
            {'name': 'admin', 'email': 'admin@example.com', 'password': 'admin123', 'role': 'admin'},
            {'name': 'user', 'email': 'user@example.com', 'password': 'user123', 'role': 'writer'},
        ]

        for user_data in users:
            if not User.objects.filter(name=user_data['name']).exists():
                user = User.objects.create(
                    name=user_data['name'],
                    email=user_data['email'],
                    hashed_password=hashPassword(user_data['password']),
                    role=user_data['role'],
                )
                self.stdout.write(f"Created user: {user.name}")
            else:
                self.stdout.write(f"User {user_data['name']} already exists.")
