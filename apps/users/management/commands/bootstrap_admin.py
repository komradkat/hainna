from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Creates a superadmin user for system bootstrapping'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Email for the superadmin', default='admin@hainna.com')
        parser.add_argument('--password', type=str, help='Password for the superadmin', default='admin123')
        parser.add_argument('--username', type=str, help='Username for the superadmin', default='admin')

    def handle(self, *args, **options):
        User = get_user_model()
        email = options['email']
        password = options['password']
        username = options['username']

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f'User with email {email} already exists.'))
            return

        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            role='Admin',
            department='Admin',
            status='Active'
        )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created superadmin "{username}" with email {email}'))
        self.stdout.write(self.style.SUCCESS(f'Password: {password}'))
        self.stdout.write(self.style.WARNING('IMPORTANT: Please change this password immediately after first login!'))
