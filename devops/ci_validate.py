import json
import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "fabric_items"
errors = []

# 1. JSON validity: every .json file in the repo
for f in ROOT.rglob("*.json"):
    try:
        json.loads(f.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        errors.append(f"[JSON] {f.relative_to(ROOT)}: {e}")

# 2. Notebook Python syntax
# fabric-cicd stores notebooks as <name>.Notebook/notebook-content.py
for f in ROOT.rglob("notebook-content.py"):
    try:
        ast.parse(f.read_text(encoding="utf-8"))
    except SyntaxError as e:
        errors.append(f"[SYNTAX] {f.relative_to(ROOT)} line {e.lineno}: {e.msg}")

# 3. Item metadata: every .platform file must have type + displayName
for f in ROOT.rglob("*.platform"):
    try:
        meta = json.loads(f.read_text(encoding="utf-8"))
        missing = [k for k in ("type", "displayName") if k not in meta.get("metadata", {})]
        if missing:
            errors.append(f"[META] {f.relative_to(ROOT)}: missing fields {missing}")
    except json.JSONDecodeError as e:
        errors.append(f"[META] {f.relative_to(ROOT)}: invalid JSON: {e}")

# Result
if errors:
    print("CI validation FAILED:")
    for e in errors:
        print(f"  {e}")
    sys.exit(1)

json_count = len(list(ROOT.rglob("*.json")))
nb_count = len(list(ROOT.rglob("notebook-content.py")))
plat_count = len(list(ROOT.rglob("*.platform")))
print(f"CI validation passed — {json_count} JSON, {nb_count} notebooks, {plat_count} platform files")
