#!/usr/bin/env python3
"""Fix the 12 pages with non-standard footer patterns."""

import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Import translations from the main script
from fix_footer_redirect import build_countries_dark, get_translations, get_footer_links

FILES_EN = [
    'en/france/daycare-calculator/index.html',
    'en/france/housing-benefit-calculator/index.html',
    'en/france/mileage-calculator/index.html',
    'en/france/mutual-termination-calculator/index.html',
    'en/france/severance-calculator/index.html',
    'en/france/unemployment-calculator/index.html',
]

FILES_FR = [
    'fr/france/creche-tarifs/index.html',
    'fr/france/simulateur-apl/index.html',
    'fr/france/simulateur-chomage-are/index.html',
    'fr/france/simulateur-indemnite-kilometrique/index.html',
    'fr/france/simulateur-indemnite-licenciement/index.html',
    'fr/france/simulateur-rupture-conventionnelle/index.html',
]


def build_enriched_footer(lang):
    t = get_translations(lang)
    fl = get_footer_links(lang)
    countries = build_countries_dark(lang)

    return f'''    <footer class="bg-slate-900 text-slate-400 py-8 px-4">
        <div class="max-w-4xl mx-auto text-sm">
{countries}
            <div class="border-t border-slate-700 pt-4 text-center">
                <p>&copy; 2026 NetSalaire. {t['copyright']}</p>
                <div class="flex justify-center gap-4 mt-2">
                    <a href="{fl['faq']}" class="hover:text-white transition-colors">{t['faq']}</a>
                    <a href="{fl['legal']}" class="hover:text-white transition-colors">{t['legal']}</a>
                    <a href="{fl['privacy']}" class="hover:text-white transition-colors">{t['privacy']}</a>
                </div>
            </div>
        </div>
    </footer>'''


def fix_file(filepath, lang):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace entire footer
    pattern = re.compile(r'<footer[^>]*>.*?</footer>', re.DOTALL)
    match = pattern.search(content)
    if not match:
        return False

    new_footer = build_enriched_footer(lang)
    content = content[:match.start()] + new_footer + content[match.end():]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True


def main():
    count = 0
    for f in FILES_EN:
        path = os.path.join(BASE_DIR, f)
        if fix_file(path, 'en'):
            print(f"  Fixed: {f}")
            count += 1

    for f in FILES_FR:
        path = os.path.join(BASE_DIR, f)
        if fix_file(path, 'fr'):
            print(f"  Fixed: {f}")
            count += 1

    print(f"\nTotal: {count} files fixed")


if __name__ == '__main__':
    main()
