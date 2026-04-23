import os
import shutil
import re

SOURCE_DIR = r'd:\first_project\sanjeri_perfume\sanjeri_app'
TARGET_DIR = r'd:\first_project\sanjeri_perfume\sanjeri_project\-ecommerce_project\apps'

# Models mapping
model_mapping = {
    'accounts': ['user_models.py', 'referral.py', 'models.py'],
    'products': ['product.py', 'category.py', 'offer_models.py', 'home_models.py'],
    'cart': ['cart.py'],
    'orders': ['order.py'],
    'payments': ['payment.py'],
    'coupons': ['coupon.py'],
    'wallet': ['wallet.py'],
    'wishlist': ['wishlist.py'],
}

# Views mapping
view_mapping = {
    'accounts': ['user_views.py', 'user_address_manage.py', 'user_userprofile_manage.py', 'referral_views.py', 'view_userside.py'],
    'products': ['product.py', 'category.py', 'home_views.py', 'homepage.py'],
    'cart': ['cart.py'],
    'checkout': ['checkout.py'],
    'orders': ['order_management.py', 'admin_order_management.py'],
    'payments': ['payment_views.py'],
    'coupons': ['coupon_views.py', 'admin_coupon_views.py', 'admin_offer_views.py'],
    'wallet': ['wallet_views.py', 'admin_wallet_views.py'],
    'wishlist': ['wishlist.py'],
    'analytics': ['sales_report_views.py', 'admin_views.py'],
}

def migrate_component(component_name, mapping):
    source_component_dir = os.path.join(SOURCE_DIR, component_name)
    if not os.path.exists(source_component_dir):
        return
    for app, files in mapping.items():
        app_target_dir = os.path.join(TARGET_DIR, app, component_name)
        os.makedirs(app_target_dir, exist_ok=True)
        init_file = os.path.join(app_target_dir, '__init__.py')
        
        # Remove default empty ones created by startapp
        default_file = os.path.join(TARGET_DIR, app, f'{component_name}.py')
        if os.path.exists(default_file):
            os.remove(default_file)
            
        imports = []
        for f in files:
            src = os.path.join(source_component_dir, f)
            dst = os.path.join(app_target_dir, f)
            if os.path.exists(src):
                shutil.copy2(src, dst)
                module_name = f.replace('.py', '')
                imports.append(f"from .{module_name} import *")
        
        with open(init_file, 'w') as f:
            f.write("\n".join(imports))

print("Migrating Models...")
migrate_component('models', model_mapping)
print("Migrating Views...")
migrate_component('views', view_mapping)

print("Migration completed!")
