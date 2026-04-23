import os, re

for filename in os.listdir('templates'):
    if not filename.endswith('.html'): continue
    filepath = os.path.join('templates', filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    # cart stuff that got swapped by replacing `variant` with `product` globally:
    content = content.replace('async function addToCart(productId, productId, button)', 'async function addToCart(variantId, productId, button)')
    content = content.replace('addToCart(productId, productId, button);', 'addToCart(variantId, productId, button);')
    content = content.replace('/cart/add/${productId}/', '/cart/add/${variantId}/')
    content = content.replace('added_${productId}', 'added_${variantId}')
    content = content.replace('/cart/check-product/${productId}/', '/cart/check-variant/${variantId}/')
    content = content.replace('checkCartForProduct(productId, button)', 'checkCartForVariant(variantId, button)')
    content = content.replace('async function checkCartForProduct(productId, button)', 'async function checkCartForVariant(variantId, button)')
    content = content.replace('const productId = button.getAttribute(\'data-product-id\');\n            const productId = button.getAttribute(\'data-product-id\');', 'const variantId = button.getAttribute(\'data-variant-id\');\n            const productId = button.getAttribute(\'data-product-id\');')
    content = content.replace('if (productId) {\n                addToCart(variantId, productId, button);', 'if (variantId) {\n                addToCart(variantId, productId, button);')
    content = content.replace('if (productId) {\n                // First check localStorage for immediate feedback', 'if (variantId) {\n                // First check localStorage for immediate feedback')
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Fixed cart in {filename}')
