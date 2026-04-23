import os
import re

apps_dir = r"d:\first_project\sanjeri_perfume\sanjeri_project\-ecommerce_project\apps"

folders_to_patch = ["utils", "templatetags", "management", "signals"]

for root, _, files in os.walk(apps_dir):
    for f in files:
        if f.endswith('.py'):
            fp = os.path.join(root, f)
            with open(fp, 'r', encoding='utf-8') as file:
                content = file.read()
            original = content
            
            for folder in folders_to_patch:
                # Match: from ..folder.X import Y
                content = re.sub(r"from\s+\.\." + folder + r"\.", f"from apps.{folder}.", content)
                
                # Match: from sanjeri_app.folder.X import Y
                content = re.sub(r"from\s+sanjeri_app\." + folder + r"\.", f"from apps.{folder}.", content)

                # Fix models imports inside the folder
                if folder in fp.replace("\\", "/"):
                    content = re.sub(r"from\s+\.\.models\s+import\s+", "from apps.sanjeri_models import ", content)
                    content = re.sub(r"from\s+sanjeri_app\.models\s+import\s+", "from apps.sanjeri_models import ", content)
                    content = re.sub(r"from\s+sanjeri_app\.models\.[a-zA-Z0-9_]+\s+import\s+", "from apps.sanjeri_models import ", content)

            if original != content:
                with open(fp, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Patched auxiliary folder imports in: {fp}")

print("Global auxiliary imports fixed!")
