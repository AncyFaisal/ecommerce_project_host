import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
django.setup()

from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
tables = [r[0] for r in cursor.fetchall()]

# check if we have any data in the core ones
if 'sanjeri_app_product' in tables:
    cursor.execute("SELECT COUNT(*) FROM sanjeri_app_product")
    print("Old Product count:", cursor.fetchone()[0])
else:
    print("Old Product count: No Table")

if 'products_product' in tables:
    cursor.execute("SELECT COUNT(*) FROM products_product")
    print("New Product count:", cursor.fetchone()[0])
else:
    print("New Product count: No Table")
