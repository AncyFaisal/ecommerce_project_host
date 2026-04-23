import os
import re

for filename in os.listdir('templates'):
    if not filename.endswith('.html'): continue
    filepath = os.path.join('templates', filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'handleWishlistClick' in content:
        # Patch data-product-id to data-variant-id
        content = content.replace("const productId = button.getAttribute('data-product-id');", "const variantId = button.getAttribute('data-variant-id');")
        content = content.replace("if (!productId) {", "if (!variantId) {")
        content = content.replace("if (!productId) return;", "if (!variantId) return;")
        # In the URL, use variantId
        content = re.sub(r'/wishlist/add/\$\{productId\}/', '/wishlist/add/${variantId}/', content)
        content = re.sub(r'/wishlist/remove/\$\{productId\}/', '/wishlist/remove/${variantId}/', content)
        # localStorage
        content = content.replace("`wishlist_${productId}`", "`wishlist_variant_${variantId}`")
        
        # In line 577 in some files: querySelectorAll
        content = content.replace(".add-to-wishlist-btn[data-product-id=\"${productId}\"]", ".add-to-wishlist-btn[data-variant-id=\"${variantId}\"]")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Patched JS in {filename}')
