import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("DELETE FROM django_migrations WHERE app='account' AND name='0001_initial'")
    print("Deleted account.0001_initial!")
    
    # Just in case there are others that are out of order, delete all of 'account' migrations
    cursor.execute("DELETE FROM django_migrations WHERE app='account'")
    print("Deleted all 'account' records from django_migrations, they will be reapplied without issues.")
