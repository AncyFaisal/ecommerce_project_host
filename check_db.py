from django.db import connection

sql = """
DROP TABLE IF EXISTS "wishlist_wishlistitem" CASCADE;
CREATE TABLE "wishlist_wishlistitem" (
    "id" serial PRIMARY KEY,
    "added_at" timestamp with time zone NOT NULL,
    "variant_id" bigint NOT NULL REFERENCES "products_productvariant" ("id") DEFERRABLE INITIALLY DEFERRED,
    "wishlist_id" bigint NOT NULL REFERENCES "wishlist_wishlist" ("id") DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT "wishlist_wishlistitem_wishlist_variant_uniq" UNIQUE ("wishlist_id", "variant_id")
);
"""

with connection.cursor() as cursor:
    cursor.execute(sql)
print("wishlist_wishlistitem table cleanly recreated.")
