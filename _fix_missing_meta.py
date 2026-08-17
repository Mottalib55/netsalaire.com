#!/usr/bin/env python3
"""
Add missing meta robots and meta author tags to pages that don't have them.
Also adds A propos link to footer where missing.
"""

import os
import re
import glob

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))

ROBOTS_META = '    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">'
AUTHOR_META = '    <meta name="author" content="Mottalib Radif">'


def fix_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes = []

    # Skip non-indexable pages and a-propos
    if '/a-propos/' in filepath:
        return changes

    # Add meta robots if missing entirely (but not on noindex pages)
    if 'name="robots"' not in content and '</head>' in content:
        # Insert before </head>
        insert_point = '    <!-- Favicon -->' if '<!-- Favicon -->' in content else '</head>'
        if insert_point in content:
            content = content.replace(
                insert_point,
                ROBOTS_META + '\n' + AUTHOR_META + '\n' + insert_point,
                1
            )
            changes.append('meta robots + author added')
    elif 'name="author"' not in content and '</head>' in content:
        # Has robots but no author
        robots_match = re.search(r'(<meta\s+name="robots"[^>]*>)', content)
        if robots_match:
            content = content.replace(
                robots_match.group(0),
                robots_match.group(0) + '\n' + AUTHOR_META
            )
            changes.append('meta author added')

    # Add A propos link to footer Informations section if missing
    if '/fr/a-propos/' not in content and 'Informations' in content:
        # Try different footer patterns
        patterns = [
            r'(Informations</p>\s*<ul[^>]*>\s*\n)',
            r'(Informations</p>\s*<ul class="space-y-2 text-sm text-slate-500">\s*\n)',
        ]
        for pat in patterns:
            match = re.search(pat, content)
            if match:
                content = content.replace(
                    match.group(0),
                    match.group(0) + '                        <li><a href="/fr/a-propos/" class="hover:text-slate-900 transition-colors">A propos</a></li>\n'
                )
                changes.append('A propos footer link added')
                break

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return changes


def main():
    fr_dir = os.path.join(SITE_ROOT, 'fr')
    html_files = glob.glob(os.path.join(fr_dir, '**', '*.html'), recursive=True)

    total = 0
    modified = 0
    for filepath in sorted(html_files):
        rel = os.path.relpath(filepath, SITE_ROOT)
        changes = fix_html_file(filepath)
        if changes:
            modified += 1
            total += len(changes)
            print(f"  {rel}: {', '.join(changes)}")

    print(f"\nDone: {modified} files modified, {total} changes.")


if __name__ == '__main__':
    main()
