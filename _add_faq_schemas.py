#!/usr/bin/env python3
"""
Add FAQPage JSON-LD schema to pages that have FAQ sections but no schema.
"""

import os
import json

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))

# Pages and their FAQ Q&A pairs
PAGES_FAQ = {
    "fr/france/simulateur-impot-revenu/index.html": [
        {
            "name": "Qu'est-ce que le taux marginal d'imposition (TMI) ?",
            "text": "Le taux marginal d'imposition est le taux applique a la derniere tranche de vos revenus. Il determine l'economie realisee pour chaque euro deduit (PER, dons...). Par exemple, avec un TMI de 30%, chaque euro verse sur un PER vous fait economiser 30 centimes d'impot."
        },
        {
            "name": "Comment fonctionne le prelevement a la source ?",
            "text": "Depuis janvier 2019, l'impot est preleve chaque mois sur votre salaire par votre employeur. Le taux applique est personnalise selon votre derniere declaration. En septembre, ce taux est recalcule. Si vous avez trop paye, vous recevez un remboursement."
        },
        {
            "name": "Quelle difference entre reduction et credit d'impot ?",
            "text": "Une reduction d'impot diminue l'impot du, mais ne peut pas creer de remboursement. Un credit d'impot est rembourse meme si vous n'etes pas imposable. Les dons donnent une reduction, l'emploi a domicile donne un credit."
        },
        {
            "name": "Comment le PER reduit-il mon impot ?",
            "text": "Les versements sur un Plan d'Epargne Retraite sont deduits de votre revenu imposable (dans la limite d'un plafond). L'economie d'impot correspond a votre TMI : avec un TMI de 30%, vous economisez 30% du montant verse."
        },
        {
            "name": "A partir de quel revenu est-on imposable ?",
            "text": "En 2026, un celibataire devient imposable a partir d'environ 17 200 EUR de revenu net imposable (avant abattement). Pour un couple, le seuil est d'environ 32 200 EUR."
        },
        {
            "name": "Les heures supplementaires sont-elles imposables ?",
            "text": "Les heures supplementaires beneficient d'une exoneration d'impot sur le revenu dans la limite de 7 500 EUR par an. Au-dela de ce plafond, elles sont imposables normalement."
        },
        {
            "name": "Comment declarer des revenus fonciers ?",
            "text": "Les revenus fonciers s'ajoutent a vos autres revenus et sont imposes au bareme progressif. Deux regimes existent : le micro-foncier (abattement de 30% si loyers inferieurs a 15 000 EUR/an) ou le reel (deduction des charges reelles)."
        },
        {
            "name": "Quand et comment declarer ses revenus ?",
            "text": "La declaration se fait en ligne sur impots.gouv.fr entre avril et juin. Votre declaration est pre-remplie avec vos salaires et revenus connus de l'administration. Vous devez verifier et completer avec vos reductions/credits d'impot."
        }
    ],
    "fr/comparateur-salaire-france-maroc/index.html": [
        {
            "name": "Quel pays est le plus avantageux fiscalement ?",
            "text": "La France est souvent plus avantageuse fiscalement pour les salaries, surtout pour les familles grace au quotient familial. Pour un celibataire, la difference peut etre faible. N'oubliez pas que le cout de la vie est 40-60% moins eleve au Maroc."
        },
        {
            "name": "Comment fonctionne le quotient familial francais ?",
            "text": "Le quotient familial divise le revenu imposable par le nombre de parts : 1 part pour un celibataire, 2 parts pour un couple marie, +0.5 part pour les 2 premiers enfants, +1 part par enfant supplementaire. Cela reduit la progressivite de l'impot."
        },
        {
            "name": "Qu'est-ce que l'abattement familial au Maroc ?",
            "text": "Au Maroc, l'abattement familial est une reduction forfaitaire de 360 MAD par an et par personne a charge (conjoint + enfants), plafonnee a 2 160 MAD par an. C'est beaucoup moins avantageux que le quotient familial francais."
        },
        {
            "name": "Les MRE doivent-ils payer des impots en France ?",
            "text": "Les Marocains Residant en France sont soumis a l'impot francais sur leurs revenus de source francaise. Grace a la convention fiscale franco-marocaine, ils ne sont pas doublement imposes sur les memes revenus."
        },
        {
            "name": "Quelle est la difference entre CNSS et Securite sociale ?",
            "text": "La CNSS marocaine preleve environ 4,48% du salaire (plafonne a 6 000 MAD/mois) contre environ 22-25% pour les cotisations sociales francaises. La France finance chomage, retraite complete et allocations familiales, tandis que la CNSS offre une couverture plus limitee."
        },
        {
            "name": "Comment est calcule le taux de change ?",
            "text": "Notre comparateur utilise le taux de change EUR/MAD fourni par la Banque Centrale Europeenne via l'API Frankfurter. Le taux est mis a jour en temps reel. Vous pouvez egalement saisir un taux personnalise."
        },
        {
            "name": "Faut-il considerer le cout de la vie ?",
            "text": "Absolument ! Ce comparateur ne montre que la fiscalite. Le cout de la vie au Maroc est environ 40-60% moins eleve qu'en France. Un salaire net inferieur au Maroc peut donc offrir un meilleur pouvoir d'achat qu'en France."
        }
    ],
    "fr/france/simulateur-apl/index.html": [],  # Will check content
    "fr/maroc/simulateur-impot-revenu/index.html": [],  # Will check content
}


def build_faq_schema(questions):
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q["name"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": q["text"]
                }
            }
            for q in questions
        ]
    }
    return json.dumps(schema, indent=8, ensure_ascii=False)


def inject_faq_schema(filepath, questions):
    if not questions:
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'FAQPage' in content:
        print(f"  SKIP {filepath}: FAQPage already present")
        return False

    schema_json = build_faq_schema(questions)
    schema_block = f'''
    <!-- Schema.org FAQPage -->
    <script type="application/ld+json">
    {schema_json}
    </script>'''

    # Insert before </head>
    content = content.replace('</head>', schema_block + '\n</head>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True


def extract_faq_from_html(filepath):
    """Extract FAQ Q&A from HTML using simple text parsing."""
    import re

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    questions = []
    # Match question text in summary/h3 elements
    q_pattern = r'(?:font-medium|font-semibold)\s+text-slate-800[^>]*>([^<]+\?)</(?:span|h3)>'
    q_matches = re.finditer(q_pattern, content)

    for qm in q_matches:
        q_text = qm.group(1).strip()
        # Find the answer text after this question
        pos = qm.end()
        # Look for the next paragraph/div with answer text
        a_pattern = r'<p[^>]*class="[^"]*text-(?:sm\s+)?text-slate-(?:600|500)[^"]*"[^>]*>(.*?)</p>'
        a_match = re.search(a_pattern, content[pos:pos+1000])
        if a_match:
            a_text = re.sub(r'<[^>]+>', '', a_match.group(1)).strip()
            if len(a_text) > 20:  # Valid answer
                questions.append({"name": q_text, "text": a_text})

    return questions


def main():
    for rel_path, questions in PAGES_FAQ.items():
        filepath = os.path.join(SITE_ROOT, rel_path)
        if not os.path.exists(filepath):
            print(f"  MISSING: {rel_path}")
            continue

        # If no pre-defined questions, try to extract from HTML
        if not questions:
            questions = extract_faq_from_html(filepath)
            if not questions:
                print(f"  SKIP {rel_path}: no FAQ questions found")
                continue

        if inject_faq_schema(filepath, questions):
            print(f"  OK {rel_path}: {len(questions)} FAQ items added")
        else:
            print(f"  SKIP {rel_path}")


if __name__ == '__main__':
    main()
