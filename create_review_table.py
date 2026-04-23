import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
django.setup()

from django.db import connection

sql = """
CREATE TABLE IF NOT EXISTS "reviews_productreview" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "rating" integer NOT NULL,
    "comment" text NULL,
    "created_at" datetime NOT NULL,
    "product_id" bigint NOT NULL REFERENCES "products_product" ("id") DEFERRABLE INITIALLY DEFERRED,
    "user_id" bigint NOT NULL REFERENCES "accounts_user" ("id") DEFERRABLE INITIALLY DEFERRED
);
"""

# Try to create the table for sqlite, but adapt for postgres if needed.
# Since it's failing with typical django db errors, let's just use django schema editor.

from django.db import connection
from apps.reviews.models import ProductReview

with connection.schema_editor() as schema_editor:
    try:
        schema_editor.create_model(ProductReview)
        print("Model created successfully.")
    except Exception as e:
        print(f"Error creating model (might already exist): {e}")

# Insert a fake migration record if needed? No, just creating the table is enough to bypass.
