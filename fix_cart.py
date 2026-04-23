import os, re

for filename in os.listdir('templates'):
    if not filename.endswith('.html'): continue
    filepath = os.path.join('templates', filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    content = re.sub(
        r'const variantId = button\.getAttribute\(\'data-variant-id\'\);\s+const variantId = button\.getAttribute\(\'data-variant-id\'\);',
        'const variantId = button.getAttribute(\'data-variant-id\');\n            const productId = button.getAttribute(\'data-product-id\');',
        content
    )
    content = content.replace('addToCart(variantId, variantId, button)', 'addToCart(variantId, productId, button)')
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Fixed cart bugs in {filename}')
