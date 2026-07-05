#!/usr/bin/env python3
"""
patch_v6_seo.py — V6 SEO fixes for netsalaire.com
NEVER touches simulateur-chomage-are or unemployment-calculator
"""

import os, re, json

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))

# PROTECTED PAGES — NEVER MODIFY
PROTECTED_SLUGS = [
    'simulateur-chomage-are',
    'unemployment-calculator',
]

def is_protected(filepath):
    for slug in PROTECTED_SLUGS:
        if slug in filepath:
            return True
    return False

# ============================================================
# 1. og:image:alt + og:image:width + og:image:height
# ============================================================
def patch_og_image_tags(html):
    if 'og:image:alt' in html:
        return html

    # Extract title for alt
    m = re.search(r'<title>([^<]+)</title>', html)
    alt = m.group(1).replace('"', '&quot;') if m else 'NetSalaire'

    # Case A: og:image exists → inject after it
    og_img = re.search(r'(<meta property="og:image" content="[^"]*">)', html)
    if og_img:
        block = (
            f'{og_img.group(1)}\n'
            f'    <meta property="og:image:alt" content="{alt}">\n'
            f'    <meta property="og:image:width" content="1200">\n'
            f'    <meta property="og:image:height" content="630">'
        )
        return html.replace(og_img.group(1), block, 1)

    # Case B: og:image missing (generated pages) → add og:image + alt/w/h after og:site_name
    site_name = re.search(r'(<meta property="og:site_name" content="[^"]*">)', html)
    if site_name:
        block = (
            f'{site_name.group(1)}\n'
            f'    <meta property="og:image" content="https://netsalaire.com/assets/images/og-home.png">\n'
            f'    <meta property="og:image:alt" content="{alt}">\n'
            f'    <meta property="og:image:width" content="1200">\n'
            f'    <meta property="og:image:height" content="630">'
        )
        return html.replace(site_name.group(1), block, 1)

    return html

# ============================================================
# 2. Twitter Card (for pages missing it)
# ============================================================
def patch_twitter_card(html):
    if 'twitter:card' in html:
        return html

    m_title = re.search(r'<meta property="og:title" content="([^"]*)">', html)
    m_desc = re.search(r'<meta property="og:description" content="([^"]*)">', html)
    m_img = re.search(r'<meta property="og:image" content="([^"]*)">', html)

    title = m_title.group(1) if m_title else ''
    desc = m_desc.group(1) if m_desc else ''
    img = m_img.group(1) if m_img else 'https://netsalaire.com/assets/images/og-home.png'

    twitter_block = (
        f'\n    <!-- Twitter Card -->\n'
        f'    <meta name="twitter:card" content="summary_large_image">\n'
        f'    <meta name="twitter:title" content="{title}">\n'
        f'    <meta name="twitter:description" content="{desc}">\n'
        f'    <meta name="twitter:image" content="{img}">'
    )

    # Insert after last og: tag
    og_matches = list(re.finditer(r'<meta property="og:[^"]*" content="[^"]*">', html))
    if og_matches:
        last_og = og_matches[-1]
        pos = last_og.end()
        return html[:pos] + twitter_block + html[pos:]

    return html

# ============================================================
# 3. BreadcrumbList JSON-LD
# ============================================================
COUNTRY_NAMES_FR = {
    'france': 'France', 'maroc': 'Maroc', 'allemagne': 'Allemagne',
    'espagne': 'Espagne', 'italie': 'Italie', 'portugal': 'Portugal',
    'belgique': 'Belgique', 'suisse': 'Suisse', 'luxembourg': 'Luxembourg',
    'royaume-uni': 'Royaume-Uni', 'usa': 'USA', 'canada': 'Canada',
    'bresil': 'Brésil', 'mexique': 'Mexique', 'argentine': 'Argentine',
    'chili': 'Chili', 'colombie': 'Colombie', 'perou': 'Pérou',
    'inde': 'Inde', 'chine': 'Chine', 'japon': 'Japon',
    'coree-du-sud': 'Corée du Sud', 'australie': 'Australie',
    'nouvelle-zelande': 'Nouvelle-Zélande', 'singapour': 'Singapour',
    'hong-kong': 'Hong Kong', 'thailande': 'Thaïlande',
    'malaisie': 'Malaisie', 'indonesie': 'Indonésie', 'vietnam': 'Vietnam',
    'philippines': 'Philippines', 'pakistan': 'Pakistan',
    'dubai': 'Dubai', 'arabie-saoudite': 'Arabie Saoudite',
    'qatar': 'Qatar', 'koweit': 'Koweït', 'egypte': 'Égypte',
    'afrique-du-sud': 'Afrique du Sud', 'turquie': 'Turquie',
    'pologne': 'Pologne', 'tchequie': 'Tchéquie', 'hongrie': 'Hongrie',
    'roumanie': 'Roumanie', 'croatie': 'Croatie', 'grece': 'Grèce',
    'danemark': 'Danemark', 'suede': 'Suède', 'norvege': 'Norvège',
    'finlande': 'Finlande', 'irlande': 'Irlande', 'pays-bas': 'Pays-Bas',
    'comparateur-global': 'Comparateur Global',
    'comparateur-salaire-france-maroc': 'Comparateur France-Maroc',
    'faq': 'FAQ', 'mentions-legales': 'Mentions légales',
    'politique-confidentialite': 'Confidentialité',
}

PAGE_NAMES_FR = {
    'simulateur-salaire-brut-net': 'Simulateur Brut Net',
    'simulateur-impot-revenu': 'Simulateur Impôt',
    'simulateur-impot': 'Simulateur Impôt',
    'simulateur-apl': 'Simulateur APL',
    'simulateur-indemnite-licenciement': 'Indemnité Licenciement',
    'simulateur-rupture-conventionnelle': 'Rupture Conventionnelle',
    'simulateur-indemnite-kilometrique': 'Indemnités Kilométriques',
    'creche-tarifs': 'Tarifs Crèche',
    'guide': 'Guide Fiscal',
    'simulateur-salaire-brut-net': 'Simulateur Brut Net',
}

PAGE_NAMES_EN = {
    'gross-to-net': 'Gross to Net',
    'income-tax': 'Income Tax',
    'housing-benefit-calculator': 'Housing Benefit',
    'severance-calculator': 'Severance Calculator',
    'mutual-termination-calculator': 'Mutual Termination',
    'mileage-calculator': 'Mileage Calculator',
    'daycare-calculator': 'Daycare Calculator',
    'tax-guide': 'Tax Guide',
    'unemployment-calculator': 'Unemployment Calculator',
}

# Map native language page slugs to readable names
NATIVE_PAGE_NAMES = {
    'einkommensteuer': 'Einkommensteuerrechner',
    'vergi-hesaplama': 'Vergi Hesaplama',
    'kalkulator-podatkowy': 'Kalkulator Podatkowy',
    'simulateur-impot': 'Simulateur Impôt',
}

def build_breadcrumb_items(filepath):
    rel = os.path.relpath(filepath, SITE_ROOT).replace('\\', '/')
    if rel.endswith('/index.html'):
        rel = rel[:-len('/index.html')]
    elif rel.endswith('index.html'):
        rel = rel[:-len('index.html')].rstrip('/')

    parts = [p for p in rel.split('/') if p]
    if not parts or len(parts) < 2:
        return None  # Home pages don't need breadcrumbs

    lang = parts[0]

    items = []
    # Home
    home_name = 'Accueil' if lang == 'fr' else 'Home'
    items.append((home_name, f'https://netsalaire.com/{lang}/'))

    if len(parts) >= 2:
        country_slug = parts[1]
        # Try FR names, then EN, then titlecase the slug
        country_name = COUNTRY_NAMES_FR.get(country_slug)
        if not country_name:
            country_name = country_slug.replace('-', ' ').title()

        if len(parts) == 2:
            items.append((country_name, None))
        else:
            items.append((country_name, f'https://netsalaire.com/{lang}/{country_slug}/'))

    if len(parts) >= 3:
        page_slug = parts[2]
        if lang == 'fr':
            page_name = PAGE_NAMES_FR.get(page_slug, page_slug.replace('-', ' ').title())
        elif lang == 'en':
            page_name = PAGE_NAMES_EN.get(page_slug, page_slug.replace('-', ' ').title())
        else:
            page_name = NATIVE_PAGE_NAMES.get(page_slug, page_slug.replace('-', ' ').title())
        items.append((page_name, None))

    return items


def patch_breadcrumbs(html, filepath):
    if 'BreadcrumbList' in html:
        return html

    items = build_breadcrumb_items(filepath)
    if not items or len(items) < 2:
        return html

    elements = []
    for i, (name, url) in enumerate(items, 1):
        el = {"@type": "ListItem", "position": i, "name": name}
        if url:
            el["item"] = url
        elements.append(el)

    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": elements
    }
    schema_json = json.dumps(schema, ensure_ascii=False, indent=8)

    block = f'\n    <script type="application/ld+json">\n    {schema_json}\n    </script>\n'

    # Insert before first existing ld+json
    m = re.search(r'(\s*<script type="application/ld\+json">)', html)
    if m:
        return html[:m.start()] + block + html[m.start():]

    # Or before </head>
    return html.replace('</head>', block + '</head>', 1)

# ============================================================
# 4. Byline + dates (E-E-A-T visible)
# ============================================================
def patch_byline(html, lang='fr'):
    if 'datetime="2026-01-15"' in html:
        return html  # Already has dates

    m = re.search(r'(</h1>)', html)
    if not m:
        return html

    if lang == 'fr':
        byline = (
            '</h1>\n'
            '                <div class="flex flex-wrap items-center justify-center gap-3 text-sm text-slate-500 mt-3">\n'
            '                    <span>Par <span class="font-medium text-slate-700">NetSalaire</span></span>\n'
            '                    <span class="text-slate-300">&middot;</span>\n'
            '                    <time datetime="2026-01-15">Publié le 15 janv. 2026</time>\n'
            '                    <span class="text-slate-300">&middot;</span>\n'
            '                    <time datetime="2026-06-20">Mis à jour le 20 juin 2026</time>\n'
            '                </div>'
        )
    elif lang == 'en':
        byline = (
            '</h1>\n'
            '                <div class="flex flex-wrap items-center justify-center gap-3 text-sm text-slate-500 mt-3">\n'
            '                    <span>By <span class="font-medium text-slate-700">NetSalaire</span></span>\n'
            '                    <span class="text-slate-300">&middot;</span>\n'
            '                    <time datetime="2026-01-15">Published Jan 15, 2026</time>\n'
            '                    <span class="text-slate-300">&middot;</span>\n'
            '                    <time datetime="2026-06-20">Updated Jun 20, 2026</time>\n'
            '                </div>'
        )
    else:
        return html  # Don't add byline for other languages

    return html.replace('</h1>', byline, 1)

# ============================================================
# 5. Fix broken SearchAction
# ============================================================
def fix_search_action(html):
    if '"SearchAction"' not in html:
        return html

    # Replace entire WebSite schema block with clean version (no SearchAction)
    pattern = r'<script type="application/ld\+json">\s*\{[^}]*"@type":\s*"WebSite".*?\}\s*\}\s*</script>'
    match = re.search(pattern, html, re.DOTALL)
    if not match:
        return html

    # Detect language
    lang_match = re.search(r'<html[^>]*lang="([^"]*)"', html)
    lang = lang_match.group(1) if lang_match else 'fr'

    new_schema = f'''<script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "NetSalaire",
        "url": "https://netsalaire.com/{lang}/"
    }}
    </script>'''

    return html[:match.start()] + new_schema + html[match.end():]

# ============================================================
# 6. Iconify sync → defer
# ============================================================
def fix_iconify_defer(html):
    old = '<script src="https://code.iconify.design/3/3.1.0/iconify.min.js"></script>'
    new = '<script defer src="https://code.iconify.design/3/3.1.0/iconify.min.js"></script>'
    return html.replace(old, new)

# ============================================================
# 7. Font preconnect (add where missing)
# ============================================================
def patch_font_preconnect(html):
    if 'preconnect' in html and 'fonts.googleapis.com' in html:
        return html  # Already has preconnect

    # Add preconnect before first font link
    font_link = re.search(r'(<link href="https://fonts\.googleapis\.com[^"]*" rel="stylesheet">)', html)
    if font_link:
        preconnect = (
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n    '
        )
        return html.replace(font_link.group(1), preconnect + font_link.group(1), 1)

    return html

# ============================================================
# MAIN
# ============================================================
def detect_lang(filepath):
    rel = os.path.relpath(filepath, SITE_ROOT).replace('\\', '/')
    parts = rel.split('/')
    if parts and len(parts[0]) <= 3:
        return parts[0]
    return 'fr'

def process_file(filepath):
    if is_protected(filepath):
        return 'protected'

    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    html = original
    lang = detect_lang(filepath)
    rel = os.path.relpath(filepath, SITE_ROOT)

    # Critical fixes — ALL pages
    html = patch_og_image_tags(html)
    html = patch_twitter_card(html)
    html = patch_breadcrumbs(html, filepath)
    html = fix_iconify_defer(html)
    html = patch_font_preconnect(html)

    # Byline — only FR and EN manual pages (france/*, maroc/*, home)
    is_manual_fr = ('fr/france/' in rel or 'fr/maroc/' in rel) and lang == 'fr'
    is_manual_en = ('en/france/' in rel or 'en/morocco/' in rel) and lang == 'en'
    is_home = rel in ('fr/index.html', 'en/index.html')

    if is_manual_fr or is_home and lang == 'fr':
        html = patch_byline(html, 'fr')
    elif is_manual_en or is_home and lang == 'en':
        html = patch_byline(html, 'en')

    # Fix SearchAction — only home pages
    if is_home:
        html = fix_search_action(html)

    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return 'patched'

    return 'unchanged'


def main():
    patched = 0
    protected = 0
    unchanged = 0

    for root, dirs, files in os.walk(SITE_ROOT):
        dirs[:] = [d for d in dirs if d not in ('node_modules', '.git', 'admin', '__pycache__')]
        for f in files:
            if not f.endswith('.html'):
                continue
            filepath = os.path.join(root, f)
            result = process_file(filepath)
            rel = os.path.relpath(filepath, SITE_ROOT)
            if result == 'patched':
                patched += 1
                print(f'  PATCHED: {rel}')
            elif result == 'protected':
                protected += 1
                print(f'  PROTECTED: {rel}')
            else:
                unchanged += 1

    print(f'\n=== DONE ===')
    print(f'  Patched:   {patched}')
    print(f'  Protected: {protected}')
    print(f'  Unchanged: {unchanged}')


if __name__ == '__main__':
    main()
