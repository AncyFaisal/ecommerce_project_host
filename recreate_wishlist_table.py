import sqlite3
import os

def run():
    db_path = 'db.sqlite3'
    if not os.path.exists(db_path):
        print("db.sqlite3 not found!")
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    try:
        print("Dropping wishlist_wishlistitem table...")
        cur.execute('DROP TABLE IF EXISTS wishlist_wishlistitem')
        
        print("Creating wishlist_wishlistitem table...")
        cur.execute('''
        CREATE TABLE "wishlist_wishlistitem" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "added_at" datetime NOT NULL,
            "product_id" bigint NOT NULL REFERENCES "products_product" ("id") DEFERRABLE INITIALLY DEFERRED,
            "wishlist_id" bigint NOT NULL REFERENCES "wishlist_wishlist" ("id") DEFERRABLE INITIALLY DEFERRED,
            "variant_id" bigint NOT NULL REFERENCES "products_productvariant" ("id") DEFERRABLE INITIALLY DEFERRED
        )
        ''')
        
        print("Creating indexes...")
        cur.execute('CREATE INDEX "wishlist_wishlistitem_product_id_idx" ON "wishlist_wishlistitem" ("product_id")')
        cur.execute('CREATE INDEX "wishlist_wishlistitem_wishlist_id_idx" ON "wishlist_wishlistitem" ("wishlist_id")')
        cur.execute('CREATE INDEX "wishlist_wishlistitem_variant_id_idx" ON "wishlist_wishlistitem" ("variant_id")')
        cur.execute('CREATE UNIQUE INDEX "wishlist_wishlistitem_wishlist_id_variant_id_uniq" ON "wishlist_wishlistitem" ("wishlist_id", "variant_id")')
        
        conn.commit()
        print("Successfully recreated wishlist_wishlistitem table.")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    run()
