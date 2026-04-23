import os
import re

app_model_mapping = {
    'user_models': 'apps.accounts.models',
    'referral': 'apps.accounts.models',
    'category': 'apps.products.models',
    'product': 'apps.products.models',
    'home_models': 'apps.products.models',
    'offer_models': 'apps.products.models',
    'cart': 'apps.cart.models',
    'order': 'apps.orders.models',
    'payment': 'apps.payments.models',
    'coupon': 'apps.coupons.models',
    'wallet': 'apps.wallet.models',
    'wishlist': 'apps.wishlist.models',
    'models': 'apps.accounts.models',
}

view_mapping = {
    'user_views': 'apps.accounts.views',
    'user_address_manage': 'apps.accounts.views',
    'user_userprofile_manage': 'apps.accounts.views',
    'referral_views': 'apps.accounts.views',
    'view_userside': 'apps.accounts.views',
    'home_views': 'apps.products.views',
    'homepage': 'apps.products.views',
    'checkout': 'apps.checkout.views',
    'order_management': 'apps.orders.views',
    'admin_order_management': 'apps.orders.views',
    'payment_views': 'apps.payments.views',
    'coupon_views': 'apps.coupons.views',
    'admin_coupon_views': 'apps.coupons.views',
    'admin_offer_views': 'apps.coupons.views',
    'wallet_views': 'apps.wallet.views',
    'admin_wallet_views': 'apps.wallet.views',
    'sales_report_views': 'apps.analytics.views',
    'admin_views': 'apps.analytics.views',
}

apps_dir = r"d:\first_project\sanjeri_perfume\sanjeri_project\-ecommerce_project\apps"

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    original_content = content

    # Patch relative model imports
    for old_mod, new_mod in app_model_mapping.items():
        content = re.sub(rf'from\s+\.{old_mod}\b', f'from {new_mod}', content)
        content = re.sub(rf'from\s+sanjeri_app\.models\.{old_mod}\b', f'from {new_mod}', content)

    # Patch relative view imports
    for old_mod, new_mod in view_mapping.items():
        content = re.sub(rf'from\s+\.{old_mod}\b', f'from {new_mod}', content)
        content = re.sub(rf'from\s+sanjeri_app\.views\.{old_mod}\b', f'from {new_mod}', content)

    # Patch base sanjeri_app imports that just grab models directly
    # 'from sanjeri_app.models import CustomUser' -> we can't easily know where CustomUser is without a map,
    # but we can try to guess or use a class dictionary later if it fails.
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Patched: {filepath}")

for root, _, files in os.walk(apps_dir):
    for f in files:
        if f.endswith('.py'):
            patch_file(os.path.join(root, f))
