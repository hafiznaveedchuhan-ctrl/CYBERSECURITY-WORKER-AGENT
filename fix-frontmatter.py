#!/usr/bin/env python3
"""Fix frontmatter IDs to match filenames in Docusaurus modules"""

import re
from pathlib import Path

# Define fixes mapping
fixes = {
    "docs/docs/module-6-advanced-implementation/02-accuracy-deep-dive.md": {
        "old_id": "id: chapter-2",
        "new_id": "id: 02-accuracy-deep-dive",
    },
    "docs/docs/module-6-advanced-implementation/03-detection-rules.md": {
        "old_id": "id: chapter-3",
        "new_id": "id: 03-detection-rules",
    },
    "docs/docs/module-6-advanced-implementation/04-compliance.md": {
        "old_id": "id: chapter-4",
        "new_id": "id: 04-compliance",
    },
    "docs/docs/module-6-advanced-implementation/05-reporting.md": {
        "old_id": "id: chapter-5",
        "new_id": "id: 05-reporting",
    },
    "docs/docs/module-7-future-proofing/01-continuous-learning.md": {
        "old_id": "id: chapter-1",
        "new_id": "id: 01-continuous-learning",
    },
    "docs/docs/module-7-future-proofing/02-zero-day-detection.md": {
        "old_id": "id: chapter-2",
        "new_id": "id: 02-zero-day-detection",
    },
    "docs/docs/module-7-future-proofing/03-threat-actor-evolution.md": {
        "old_id": "id: chapter-3",
        "new_id": "id: 03-threat-actor-evolution",
    },
    "docs/docs/module-7-future-proofing/04-global-soc.md": {
        "old_id": "id: chapter-4",
        "new_id": "id: 04-global-soc",
    },
}

for filepath, replacements in fixes.items():
    path = Path(filepath)
    if path.exists():
        content = path.read_text(encoding='utf-8')
        # Replace only the first occurrence in frontmatter (within first 10 lines)
        lines = content.split('\n')
        for i, line in enumerate(lines[:10]):
            if replacements['old_id'] in line:
                lines[i] = replacements['new_id']
                break
        path.write_text('\n'.join(lines), encoding='utf-8')
        print(f"[OK] Fixed: {path.name}")
    else:
        print(f"[ERROR] Not found: {filepath}")

print("\n[SUCCESS] All frontmatter IDs fixed!")
