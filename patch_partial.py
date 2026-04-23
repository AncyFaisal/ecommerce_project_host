import os

if os.path.exists('templates/wishlist_items_partial.html'):
    with open('templates/wishlist_items_partial.html', 'r', encoding='utf-8') as f:
        html = f.read()

    if '{% with product=item.product %}' in html:
        html = html.replace('{% with product=item.product %}', '{% with product=item.variant.product %}')
    
    html = html.replace('data-variant-id="{{ product.variants.first.id }}"', 'data-variant-id="{{ item.variant.id }}"')
    html = html.replace('{% with variant=product.variants.first %}', '{% with variant=item.variant %}')

    with open('templates/wishlist_items_partial.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('Patched partial')
else:
    print('No partial file found')
