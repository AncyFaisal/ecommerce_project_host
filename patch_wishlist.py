import os

with open('templates/wishlist.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make sure it actually has item.variant.product
if '{% with product=item.product %}' in html:
    html = html.replace('{% with product=item.product %}', '{% with product=item.variant.product %}')

html = html.replace('data-variant-id="{{ product.variants.first.id }}"', 'data-variant-id="{{ item.variant.id }}"')
html = html.replace('{% with variant=product.variants.first %}', '{% with variant=item.variant %}')

with open('templates/wishlist.html', 'w', encoding='utf-8') as f:
    f.write(html)
