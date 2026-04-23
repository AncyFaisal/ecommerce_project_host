import os
import re

apps_dir = r"d:\first_project\sanjeri_perfume\sanjeri_project\-ecommerce_project\apps"
for root, _, files in os.walk(apps_dir):
    for f in files:
        if f.endswith('.py'):
            fp = os.path.join(root, f)
            with open(fp, 'r', encoding='utf-8') as file:
                content = file.read()
            original = content
            # Remove rogue app_labels completely to let Django resolve naturally
            content = re.sub(r"^[ \t]*app_label\s*=\s*['\"]sanjeri_app['\"]\s*\n", "", content, flags=re.MULTILINE)

            res = fp.replace("\\", "/")
            if "models/order.py" in res or "models/wallet.py" in res or "models/offer_models.py" in res or "models/cart.py" in res or "models/coupon.py" in res or "models/payment.py" in res or "models/product.py" in res or "models/user_models.py" in res:
                # Patch explicit cross-app foreign key string references
                content = content.replace("ForeignKey('Coupon', \n", "ForeignKey('coupons.Coupon', \n")
                content = content.replace("ForeignKey('Coupon',", "ForeignKey('coupons.Coupon',")
                content = content.replace('ForeignKey("Coupon",', 'ForeignKey("coupons.Coupon",')
                
                content = content.replace("ForeignKey('Order',", "ForeignKey('orders.Order',")
                content = content.replace('ForeignKey("Order",', 'ForeignKey("orders.Order",')
                
                content = content.replace("ForeignKey(\n        'Order',", "ForeignKey(\n        'orders.Order',")
                content = content.replace("ForeignKey(\n        'OrderItem',", "ForeignKey(\n        'orders.OrderItem',")

                content = content.replace("ForeignKey('OrderItem',", "ForeignKey('orders.OrderItem',")
                content = content.replace('ForeignKey("OrderItem",', 'ForeignKey("orders.OrderItem",')
                
                content = content.replace("ForeignKey('Product',", "ForeignKey('products.Product',")
                content = content.replace('ForeignKey("Product",', 'ForeignKey("products.Product",')
                
                content = content.replace("ManyToManyField('Product'", "ManyToManyField('products.Product'")

                content = content.replace("ForeignKey('Category',", "ForeignKey('products.Category',")
                
                content = content.replace("ForeignKey('CustomUser'", "ForeignKey('accounts.CustomUser'")

            if original != content:
                with open(fp, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Patched: {fp}")
