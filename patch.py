import re

with open('templates/product_detail.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace HTML data-product-id
html = re.sub(r'data-product-id="\{\{ product\.id \}\}"', 'data-variant-id="{% if variants %}{{ variants.first.id }}{% endif %}"', html)
html = re.sub(r'data-product-id="\{\{ related\.id \}\}"', 'data-variant-id="{{ related.variants.first.id }}"', html)

# Replace Javascript logic
js_replacements = {
    'button.dataset.productId': 'button.dataset.variantId || (button.id === \'main-wishlist-btn\' ? selectedVariantId : null)',
    'dataset.productId': 'dataset.variantId',
    'addToWishlist(productId': 'addToWishlist(variantId',
    'removeFromWishlist(productId': 'removeFromWishlist(variantId',
    'const productId =': 'const variantId =',
    'wishlist_product_${productId}': 'wishlist_variant_${variantId}',
    'wishlist_product_${selectedVariantId}': 'wishlist_variant_${selectedVariantId}',
    '`/wishlist/add/${productId}/`': '`/wishlist/add/${variantId}/`',
    '`/wishlist/remove/${productId}/`': '`/wishlist/remove/${variantId}/`',
    '`/wishlist/check/${productId}/`': '`/wishlist/check/${selectedVariantId}/`',
    '[data-product-id]': '[data-variant-id]',
    'data-product-id="${productId}"': 'data-variant-id="${variantId}"',
}

for old, new_ in js_replacements.items():
    html = html.replace(old, new_)

with open('templates/product_detail.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Updated product_detail.html successfully!')
