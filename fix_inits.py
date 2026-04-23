import os

TARGET_DIR = r'd:\first_project\sanjeri_perfume\sanjeri_project\-ecommerce_project\apps'

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

def rebuild_inits(component_name, mapping):
    for app, files in mapping.items():
        app_target_dir = os.path.join(TARGET_DIR, app, component_name)
        init_file = os.path.join(app_target_dir, '__init__.py')
        if os.path.exists(app_target_dir):
            imports = []
            for f in files:
                if os.path.exists(os.path.join(app_target_dir, f)):
                    module_name = f.replace('.py', '')
                    imports.append(f"from .{module_name} import *")
            
            with open(init_file, 'w') as fh:
                fh.write("\n".join(imports))

rebuild_inits('models', model_mapping)
rebuild_inits('views', view_mapping)

print("init.py files restored successfully!")
