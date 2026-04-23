import os

files = ['templates/men.html', 'templates/women.html', 'templates/unisex.html']
for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # In handleWishlistClick
    content = content.replace("const productId = button.getAttribute('data-product-id');", "const variantId = button.getAttribute('data-variant-id');")
    content = content.replace("if (!productId)", "if (!variantId)")
    content = content.replace("/wishlist/remove/${productId}/", "/wishlist/remove/${variantId}/")
    content = content.replace("/wishlist/add/${productId}/", "/wishlist/add/${variantId}/")
    content = content.replace("wishlist_product_${productId}", "wishlist_variant_${variantId}")
    
    # In refreshWishlistStatus (women.html, unisex.html)
    content = content.replace("const productIds =", "const variantIds =")
    content = content.replace("getAttribute('data-product-id')", "getAttribute('data-variant-id')")
    content = content.replace("product_ids: productIds", "variant_ids: variantIds")
    content = content.replace("const isInWishlist = data[productId]", "const isInWishlist = data[variantId]")
    
    # In checkWishlistStatusIndividually
    content = content.replace("if (productId)", "if (variantId)")
    content = content.replace("/wishlist/check/${productId}/", "/wishlist/check/${variantId}/")
    content = content.replace("error checking variant ${productId}", "error checking variant ${variantId}")
    content = content.replace('data-product-id="${productId}"', 'data-variant-id="${variantId}"')
    
    # Duplicate variantId definition fix
    content = content.replace("const variantId = button.getAttribute('data-variant-id');\n            const variantId = button.getAttribute('data-variant-id');", "const variantId = button.getAttribute('data-variant-id');\n            const productId = button.getAttribute('data-product-id');")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updated multiple JS variable problems.")
