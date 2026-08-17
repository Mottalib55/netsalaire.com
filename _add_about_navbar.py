#!/usr/bin/env python3
"""
Add "A propos" link to the main desktop navbar on all pages,
next to the FAQ link, for YMYL E-E-A-T compliance.
"""

import os
import re
import glob

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))


def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip a-propos page itself (already has it highlighted)
    if '/a-propos/' in filepath:
        return False

    # Pattern: FAQ link in desktop navbar (not mobile)
    # Look for: <a href="/fr/faq/" ...>FAQ</a> in the desktop nav section
    old = '<a href="/fr/faq/" class="hover:text-slate-900 transition-colors">FAQ</a>'
    new = '<a href="/fr/faq/" class="hover:text-slate-900 transition-colors">FAQ</a>\n                <a href="/fr/a-propos/" class="hover:text-slate-900 transition-colors">A propos</a>'

    if old in content and 'A propos</a>\n' not in content.split('</nav>')[0]:
        content = content.replace(old, new, 1)  # Only first occurrence (desktop nav)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    return False


def main():
    fr_dir = os.path.join(SITE_ROOT, 'fr')
    html_files = glob.glob(os.path.join(fr_dir, '**', '*.html'), recursive=True)
    modified = 0
    for filepath in sorted(html_files):
        if fix_file(filepath):
            modified += 1
            print(f"  OK {os.path.relpath(filepath, SITE_ROOT)}")
    print(f"\nDone: {modified} files modified.")


if __name__ == '__main__':
    main()
