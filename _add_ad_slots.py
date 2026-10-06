#!/usr/bin/env python3
"""Emplacements publicitaires fixes sur les pages les plus visitées (2026-10-06).

Trois blocs AdSense par page, posés à la main aux endroits qui gênent le moins
et rapportent le plus :
  1. juste sous le résultat du simulateur (bloc display responsive) ;
  2. au milieu de l'article (bloc In-Article) ;
  3. avant la FAQ ou en fin de page (bloc multiplex).
Jamais au-dessus du simulateur. Chaque bloc réserve sa hauteur (pas de saut de
page) : un emplacement vide ne prend aucune place, et n'affiche son
libellé « Publicité » qu'une fois rempli. Le reste du site
est couvert par les annonces automatiques (bannière du bas sur mobile, liens
d'intention, bannières espacées d'au moins 880 px).

Relançable : une page qui porte déjà les blocs n'est pas modifiée.
"""
from pathlib import Path

CLIENT = "ca-pub-8509347331076245"
SLOTS = {
    "resultat": ('data-ad-slot="4822195144" data-ad-format="auto" data-full-width-responsive="true"', 280),
    "article": ('data-ad-slot="5317019164" data-ad-layout="in-article" data-ad-format="fluid"', 250),
    "fin": ('data-ad-slot="4980968080" data-ad-format="autorelaxed"', 300),
}

STYLE = """    <style id="ns-ads">
      /* Un emplacement ne prend de place qu'une fois rempli : vide, il ne laisse pas de trou. */
      .ns-ad { margin: 0 auto; max-width: 100%; text-align: center; }
      .ns-ad__label { display: none; font-size: 11px; letter-spacing: .04em; text-transform: uppercase; color: #94a3b8; margin-bottom: .35rem; }
      /* Google réserve la hauteur pendant qu'il cherche une annonce : tant qu'elle
         n'est pas là, l'emplacement reste à zéro (la largeur suffit à la demande). */
      .ns-ad ins.adsbygoogle:not([data-ad-status="filled"]) { height: 0 !important; min-height: 0 !important; overflow: hidden; }
      .ns-ad:has(ins[data-ad-status="filled"]) { margin: 2rem auto; }
      .ns-ad:has(ins[data-ad-status="filled"]) .ns-ad__label { display: block; }
    </style>
"""


def bloc(kind: str) -> str:
    attrs, height = SLOTS[kind]
    return (
        f'            <div class="ns-ad ns-ad--{kind}">\n'
        f'                <span class="ns-ad__label">Publicité</span>\n'
        f'                <ins class="adsbygoogle" style="display:block" data-ad-client="{CLIENT}" {attrs}></ins>\n'
        f'                <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>\n'
        f'            </div>\n'
    )


# Page → [(repère, bloc, décalage)] : le bloc est inséré avant la ligne qui
# contient le repère, remontée de `décalage` lignes (pour passer devant la
# balise ouvrante d'une section dont le repère est le titre).
PAGES = {
    "fr/france/simulateur-chomage-are/index.html": [
        ('<section id="en-bref"', "resultat", 0),
        ("<!-- Conditions -->", "article", 0),
        ("<!-- FAQ -->", "fin", 0),
    ],
    "fr/france/simulateur-salaire-brut-net/index.html": [
        ('<section id="en-bref"', "resultat", 0),
        ("Tableau des taux de cotisations salariales 2026</h2>", "article", 1),
        ("<!-- FAQ Section -->", "fin", 0),
    ],
    "fr/espagne/simulateur-impot/index.html": [
        ("<!-- Example Calculation -->", "resultat", 0),
        ("<!-- Guide Complet Fiscalité Espagne -->", "article", 0),
        ("<!-- FAQ -->", "fin", 0),
    ],
    "fr/portugal/simulateur-impot/index.html": [
        ('<section id="en-bref"', "resultat", 0),
        ("Guide complet de la fiscalité portugaise</h2>", "article", 1),
        ("<!-- FAQ -->", "fin", 0),
    ],
    "fr/pays-bas/simulateur-impot/index.html": [
        ('<section id="en-bref"', "resultat", 0),
        ("<!-- Comprendre l'impôt aux Pays-Bas -->", "article", 0),
        ("<!-- FAQ -->", "fin", 0),
    ],
    "fr/france/simulateur-apl/index.html": [
        ("<!-- Informations -->", "resultat", 0),
        ("<!-- Plafonds de loyer -->", "article", 0),
        ("<!-- Autres simulateurs -->", "fin", 0),
    ],
}


def main():
    racine = Path(__file__).parent
    for rel, places in PAGES.items():
        path = racine / rel
        html = path.read_text(encoding="utf-8")
        if "ns-ad--" in html:
            print(f"déjà fait : {rel}")
            continue
        lines = html.split("\n")
        inserts = []
        for anchor, kind, back in places:
            idx = [i for i, l in enumerate(lines) if anchor in l]
            if len(idx) != 1:
                raise SystemExit(f"{rel} : repère « {anchor} » trouvé {len(idx)} fois")
            inserts.append((idx[0] - back, kind))
        for i, kind in sorted(inserts, reverse=True):
            lines[i:i] = bloc(kind).rstrip("\n").split("\n")
        html = "\n".join(lines)
        if 'id="ns-ads"' not in html:
            html = html.replace("</head>", STYLE + "</head>", 1)
        path.write_text(html, encoding="utf-8")
        print(f"3 blocs posés : {rel}")


if __name__ == "__main__":
    main()
