#!/usr/bin/env python3
"""
Batch SEO E-E-A-T fix script for netsalaire.com
Applies across all HTML pages:
1. Update meta robots to include max-snippet:-1, max-image-preview:large, max-video-preview:-1
2. Update meta author to Mottalib Radif
3. Add Person schema JSON-LD for E-E-A-T
4. Add "A propos" link in footer where missing
5. Enrich Organization schema where present
"""

import os
import re
import glob

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))

# Person schema to inject (as string for insertion)
PERSON_SCHEMA = '''
    <!-- Schema.org Person (E-E-A-T) -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": "Mottalib Radif",
        "jobTitle": "Fondateur de NetSalaire",
        "description": "MBA INSEAD, passionne par la finance personnelle. Createur de NetSalaire, plateforme de simulateurs fiscaux gratuits couvrant 18+ pays.",
        "url": "https://netsalaire.com/fr/a-propos/",
        "alumniOf": {
            "@type": "EducationalOrganization",
            "name": "INSEAD",
            "url": "https://www.insead.edu"
        },
        "knowsAbout": ["finance personnelle", "fiscalite internationale", "simulation fiscale"],
        "worksFor": {
            "@type": "Organization",
            "name": "NetSalaire",
            "url": "https://netsalaire.com"
        }
    }
    </script>'''


def fix_html_file(filepath):
    """Apply all SEO fixes to a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes = []

    # Skip the a-propos page (already fully optimized)
    if '/a-propos/' in filepath:
        return changes

    # 1. Fix meta robots: add max-snippet, max-image-preview, max-video-preview
    # Match existing robots meta tag
    robots_pattern = r'<meta\s+name="robots"\s+content="([^"]*)"'
    robots_match = re.search(robots_pattern, content)
    if robots_match:
        current_content = robots_match.group(1)
        if 'max-snippet' not in current_content and 'noindex' not in current_content:
            new_content = current_content.rstrip(', ') + ', max-snippet:-1, max-image-preview:large, max-video-preview:-1'
            content = content.replace(
                robots_match.group(0),
                f'<meta name="robots" content="{new_content}"'
            )
            changes.append('robots meta enriched')

    # 2. Fix meta author: change from "NetSalaire" to "Mottalib Radif"
    author_pattern = r'<meta\s+name="author"\s+content="NetSalaire"'
    if re.search(author_pattern, content):
        content = re.sub(
            author_pattern,
            '<meta name="author" content="Mottalib Radif"',
            content
        )
        changes.append('author updated')

    # 3. Add Person schema if not already present
    if '"@type": "Person"' not in content and '"@type":"Person"' not in content:
        # Insert before </head>
        if '</head>' in content:
            content = content.replace('</head>', PERSON_SCHEMA + '\n</head>')
            changes.append('Person schema added')

    # 4. Add "A propos" link in footer if missing
    if '/fr/a-propos/' not in content:
        # Look for the Informations section in footer
        info_pattern = r'(<p class="font-semibold text-slate-900 mb-3 text-sm">Informations</p>\s*<ul[^>]*>)'
        info_match = re.search(info_pattern, content)
        if info_match:
            replacement = info_match.group(1) + '\n                        <li><a href="/fr/a-propos/" class="hover:text-slate-900 transition-colors">A propos</a></li>'
            content = content.replace(info_match.group(1), replacement)
            changes.append('A propos link added to footer')

    # 5. Update copyright line to include author
    old_copyright = '&copy; 2026 NetSalaire.com - Tous droits réservés'
    new_copyright = '&copy; 2026 NetSalaire.com &mdash; Cree par Mottalib Radif'
    if old_copyright in content:
        content = content.replace(old_copyright, new_copyright)
        changes.append('copyright updated with author')

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return changes


def main():
    # Find all HTML files under /fr/
    fr_dir = os.path.join(SITE_ROOT, 'fr')
    html_files = glob.glob(os.path.join(fr_dir, '**', '*.html'), recursive=True)

    # Also include root-level HTML files
    root_html = glob.glob(os.path.join(SITE_ROOT, '*.html'))
    all_files = html_files + root_html

    total_changes = 0
    files_modified = 0

    for filepath in sorted(all_files):
        rel_path = os.path.relpath(filepath, SITE_ROOT)
        changes = fix_html_file(filepath)
        if changes:
            files_modified += 1
            total_changes += len(changes)
            print(f"  {rel_path}: {', '.join(changes)}")

    print(f"\nDone: {files_modified} files modified, {total_changes} total changes across {len(all_files)} HTML files.")


if __name__ == '__main__':
    main()
