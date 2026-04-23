import os
import re

SOURCE_URLS = r"d:\first_project\sanjeri_perfume\sanjeri_app\urls.py"
TARGET_URLS = r"d:\first_project\sanjeri_perfume\sanjeri_project\-ecommerce_project\core\urls.py"

view_mapping = {
    'user_views': 'apps.accounts.views',
    'user_address_manage': 'apps.accounts.views',
    'user_userprofile_manage': 'apps.accounts.views',
    'referral_views': 'apps.accounts.views',
    'view_userside': 'apps.accounts.views',
    'product': 'apps.products.views',
    'category': 'apps.products.views',
    'home_views': 'apps.products.views',
    'homepage': 'apps.products.views',
    'cart': 'apps.cart.views',
    'checkout': 'apps.checkout.views',
    'order_management': 'apps.orders.views',
    'admin_order_management': 'apps.orders.views',
    'payment_views': 'apps.payments.views',
    'coupon_views': 'apps.coupons.views',
    'admin_coupon_views': 'apps.coupons.views',
    'admin_offer_views': 'apps.coupons.views',
    'wallet_views': 'apps.wallet.views',
    'admin_wallet_views': 'apps.wallet.views',
    'wishlist': 'apps.wishlist.views',
    'sales_report_views': 'apps.analytics.views',
    'admin_views': 'apps.analytics.views',
}

with open(SOURCE_URLS, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace imports
for old_mod, new_mod in view_mapping.items():
    content = re.sub(rf'from\s+\.views\.{old_mod}\b', f'from {new_mod}', content)
    content = re.sub(rf'from\s+sanjeri_app\.views\.{old_mod}\b', f'from {new_mod}', content)

# Inject standard Django admin and error handlers
header = """from django.conf import settings
from django.conf.urls.static import static

# Custom error handlers
handler404 = 'core.views.error_404'
handler500 = 'core.views.error_500'
handler403 = 'core.views.error_403'
handler400 = 'core.views.error_400'
"""

# Try to find the start of urlpatterns to inject admin
if 'urlpatterns = [' in content:
    content = content.replace('urlpatterns = [', 'urlpatterns = [\n    path("admin/", admin.site.urls),')

content = header + "\n" + content

# Add static/media routes at the end
footer = """
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
"""
content += footer

with open(TARGET_URLS, 'w', encoding='utf-8') as f:
    f.write(content)

print("URLs migrated successfully!")
