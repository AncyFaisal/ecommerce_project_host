import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
django.setup()

from django.apps import apps
from django.db import connection

with connection.cursor() as cursor:
    # Get all tables in public schema
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    existing_tables = set(r[0] for r in cursor.fetchall())
    
    # Track actions
    renames = []
    
    for model in apps.get_models():
        target_table = model._meta.db_table
        
        # Determine the old table name
        model_name = model.__name__.lower()
        old_table_candidates = [
            f"sanjeri_app_{model_name}",
            f"{model._meta.app_label}_{model_name}" # In case it's another format
        ]
        
        for old_table in old_table_candidates:
            if old_table != target_table and old_table in existing_tables and target_table not in existing_tables:
                renames.append((old_table, target_table))
                existing_tables.remove(old_table) # Process once
                existing_tables.add(target_table)
                break

    for old, new in renames:
        print(f"ALTER TABLE {old} RENAME TO {new};")
        cursor.execute(f"ALTER TABLE {old} RENAME TO {new};")
        # Also rename sequence if it exists
        seq_old = f"{old}_id_seq"
        seq_new = f"{new}_id_seq"
        if seq_old in [t for t in existing_tables if t.endswith('_seq')]:
             print(f"ALTER SEQUENCE {seq_old} RENAME TO {seq_new};")

print("Done. Renamed", len(renames), "tables.")
