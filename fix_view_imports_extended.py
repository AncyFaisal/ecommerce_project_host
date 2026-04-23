import os
import re

apps_dir = r"d:\first_project\sanjeri_perfume\sanjeri_project\-ecommerce_project\apps"
for root, _, files in os.walk(apps_dir):
    for f in files:
        if f.endswith('.py') and f != "sanjeri_models.py":
            fp = os.path.join(root, f)
            with open(fp, 'r', encoding='utf-8') as file:
                content = file.read()
            original = content
            
            # Match: from ..models.something import X, Y, Z
            content = re.sub(r"from\s+\.\.models\.[a-zA-Z0-9_]+\s+import\s+", "from apps.sanjeri_models import ", content)
            
            # Match: from sanjeri_app.models.something import X, Y, Z
            content = re.sub(r"from\s+sanjeri_app\.models\.[a-zA-Z0-9_]+\s+import\s+", "from apps.sanjeri_models import ", content)

            if original != content:
                with open(fp, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Patched extended ..models import in: {fp}")

print("Global extended view imports fixed!")
