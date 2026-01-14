#!/usr/bin/env python3
"""
Verify backend-services-architect skill structure and content
"""

import sys
from pathlib import Path
import yaml

def verify_skill(skill_path: str = '.') -> bool:
    """Verify skill structure and content"""
    base_dir = Path(skill_path)
    errors = []
    warnings = []

    # Check SKILL.md exists
    skill_md = base_dir / 'SKILL.md'
    if not skill_md.exists():
        errors.append('SKILL.md not found')
        return False

    # Verify SKILL.md structure
    content = skill_md.read_text()
    lines = content.split('\n')

    # Check frontmatter
    if not content.startswith('---'):
        errors.append('SKILL.md must start with YAML frontmatter (---)')

    # Extract and validate frontmatter
    try:
        end_idx = lines[1:].index('---') + 1
        frontmatter_text = '\n'.join(lines[1:end_idx])
        frontmatter = yaml.safe_load(frontmatter_text)

        # Check required fields
        if not frontmatter.get('name'):
            errors.append('YAML frontmatter missing required field: name')
        if not frontmatter.get('description'):
            errors.append('YAML frontmatter missing required field: description')

        # Check description mentions "Use when"
        desc = frontmatter.get('description', '')
        if not desc.startswith('Use when'):
            warnings.append('Description should start with "Use when..."')

        # Check for exclusions
        if ' NOT when ' not in desc:
            warnings.append('Consider adding "NOT when..." to clarify when NOT to use the skill')

    except Exception as e:
        errors.append(f'Failed to parse SKILL.md frontmatter: {str(e)}')

    # Check for references
    refs_dir = base_dir / 'references'
    if refs_dir.exists():
        ref_files = list(refs_dir.glob('*.md'))
        print(f'[OK] Found {len(ref_files)} reference files')
        for ref in ref_files:
            print(f'  - {ref.name}')
    else:
        warnings.append('No references/ directory found')

    # Check for scripts
    scripts_dir = base_dir / 'scripts'
    if scripts_dir.exists():
        script_files = list(scripts_dir.glob('*'))
        script_files = [f for f in script_files if f.is_file() and f.name != '__init__.py']
        print(f'[OK] Found {len(script_files)} script files')
        for script in script_files:
            print(f'  - {script.name}')
    else:
        warnings.append('No scripts/ directory found')

    # Report results
    if errors:
        print('\n[ERROR] ERRORS:')
        for error in errors:
            print(f'  - {error}')
        return False

    if warnings:
        print('\n[WARN] WARNINGS:')
        for warning in warnings:
            print(f'  - {warning}')

    print('\n[OK] Skill structure verified successfully')
    return True

if __name__ == '__main__':
    skill_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    success = verify_skill(skill_path)
    sys.exit(0 if success else 1)
