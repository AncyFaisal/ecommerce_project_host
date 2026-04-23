import os, re

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html

    # Replace item.product with item.variant.product in wishlist loops
    if "wishlist" in filepath.lower() or "partial" in filepath.lower():
        html = html.replace('item.product.', 'item.variant.product.')
        # but wait, product card may expect product=p. We pass variant=v already earlier!
        # fix variant references from the product loop
        html = html.replace('data-product-id="{{ item.product.id }}"', 'data-variant-id="{{ item.variant.id }}"')
        html = html.replace('data-product-id="{{ product.id }}"', 'data-variant-id="{{ product.variants.first.id }}"')

    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Patched {filepath}")

for root, _, files in os.walk('templates'):
    for file in files:
        if file.endswith('.html'):
            try:
                patch_file(os.path.join(root, file))
            except Exception as e:
                print(e)
