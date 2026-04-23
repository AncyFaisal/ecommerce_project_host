import re

files = ['templates/men.html', 'templates/women.html', 'templates/unisex.html']
for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix duplicate declaration
    bad_decl = "const variantId = button.getAttribute('data-variant-id');\n        const variantId = button.getAttribute('data-variant-id');"
    good_decl = "const variantId = button.getAttribute('data-variant-id');\n        const productId = button.getAttribute('data-product-id');"
    content = content.replace(bad_decl, good_decl)

    bad_decl_2 = "const variantId = button.getAttribute('data-variant-id');\n      const variantId = button.getAttribute('data-variant-id');"
    good_decl_2 = "const variantId = button.getAttribute('data-variant-id');\n      const productId = button.getAttribute('data-product-id');"
    content = content.replace(bad_decl_2, good_decl_2)

    # regex to fix variable length space duplicate decl
    content = re.sub(
        r"const variantId = button\.getAttribute\('data-variant-id'\);\s*const variantId = button\.getAttribute\('data-variant-id'\);",
        "const variantId = button.getAttribute('data-variant-id');\n        const productId = button.getAttribute('data-product-id');",
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print('Done fixing JS syntax errors')
