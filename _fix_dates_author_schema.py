#!/usr/bin/env python3
"""
Add datePublished, dateModified, and author to WebApplication schemas.
Also add Article schema for editorial content sections.
"""

import os
import re
import glob

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
TODAY = "2026-08-17"
PUBLISHED = "2026-01-15"

ARTICLE_SCHEMA = '''
    <!-- Schema.org Article (E-E-A-T editorial content) -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{headline}",
        "description": "{description}",
        "url": "{url}",
        "datePublished": "{published}",
        "dateModified": "{modified}",
        "author": {{
            "@type": "Person",
            "name": "Mottalib Radif",
            "jobTitle": "Fondateur de NetSalaire",
            "url": "https://netsalaire.com/fr/a-propos/"
        }},
        "publisher": {{
            "@type": "Organization",
            "name": "NetSalaire",
            "url": "https://netsalaire.com",
            "logo": {{
                "@type": "ImageObject",
                "url": "https://netsalaire.com/assets/images/logo-512.png"
            }}
        }},
        "mainEntityOfPage": {{
            "@type": "WebPage",
            "@id": "{url}"
        }},
        "inLanguage": "fr"
    }}
    </script>'''

# Pages to add Article schema to (those with substantial editorial content)
PAGES = {
    "fr/france/simulateur-salaire-brut-net/index.html": {
        "headline": "Simulateur Salaire Brut Net 2026 - Cadre et Non-Cadre",
        "description": "Convertir brut en net gratuitement. Calcul salaire brut net selon statut cadre ou non-cadre. Baremes 2026.",
        "url": "https://netsalaire.com/fr/france/simulateur-salaire-brut-net/"
    },
    "fr/france/simulateur-impot-revenu/index.html": {
        "headline": "Simulateur Impot sur le Revenu France 2026",
        "description": "Calculez votre impot sur le revenu en France avec quotient familial, tranches IR et simulation PER. Bareme 2026 officiel.",
        "url": "https://netsalaire.com/fr/france/simulateur-impot-revenu/"
    },
    "fr/comparateur-salaire-france-maroc/index.html": {
        "headline": "Comparateur Salaire France vs Maroc 2026 - Net et Impots",
        "description": "Simulateur fiscal gratuit pour MRE : compare ton salaire net entre la France et le Maroc.",
        "url": "https://netsalaire.com/fr/comparateur-salaire-france-maroc/"
    },
    "fr/france/simulateur-chomage-are/index.html": {
        "headline": "Simulateur Chomage ARE 2026 - Calcul Allocation",
        "description": "Calculez votre allocation chomage ARE en France. Simulation gratuite avec les baremes 2026.",
        "url": "https://netsalaire.com/fr/france/simulateur-chomage-are/"
    },
    "fr/france/simulateur-apl/index.html": {
        "headline": "Simulateur APL 2026 - Aide Personnalisee au Logement",
        "description": "Estimez votre aide au logement APL en France. Calcul gratuit selon zone, loyer et revenus.",
        "url": "https://netsalaire.com/fr/france/simulateur-apl/"
    },
    "fr/maroc/simulateur-salaire-brut-net/index.html": {
        "headline": "Simulateur Salaire Brut Net Maroc 2026",
        "description": "Calculez votre salaire net au Maroc. Cotisations CNSS, AMO et IR marocain. Baremes 2026.",
        "url": "https://netsalaire.com/fr/maroc/simulateur-salaire-brut-net/"
    },
    "fr/maroc/simulateur-impot-revenu/index.html": {
        "headline": "Simulateur Impot sur le Revenu Maroc 2026",
        "description": "Calculez votre IR au Maroc avec CNSS, AMO et abattement familial. Baremes 2026 officiels.",
        "url": "https://netsalaire.com/fr/maroc/simulateur-impot-revenu/"
    },
    "fr/faq/index.html": {
        "headline": "FAQ - Questions Frequentes sur les Simulateurs Fiscaux",
        "description": "Reponses aux questions frequentes sur le calcul du salaire brut net, l'impot sur le revenu et les cotisations sociales.",
        "url": "https://netsalaire.com/fr/faq/"
    },
}


def fix_file(rel_path, page_info):
    filepath = os.path.join(SITE_ROOT, rel_path)
    if not os.path.exists(filepath):
        print(f"  SKIP {rel_path}: file not found")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    changes = []

    # 1. Enrich WebApplication schema with datePublished, dateModified, author
    if '"@type": "WebApplication"' in content and '"datePublished"' not in content:
        old_pattern = '"operatingSystem": "Web"\n    }'
        new_replacement = '''"operatingSystem": "Web",
        "datePublished": "''' + PUBLISHED + '''",
        "dateModified": "''' + TODAY + '''",
        "author": {
            "@type": "Person",
            "name": "Mottalib Radif",
            "url": "https://netsalaire.com/fr/a-propos/"
        }
    }'''
        if old_pattern in content:
            content = content.replace(old_pattern, new_replacement, 1)
            changes.append("WebApplication enriched with dates+author")

    # 2. Add Article schema if not present
    if '"@type": "Article"' not in content and '</head>' in content:
        article = ARTICLE_SCHEMA.format(
            headline=page_info["headline"],
            description=page_info["description"],
            url=page_info["url"],
            published=PUBLISHED,
            modified=TODAY
        )
        # Insert before Person schema or before </head>
        if '<!-- Schema.org Person' in content:
            content = content.replace(
                '    <!-- Schema.org Person',
                article + '\n\n    <!-- Schema.org Person',
                1
            )
        else:
            content = content.replace('</head>', article + '\n</head>')
        changes.append("Article schema added")

    if changes:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  OK {rel_path}: {', '.join(changes)}")
        return True

    print(f"  SKIP {rel_path}: no changes needed")
    return False


def main():
    modified = 0
    for rel_path, info in PAGES.items():
        if fix_file(rel_path, info):
            modified += 1
    print(f"\nDone: {modified} files modified.")


if __name__ == '__main__':
    main()
