import os
import re

# 1. Create the global models registry
registry_path = r"d:\first_project\sanjeri_perfume\sanjeri_project\-ecommerce_project\apps\sanjeri_models.py"
registry_content = """
# Legacy Models Registry to bridge imports during architecture transition
from apps.accounts.models import CustomUser, Address, ReferralCoupon, UserData
from apps.products.models import Product, ProductVariant, Category, HomeBrand, HomeCategory, HomeRating, HomeProduct, CategoryOffer, ProductOffer, OfferApplication
from apps.orders.models import Order, OrderItem
from apps.cart.models import Cart, CartItem
from apps.wishlist.models import Wishlist, WishlistItem
from apps.coupons.models import Coupon
from apps.wallet.models import Wallet, WalletTransaction
from apps.payments.models import PaymentTransaction
"""
with open(registry_path, 'w', encoding='utf-8') as f:
    f.write(registry_content)

# 2. Patch all views to use the registry for `..models`
apps_dir = r"d:\first_project\sanjeri_perfume\sanjeri_project\-ecommerce_project\apps"
for root, _, files in os.walk(apps_dir):
    for f in files:
        if f.endswith('.py') and f != "sanjeri_models.py":
            fp = os.path.join(root, f)
            with open(fp, 'r', encoding='utf-8') as file:
                content = file.read()
            original = content
            
            # Match: from ..models import X, Y, Z
            content = re.sub(r"from\s+\.\.models\s+import\s+", "from apps.sanjeri_models import ", content)
            
            # Match: from sanjeri_app.models import X, Y, Z
            content = re.sub(r"from\s+sanjeri_app\.models\s+import\s+", "from apps.sanjeri_models import ", content)

            if original != content:
                with open(fp, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Patched ..models import in: {fp}")

print("Global view imports fixed!")
