import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Resets the database by deleting the database file and running migrations.'

    def handle(self, *args, **options):
        db_path = settings.DATABASES['default']['NAME']
        migrations_paths = []
        for app in settings.INSTALLED_APPS:
            app_path = __import__(app).__path__[0]
            migrations_path = os.path.join(app_path, 'migrations')
            if os.path.exists(migrations_path):
                migrations_paths.append(migrations_path)

        if os.path.exists(db_path):
            os.remove(db_path)
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted database file: {db_path}'))
        else:
            self.stdout.write(self.style.WARNING(f'Database file not found: {db_path}'))

        for path in migrations_paths:
            for filename in os.listdir(path):
                if filename != '__init__.py' and filename.endswith('.py'):
                    file_path = os.path.join(path, filename)
                    os.remove(file_path)
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted migrations in: {path}'))

        self.stdout.write(self.style.WARNING('Running makemigrations...'))
        os.system('python manage.py makemigrations')

        self.stdout.write(self.style.WARNING('Running migrate...'))
        os.system('python manage.py migrate')

        self.stdout.write(self.style.SUCCESS('Database has been successfully reset.'))