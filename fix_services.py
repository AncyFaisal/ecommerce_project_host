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
            
            # Match: from ..services.X import Y
            content = re.sub(r"from\s+\.\.services\.", "from apps.services.", content)
            
            # Match: from sanjeri_app.services.X import Y
            content = re.sub(r"from\s+sanjeri_app\.services\.", "from apps.services.", content)

            # Important: patch models imports INSIDE services too!
            if "services" in fp.replace("\\", "/"):
                content = re.sub(r"from\s+\.\.models\s+import\s+", "from apps.sanjeri_models import ", content)
                content = re.sub(r"from\s+sanjeri_app\.models\s+import\s+", "from apps.sanjeri_models import ", content)
                content = re.sub(r"from\s+sanjeri_app\.models\.[a-zA-Z0-9_]+\s+import\s+", "from apps.sanjeri_models import ", content)


            if original != content:
                with open(fp, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Patched ..services import in: {fp}")

print("Global service imports fixed!")
