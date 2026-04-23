import os
import re

# 1. Create the global forms registry
registry_path = r"d:\first_project\sanjeri_perfume\sanjeri_project\-ecommerce_project\apps\sanjeri_forms.py"
registry_content = """
# Legacy Forms Registry
from apps.accounts.forms.user_address_manage import *
from apps.accounts.forms.user_forms import *
from apps.accounts.forms.user_userprofile_manage import *
from apps.accounts.forms.forms import *
from apps.products.forms.category import *
from apps.products.forms.product import *
from apps.wallet.forms.wallet_forms import *
"""
with open(registry_path, 'w', encoding='utf-8') as f:
    f.write(registry_content)

# 2. Patch all views to use the registry for `..forms`
apps_dir = r"d:\first_project\sanjeri_perfume\sanjeri_project\-ecommerce_project\apps"
for root, _, files in os.walk(apps_dir):
    for f in files:
        if f.endswith('.py') and f != "sanjeri_forms.py":
            fp = os.path.join(root, f)
            with open(fp, 'r', encoding='utf-8') as file:
                content = file.read()
            original = content
            
            # Match: from ..forms import X
            content = re.sub(r"from\s+\.\.forms\s+import\s+", "from apps.sanjeri_forms import ", content)
            
            # Match: from ..forms.something import X
            content = re.sub(r"from\s+\.\.forms\.[a-zA-Z0-9_]+\s+import\s+", "from apps.sanjeri_forms import ", content)
            
            # Match: from sanjeri_app.forms import X
            content = re.sub(r"from\s+sanjeri_app\.forms\s+import\s+", "from apps.sanjeri_forms import ", content)
            
            # Match: from sanjeri_app.forms.something import X
            content = re.sub(r"from\s+sanjeri_app\.forms\.[a-zA-Z0-9_]+\s+import\s+", "from apps.sanjeri_forms import ", content)

            if original != content:
                with open(fp, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Patched ..forms import in: {fp}")

print("Global form imports fixed!")
