import os

filepath = r"d:\New folder (9)\-ecommerce_project\apps\accounts\views\view_userside.py"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update ProductVariant.objects.filter in home, men, women, unisex
# They usually look like:
"""
        is_active=True,
        product__is_active=True,
        product__is_deleted=False,
"""
# We'll replace it with our extensive one.
# Wait, some have gender='Male', gender='Female', gender=gender_filter in the same block. Let's just find and replace the common prefix.
old_variant_base = "is_active=True,\n        product__is_active=True,\n        product__is_deleted=False"
new_variant_base = "is_active=True,\n        stock__gt=0,\n        product__is_active=True,\n        product__is_deleted=False,\n        product__category__is_active=True,\n        product__category__is_deleted=False"

content = content.replace("is_active=True,\n        product__is_active=True,\n        product__is_deleted=False", new_variant_base)

# 2. Update Product.objects.filter across the file
# Usually occurs as:
"""
        is_active=True,
        is_deleted=False,
        variants__is_active=True
"""
old_product_base = "is_active=True,\n        is_deleted=False,\n        variants__is_active=True"
new_product_base = "is_active=True,\n        is_deleted=False,\n        category__is_active=True,\n        category__is_deleted=False,\n        variants__is_active=True,\n        variants__stock__gt=0,\n        variants__is_deleted=False"

content = content.replace(old_product_base, new_product_base)

# Wait, search uses a list inside Q() and then filter():
"""
            is_active=True,
            is_deleted=False,
            variants__is_active=True
"""
old_product_base_2 = "is_active=True,\n            is_deleted=False,\n            variants__is_active=True"
new_product_base_2 = "is_active=True,\n            is_deleted=False,\n            category__is_active=True,\n            category__is_deleted=False,\n            variants__is_active=True,\n            variants__stock__gt=0,\n            variants__is_deleted=False"

content = content.replace(old_product_base_2, new_product_base_2)

# Also check available_volumes / available_fragrance filters.
# These use Product.objects.filter or ProductVariant.objects.filter and we don't want to show variants that are out of stock in the filter sidebar!
# Fortunately, our new_variant_base replaces product__is_deleted=False with the extensive check.
# Let's save and test
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated view_userside.py')
