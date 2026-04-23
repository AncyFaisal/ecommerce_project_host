import os
import shutil
import re

SOURCE_DIR = r"d:\first_project\sanjeri_perfume\sanjeri_app\forms"
TARGET_DIR = r"d:\first_project\sanjeri_perfume\sanjeri_project\-ecommerce_project\apps"

form_mapping = {
    'category.py': 'products',
    'product.py': 'products',
    'user_address_manage.py': 'accounts',
    'user_forms.py': 'accounts',
    'user_userprofile_manage.py': 'accounts',
    'wallet_forms.py': 'wallet',
    'forms.py': 'accounts'
}

for map_file, app in form_mapping.items():
    src_file = os.path.join(SOURCE_DIR, map_file)
    dst_dir = os.path.join(TARGET_DIR, app, 'forms')
    os.makedirs(dst_dir, exist_ok=True)
    dst_file = os.path.join(dst_dir, map_file)
    
    if os.path.exists(src_file):
        shutil.copy2(src_file, dst_file)
        
        # fix the __init__.py
        init_file = os.path.join(dst_dir, '__init__.py')
        module_name = map_file.replace('.py', '')
        with open(init_file, 'a', encoding='utf-8') as f:
            f.write(f"from .{module_name} import *\n")

        # patch out the "sanjeri_app" from the newly copied form files
        with open(dst_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        content = content.replace("sanjeri_app.models", f"apps.{app}.models")
        content = content.replace("from .product import", "from .product import")  # noop, just an example
        
        with open(dst_file, 'w', encoding='utf-8') as f:
            f.write(content)

print("Forms migrated successfully!")
