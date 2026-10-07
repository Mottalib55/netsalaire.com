#!/usr/bin/env python3
"""
Generate native-language country tax pages.
Creates 33 pages in 22 languages from FR source pages.
"""

import os
import re
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_URL = 'https://netsalaire.com'

# ============================================================
# COUNTRY CONFIGURATION (33 countries)
# ============================================================
COUNTRIES = [
    # (lang, fr_slug, en_slug, native_country_slug, native_page_slug, country_name_native, flag, currency, flag_icon, text_dir)
    # German
    ('de', 'allemagne', 'germany', 'deutschland', 'einkommensteuer', 'Deutschland', '\U0001f1e9\U0001f1ea', 'EUR', 'circle-flags:de', 'ltr'),
    ('de', 'autriche', 'austria', 'oesterreich', 'einkommensteuer', '\u00d6sterreich', '\U0001f1e6\U0001f1f9', 'EUR', 'circle-flags:at', 'ltr'),
    ('de', 'suisse', 'switzerland', 'schweiz', 'einkommensteuer', 'Schweiz', '\U0001f1e8\U0001f1ed', 'CHF', 'circle-flags:ch', 'ltr'),
    # Spanish
    ('es', 'espagne', 'spain', 'espana', 'simulador-impuestos', 'Espa\u00f1a', '\U0001f1ea\U0001f1f8', 'EUR', 'circle-flags:es', 'ltr'),
    ('es', 'mexique', 'mexico', 'mexico', 'simulador-impuestos', 'M\u00e9xico', '\U0001f1f2\U0001f1fd', 'MXN', 'circle-flags:mx', 'ltr'),
    ('es', 'argentine', 'argentina', 'argentina', 'simulador-impuestos', 'Argentina', '\U0001f1e6\U0001f1f7', 'ARS', 'circle-flags:ar', 'ltr'),
    ('es', 'chili', 'chile', 'chile', 'simulador-impuestos', 'Chile', '\U0001f1e8\U0001f1f1', 'CLP', 'circle-flags:cl', 'ltr'),
    ('es', 'colombie', 'colombia', 'colombia', 'simulador-impuestos', 'Colombia', '\U0001f1e8\U0001f1f4', 'COP', 'circle-flags:co', 'ltr'),
    ('es', 'perou', 'peru', 'peru', 'simulador-impuestos', 'Per\u00fa', '\U0001f1f5\U0001f1ea', 'PEN', 'circle-flags:pe', 'ltr'),
    # Portuguese
    ('pt', 'portugal', 'portugal', 'portugal', 'simulador-impostos', 'Portugal', '\U0001f1f5\U0001f1f9', 'EUR', 'circle-flags:pt', 'ltr'),
    ('pt', 'bresil', 'brazil', 'brasil', 'simulador-impostos', 'Brasil', '\U0001f1e7\U0001f1f7', 'BRL', 'circle-flags:br', 'ltr'),
    # Dutch
    ('nl', 'pays-bas', 'netherlands', 'nederland', 'belasting-berekenen', 'Nederland', '\U0001f1f3\U0001f1f1', 'EUR', 'circle-flags:nl', 'ltr'),
    ('nl', 'belgique', 'belgium', 'belgie', 'belasting-berekenen', 'Belgi\u00eb', '\U0001f1e7\U0001f1ea', 'EUR', 'circle-flags:be', 'ltr'),
    # Arabic
    ('ar', 'arabie-saoudite', 'saudi-arabia', 'arabie-saoudite', 'tax-calculator', '\u0627\u0644\u0633\u0639\u0648\u062f\u064a\u0629', '\U0001f1f8\U0001f1e6', 'SAR', 'circle-flags:sa', 'rtl'),
    ('ar', 'dubai', 'dubai', 'dubai', 'tax-calculator', '\u062f\u0628\u064a', '\U0001f1e6\U0001f1ea', 'AED', 'circle-flags:ae', 'rtl'),
    ('ar', 'qatar', 'qatar', 'qatar', 'tax-calculator', '\u0642\u0637\u0631', '\U0001f1f6\U0001f1e6', 'QAR', 'circle-flags:qa', 'rtl'),
    ('ar', 'koweit', 'kuwait', 'koweit', 'tax-calculator', '\u0627\u0644\u0643\u0648\u064a\u062a', '\U0001f1f0\U0001f1fc', 'KWD', 'circle-flags:kw', 'rtl'),
    ('ar', 'egypte', 'egypt', 'egypte', 'tax-calculator', '\u0645\u0635\u0631', '\U0001f1ea\U0001f1ec', 'EGP', 'circle-flags:eg', 'rtl'),
    # Italian
    ('it', 'italie', 'italy', 'italia', 'calcolatore-imposte', 'Italia', '\U0001f1ee\U0001f1f9', 'EUR', 'circle-flags:it', 'ltr'),
    # Swedish
    ('sv', 'suede', 'sweden', 'sverige', 'skatteberaknare', 'Sverige', '\U0001f1f8\U0001f1ea', 'SEK', 'circle-flags:se', 'ltr'),
    # Norwegian
    ('no', 'norvege', 'norway', 'norge', 'skattekalkulator', 'Norge', '\U0001f1f3\U0001f1f4', 'NOK', 'circle-flags:no', 'ltr'),
    # Danish
    ('da', 'danemark', 'denmark', 'danmark', 'skatteberegner', 'Danmark', '\U0001f1e9\U0001f1f0', 'DKK', 'circle-flags:dk', 'ltr'),
    # Finnish
    ('fi', 'finlande', 'finland', 'suomi', 'verolaskuri', 'Suomi', '\U0001f1eb\U0001f1ee', 'EUR', 'circle-flags:fi', 'ltr'),
    # Greek
    ('el', 'grece', 'greece', 'ellada', 'ypologismos-forou', '\u0395\u03bb\u03bb\u03ac\u03b4\u03b1', '\U0001f1ec\U0001f1f7', 'EUR', 'circle-flags:gr', 'ltr'),
    # Polish
    ('pl', 'pologne', 'poland', 'polska', 'kalkulator-podatkowy', 'Polska', '\U0001f1f5\U0001f1f1', 'PLN', 'circle-flags:pl', 'ltr'),
    # Czech
    ('cs', 'tchequie', 'czech-republic', 'cesko', 'danovy-kalkulator', '\u010cesko', '\U0001f1e8\U0001f1ff', 'CZK', 'circle-flags:cz', 'ltr'),
    # Hungarian
    ('hu', 'hongrie', 'hungary', 'magyarorszag', 'ado-kalkulator', 'Magyarorsz\u00e1g', '\U0001f1ed\U0001f1fa', 'HUF', 'circle-flags:hu', 'ltr'),
    # Romanian
    ('ro', 'roumanie', 'romania', 'romania', 'calculator-impozit', 'Rom\u00e2nia', '\U0001f1f7\U0001f1f4', 'RON', 'circle-flags:ro', 'ltr'),
    # Croatian
    ('hr', 'croatie', 'croatia', 'hrvatska', 'porezni-kalkulator', 'Hrvatska', '\U0001f1ed\U0001f1f7', 'EUR', 'circle-flags:hr', 'ltr'),
    # Turkish
    ('tr', 'turquie', 'turkey', 'turkiye', 'vergi-hesaplama', 'T\u00fcrkiye', '\U0001f1f9\U0001f1f7', 'TRY', 'circle-flags:tr', 'ltr'),
    # Japanese
    ('ja', 'japon', 'japan', 'nihon', 'zeikin-keisan', '\u65e5\u672c', '\U0001f1ef\U0001f1f5', 'JPY', 'circle-flags:jp', 'ltr'),
    # Korean
    ('ko', 'coree-du-sud', 'south-korea', 'hanguk', 'segeum-gyesan', '\ud55c\uad6d', '\U0001f1f0\U0001f1f7', 'KRW', 'circle-flags:kr', 'ltr'),
    # Chinese
    ('zh', 'chine', 'china', 'zhongguo', 'shuishou-jisuan', '\u4e2d\u56fd', '\U0001f1e8\U0001f1f3', 'CNY', 'circle-flags:cn', 'ltr'),
    # Thai
    ('th', 'thailande', 'thailand', 'prathet-thai', 'khamnuan-phasi', '\u0e1b\u0e23\u0e30\u0e40\u0e17\u0e28\u0e44\u0e17\u0e22', '\U0001f1f9\U0001f1ed', 'THB', 'circle-flags:th', 'ltr'),
    # Malay
    ('ms', 'malaisie', 'malaysia', 'malaysia', 'kalkulator-cukai', 'Malaysia', '\U0001f1f2\U0001f1fe', 'MYR', 'circle-flags:my', 'ltr'),
    # Indonesian
    ('id', 'indonesie', 'indonesia', 'indonesia', 'kalkulator-pajak', 'Indonesia', '\U0001f1ee\U0001f1e9', 'IDR', 'circle-flags:id', 'ltr'),
    # Vietnamese
    ('vi', 'vietnam', 'vietnam', 'viet-nam', 'tinh-thue', 'Vi\u1ec7t Nam', '\U0001f1fb\U0001f1f3', 'VND', 'circle-flags:vn', 'ltr'),
]

# ============================================================
# UI TRANSLATIONS (22 languages x ~50 strings)
# ============================================================
UI = {
    'de': {
        'title': 'Einkommensteuerrechner {country} 2026 - Kostenlose Berechnung',
        'meta_desc': 'Berechnen Sie Ihre Steuern in {country} kostenlos. Detaillierte Simulation mit Einkommensteuer und Sozialabgaben. Steuertarife 2026.',
        'h1': 'Einkommensteuerrechner {country}',
        'h1_year': '2026',
        'subtitle': 'Berechnen Sie Ihre Steuern in {country}: Einkommensteuer + Sozialabgaben',
        'monthly_income': 'Monatliches Einkommen',
        'annual_income': 'J\u00e4hrliches Einkommen',
        'income_tax': 'Einkommensteuer',
        'effective_rate': 'Effektiver Steuersatz',
        'social_contributions': 'Sozialabgaben',
        'employee_share': '~{rate}% (Arbeitnehmer)',
        'net_annual': 'Jahresnettoeinkommen',
        'net_monthly': 'Monatlich',
        'income_breakdown': 'Aufschl\u00fcsselung Ihres Einkommens',
        'net_label': 'Nettoeinkommen',
        'tax_label': 'Steuern',
        'social_label': 'Sozialabgaben',
        'total_tax_burden': 'Gesamte Steuerbelastung',
        'total_effective_rate': 'Gesamter effektiver Steuersatz',
        'tax_brackets': 'Steuertarife {country} 2026',
        'compare_title': 'Mit \u00e4hnlichen L\u00e4ndern vergleichen',
        'compare_btn': 'Mit anderen L\u00e4ndern vergleichen',
        'footer_copy': '\u00a9 2026 NetSalaire. Steuerberechnungen sind Sch\u00e4tzungen zu Informationszwecken.',
        'faq': 'FAQ',
        'legal': 'Impressum',
        'privacy': 'Datenschutz',
        'lang_native': 'Deutsch',
        'lang_flag': '\U0001f1e9\U0001f1ea',
        'simulator_link': 'Rechner',
        'net': 'Netto',
    },
    'es': {
        'title': 'Simulador de Impuestos {country} 2026 - C\u00e1lculo Gratuito',
        'meta_desc': 'Calcule sus impuestos en {country} gratuitamente. Simulaci\u00f3n detallada con impuesto sobre la renta y cotizaciones sociales. Baremos 2026.',
        'h1': 'Simulador de Impuestos {country}',
        'h1_year': '2026',
        'subtitle': 'Calcule sus impuestos en {country}: Impuesto sobre la renta + Cotizaciones sociales',
        'monthly_income': 'Ingreso Mensual',
        'annual_income': 'Ingreso Anual',
        'income_tax': 'Impuesto sobre la Renta',
        'effective_rate': 'Tasa efectiva',
        'social_contributions': 'Cotizaciones Sociales',
        'employee_share': '~{rate}% (empleado)',
        'net_annual': 'Ingreso Neto Anual',
        'net_monthly': 'Mensual',
        'income_breakdown': 'Desglose de su ingreso',
        'net_label': 'Ingreso neto',
        'tax_label': 'Impuestos',
        'social_label': 'Cotizaciones',
        'total_tax_burden': 'Carga Fiscal Total',
        'total_effective_rate': 'Tasa efectiva total',
        'tax_brackets': 'Baremos {country} 2026',
        'compare_title': 'Comparar con pa\u00edses similares',
        'compare_btn': 'Comparar con otros pa\u00edses',
        'footer_copy': '\u00a9 2026 NetSalaire. Los c\u00e1lculos fiscales son estimaciones informativas.',
        'faq': 'FAQ',
        'legal': 'Aviso legal',
        'privacy': 'Privacidad',
        'lang_native': 'Espa\u00f1ol',
        'lang_flag': '\U0001f1ea\U0001f1f8',
        'simulator_link': 'Simulador',
        'net': 'Neto',
    },
    'pt': {
        'title': 'Simulador de Impostos {country} 2026 - C\u00e1lculo Gratuito',
        'meta_desc': 'Calcule seus impostos em {country} gratuitamente. Simula\u00e7\u00e3o detalhada com imposto de renda e contribui\u00e7\u00f5es sociais. Tabelas 2026.',
        'h1': 'Simulador de Impostos {country}',
        'h1_year': '2026',
        'subtitle': 'Calcule seus impostos em {country}: Imposto de renda + Contribui\u00e7\u00f5es sociais',
        'monthly_income': 'Renda Mensal',
        'annual_income': 'Renda Anual',
        'income_tax': 'Imposto de Renda',
        'effective_rate': 'Taxa efetiva',
        'social_contributions': 'Contribui\u00e7\u00f5es Sociais',
        'employee_share': '~{rate}% (empregado)',
        'net_annual': 'Renda L\u00edquida Anual',
        'net_monthly': 'Mensal',
        'income_breakdown': 'Distribui\u00e7\u00e3o da sua renda',
        'net_label': 'Renda l\u00edquida',
        'tax_label': 'Impostos',
        'social_label': 'Contribui\u00e7\u00f5es',
        'total_tax_burden': 'Carga Tribut\u00e1ria Total',
        'total_effective_rate': 'Taxa efetiva total',
        'tax_brackets': 'Tabelas {country} 2026',
        'compare_title': 'Comparar com pa\u00edses similares',
        'compare_btn': 'Comparar com outros pa\u00edses',
        'footer_copy': '\u00a9 2026 NetSalaire. Os c\u00e1lculos fiscais s\u00e3o estimativas informativas.',
        'faq': 'FAQ',
        'legal': 'Aviso legal',
        'privacy': 'Privacidade',
        'lang_native': 'Portugu\u00eas',
        'lang_flag': '\U0001f1f5\U0001f1f9',
        'simulator_link': 'Simulador',
        'net': 'L\u00edquido',
    },
    'nl': {
        'title': 'Belastingcalculator {country} 2026 - Gratis Berekening',
        'meta_desc': 'Bereken uw belastingen in {country} gratis. Gedetailleerde simulatie met inkomstenbelasting en sociale premies. Tarieven 2026.',
        'h1': 'Belastingcalculator {country}',
        'h1_year': '2026',
        'subtitle': 'Bereken uw belastingen in {country}: Inkomstenbelasting + Sociale premies',
        'monthly_income': 'Maandelijks Inkomen',
        'annual_income': 'Jaarlijks Inkomen',
        'income_tax': 'Inkomstenbelasting',
        'effective_rate': 'Effectief tarief',
        'social_contributions': 'Sociale Premies',
        'employee_share': '~{rate}% (werknemer)',
        'net_annual': 'Jaarlijks Netto-inkomen',
        'net_monthly': 'Maandelijks',
        'income_breakdown': 'Verdeling van uw inkomen',
        'net_label': 'Netto-inkomen',
        'tax_label': 'Belastingen',
        'social_label': 'Premies',
        'total_tax_burden': 'Totale Belastingdruk',
        'total_effective_rate': 'Totaal effectief tarief',
        'tax_brackets': 'Belastingtarieven {country} 2026',
        'compare_title': 'Vergelijk met vergelijkbare landen',
        'compare_btn': 'Vergelijk met andere landen',
        'footer_copy': '\u00a9 2026 NetSalaire. Belastingberekeningen zijn schattingen ter informatie.',
        'faq': 'FAQ',
        'legal': 'Juridische informatie',
        'privacy': 'Privacy',
        'lang_native': 'Nederlands',
        'lang_flag': '\U0001f1f3\U0001f1f1',
        'simulator_link': 'Calculator',
        'net': 'Netto',
    },
    'ar': {
        'title': '\u062d\u0627\u0633\u0628\u0629 \u0627\u0644\u0636\u0631\u0627\u0626\u0628 {country} 2026 - \u062d\u0633\u0627\u0628 \u0645\u062c\u0627\u0646\u064a',
        'meta_desc': '\u0627\u062d\u0633\u0628 \u0636\u0631\u0627\u0626\u0628\u0643 \u0641\u064a {country} \u0645\u062c\u0627\u0646\u0627\u064b. \u0645\u062d\u0627\u0643\u0627\u0629 \u0645\u0641\u0635\u0644\u0629 \u0645\u0639 \u0636\u0631\u064a\u0628\u0629 \u0627\u0644\u062f\u062e\u0644 \u0648\u0627\u0644\u0627\u0634\u062a\u0631\u0627\u0643\u0627\u062a \u0627\u0644\u0627\u062c\u062a\u0645\u0627\u0639\u064a\u0629. \u062c\u062f\u0627\u0648\u0644 2026.',
        'h1': '\u062d\u0627\u0633\u0628\u0629 \u0627\u0644\u0636\u0631\u0627\u0626\u0628 {country}',
        'h1_year': '2026',
        'subtitle': '\u0627\u062d\u0633\u0628 \u0636\u0631\u0627\u0626\u0628\u0643 \u0641\u064a {country}: \u0636\u0631\u064a\u0628\u0629 \u0627\u0644\u062f\u062e\u0644 + \u0627\u0644\u0627\u0634\u062a\u0631\u0627\u0643\u0627\u062a \u0627\u0644\u0627\u062c\u062a\u0645\u0627\u0639\u064a\u0629',
        'monthly_income': '\u0627\u0644\u062f\u062e\u0644 \u0627\u0644\u0634\u0647\u0631\u064a',
        'annual_income': '\u0627\u0644\u062f\u062e\u0644 \u0627\u0644\u0633\u0646\u0648\u064a',
        'income_tax': '\u0636\u0631\u064a\u0628\u0629 \u0627\u0644\u062f\u062e\u0644',
        'effective_rate': '\u0627\u0644\u0645\u0639\u062f\u0644 \u0627\u0644\u0641\u0639\u0644\u064a',
        'social_contributions': '\u0627\u0644\u0627\u0634\u062a\u0631\u0627\u0643\u0627\u062a \u0627\u0644\u0627\u062c\u062a\u0645\u0627\u0639\u064a\u0629',
        'employee_share': '~{rate}% (\u0645\u0648\u0638\u0641)',
        'net_annual': '\u0627\u0644\u062f\u062e\u0644 \u0627\u0644\u0635\u0627\u0641\u064a \u0627\u0644\u0633\u0646\u0648\u064a',
        'net_monthly': '\u0634\u0647\u0631\u064a',
        'income_breakdown': '\u062a\u0648\u0632\u064a\u0639 \u062f\u062e\u0644\u0643',
        'net_label': '\u0627\u0644\u062f\u062e\u0644 \u0627\u0644\u0635\u0627\u0641\u064a',
        'tax_label': '\u0627\u0644\u0636\u0631\u0627\u0626\u0628',
        'social_label': '\u0627\u0644\u0627\u0634\u062a\u0631\u0627\u0643\u0627\u062a',
        'total_tax_burden': '\u0625\u062c\u0645\u0627\u0644\u064a \u0627\u0644\u0639\u0628\u0621 \u0627\u0644\u0636\u0631\u064a\u0628\u064a',
        'total_effective_rate': '\u0627\u0644\u0645\u0639\u062f\u0644 \u0627\u0644\u0641\u0639\u0644\u064a \u0627\u0644\u0625\u062c\u0645\u0627\u0644\u064a',
        'tax_brackets': '\u062c\u062f\u0627\u0648\u0644 \u0627\u0644\u0636\u0631\u0627\u0626\u0628 {country} 2026',
        'compare_title': '\u0642\u0627\u0631\u0646 \u0645\u0639 \u062f\u0648\u0644 \u0645\u0634\u0627\u0628\u0647\u0629',
        'compare_btn': '\u0642\u0627\u0631\u0646 \u0645\u0639 \u062f\u0648\u0644 \u0623\u062e\u0631\u0649',
        'footer_copy': '\u00a9 2026 NetSalaire. \u0627\u0644\u062d\u0633\u0627\u0628\u0627\u062a \u0627\u0644\u0636\u0631\u064a\u0628\u064a\u0629 \u0647\u064a \u062a\u0642\u062f\u064a\u0631\u0627\u062a \u0644\u0623\u063a\u0631\u0627\u0636 \u0625\u0639\u0644\u0627\u0645\u064a\u0629.',
        'faq': '\u0627\u0644\u0623\u0633\u0626\u0644\u0629 \u0627\u0644\u0634\u0627\u0626\u0639\u0629',
        'legal': '\u0625\u0634\u0639\u0627\u0631 \u0642\u0627\u0646\u0648\u0646\u064a',
        'privacy': '\u0627\u0644\u062e\u0635\u0648\u0635\u064a\u0629',
        'lang_native': '\u0627\u0644\u0639\u0631\u0628\u064a\u0629',
        'lang_flag': '\U0001f1f8\U0001f1e6',
        'simulator_link': '\u062d\u0627\u0633\u0628\u0629',
        'net': '\u0635\u0627\u0641\u064a',
    },
    'it': {
        'title': 'Calcolatore Imposte {country} 2026 - Calcolo Gratuito',
        'meta_desc': 'Calcola le tue tasse in {country} gratuitamente. Simulazione dettagliata con imposta sul reddito e contributi sociali. Aliquote 2026.',
        'h1': 'Calcolatore Imposte {country}',
        'h1_year': '2026',
        'subtitle': 'Calcola le tue tasse in {country}: Imposta sul reddito + Contributi sociali',
        'monthly_income': 'Reddito Mensile',
        'annual_income': 'Reddito Annuale',
        'income_tax': 'Imposta sul Reddito',
        'effective_rate': 'Aliquota effettiva',
        'social_contributions': 'Contributi Sociali',
        'employee_share': '~{rate}% (dipendente)',
        'net_annual': 'Reddito Netto Annuale',
        'net_monthly': 'Mensile',
        'income_breakdown': 'Ripartizione del tuo reddito',
        'net_label': 'Reddito netto',
        'tax_label': 'Imposte',
        'social_label': 'Contributi',
        'total_tax_burden': 'Carico Fiscale Totale',
        'total_effective_rate': 'Aliquota effettiva totale',
        'tax_brackets': 'Aliquote {country} 2026',
        'compare_title': 'Confronta con paesi simili',
        'compare_btn': 'Confronta con altri paesi',
        'footer_copy': '\u00a9 2026 NetSalaire. I calcoli fiscali sono stime a scopo informativo.',
        'faq': 'FAQ',
        'legal': 'Note legali',
        'privacy': 'Privacy',
        'lang_native': 'Italiano',
        'lang_flag': '\U0001f1ee\U0001f1f9',
        'simulator_link': 'Calcolatore',
        'net': 'Netto',
    },
    'sv': {
        'title': 'Skatteberäknare {country} 2026 - Gratis Beräkning',
        'meta_desc': 'Beräkna dina skatter i {country} gratis. Detaljerad simulering med inkomstskatt och sociala avgifter. Skattesatser 2026.',
        'h1': 'Skatteberäknare {country}',
        'h1_year': '2026',
        'subtitle': 'Beräkna dina skatter i {country}: Inkomstskatt + Sociala avgifter',
        'monthly_income': 'Månadsinkomst',
        'annual_income': 'Årsinkomst',
        'income_tax': 'Inkomstskatt',
        'effective_rate': 'Effektiv skattesats',
        'social_contributions': 'Sociala Avgifter',
        'employee_share': '~{rate}% (anställd)',
        'net_annual': 'Årlig Nettoinkomst',
        'net_monthly': 'Månadsvis',
        'income_breakdown': 'Fördelning av din inkomst',
        'net_label': 'Nettoinkomst',
        'tax_label': 'Skatter',
        'social_label': 'Avgifter',
        'total_tax_burden': 'Total Skattebörda',
        'total_effective_rate': 'Total effektiv skattesats',
        'tax_brackets': 'Skattesatser {country} 2026',
        'compare_title': 'Jämför med liknande länder',
        'compare_btn': 'Jämför med andra länder',
        'footer_copy': '© 2026 NetSalaire. Skatteberäkningar är uppskattningar i informationssyfte.',
        'faq': 'FAQ',
        'legal': 'Juridisk information',
        'privacy': 'Integritet',
        'lang_native': 'Svenska',
        'lang_flag': '🇸🇪',
        'simulator_link': 'Beräknare',
        'net': 'Netto',
    },
    'no': {
        'title': 'Skattekalkulator {country} 2026 - Gratis Beregning',
        'meta_desc': 'Beregn skattene dine i {country} gratis. Detaljert simulering med inntektsskatt og sosiale avgifter. Skattesatser 2026.',
        'h1': 'Skattekalkulator {country}',
        'h1_year': '2026',
        'subtitle': 'Beregn skattene dine i {country}: Inntektsskatt + Sosiale avgifter',
        'monthly_income': 'Månedsinntekt',
        'annual_income': 'Årsinntekt',
        'income_tax': 'Inntektsskatt',
        'effective_rate': 'Effektiv skattesats',
        'social_contributions': 'Sosiale Avgifter',
        'employee_share': '~{rate}% (ansatt)',
        'net_annual': 'Årlig Nettoinntekt',
        'net_monthly': 'Månedlig',
        'income_breakdown': 'Fordeling av inntekten din',
        'net_label': 'Nettoinntekt',
        'tax_label': 'Skatter',
        'social_label': 'Avgifter',
        'total_tax_burden': 'Total Skattebyrde',
        'total_effective_rate': 'Total effektiv skattesats',
        'tax_brackets': 'Skattesatser {country} 2026',
        'compare_title': 'Sammenlign med lignende land',
        'compare_btn': 'Sammenlign med andre land',
        'footer_copy': '© 2026 NetSalaire. Skatteberegninger er estimater for informasjonsformål.',
        'faq': 'FAQ',
        'legal': 'Juridisk informasjon',
        'privacy': 'Personvern',
        'lang_native': 'Norsk',
        'lang_flag': '🇳🇴',
        'simulator_link': 'Kalkulator',
        'net': 'Netto',
    },
    'da': {
        'title': 'Skatteberegner {country} 2026 - Gratis Beregning',
        'meta_desc': 'Beregn dine skatter i {country} gratis. Detaljeret simulering med indkomstskat og sociale bidrag. Skattesatser 2026.',
        'h1': 'Skatteberegner {country}',
        'h1_year': '2026',
        'subtitle': 'Beregn dine skatter i {country}: Indkomstskat + Sociale bidrag',
        'monthly_income': 'Månedlig Indkomst',
        'annual_income': 'Årlig Indkomst',
        'income_tax': 'Indkomstskat',
        'effective_rate': 'Effektiv skattesats',
        'social_contributions': 'Sociale Bidrag',
        'employee_share': '~{rate}% (ansat)',
        'net_annual': 'Årlig Nettoindkomst',
        'net_monthly': 'Månedlig',
        'income_breakdown': 'Fordeling af din indkomst',
        'net_label': 'Nettoindkomst',
        'tax_label': 'Skatter',
        'social_label': 'Bidrag',
        'total_tax_burden': 'Samlet Skattebyrde',
        'total_effective_rate': 'Samlet effektiv skattesats',
        'tax_brackets': 'Skattesatser {country} 2026',
        'compare_title': 'Sammenlign med lignende lande',
        'compare_btn': 'Sammenlign med andre lande',
        'footer_copy': '© 2026 NetSalaire. Skatteberegninger er estimater til informationsformål.',
        'faq': 'FAQ',
        'legal': 'Juridisk information',
        'privacy': 'Privatlivspolitik',
        'lang_native': 'Dansk',
        'lang_flag': '<iconify-icon icon="circle-flags:dk" width="16"></iconify-icon>',
        'simulator_link': 'Beregner',
        'net': 'Netto',
    },
    'fi': {
        'title': 'Verolaskuri {country} 2026 - Ilmainen Laskenta',
        'meta_desc': 'Laske verot {country} ilmaiseksi. Yksityiskohtainen simulaatio tuloverolla ja sosiaalimaksuilla. Veroprosentit 2026.',
        'h1': 'Verolaskuri {country}',
        'h1_year': '2026',
        'subtitle': 'Laske verot {country}: Tulovero + Sosiaalimaksut',
        'monthly_income': 'Kuukausitulot',
        'annual_income': 'Vuositulot',
        'income_tax': 'Tulovero',
        'effective_rate': 'Efektiivinen veroprosentti',
        'social_contributions': 'Sosiaalimaksut',
        'employee_share': '~{rate}% (työntekijä)',
        'net_annual': 'Vuotuinen Nettotulo',
        'net_monthly': 'Kuukausittain',
        'income_breakdown': 'Tulojesi jakautuminen',
        'net_label': 'Nettotulo',
        'tax_label': 'Verot',
        'social_label': 'Maksut',
        'total_tax_burden': 'Kokonaisverorasitus',
        'total_effective_rate': 'Kokonaisveroprosentti',
        'tax_brackets': 'Veroprosentit {country} 2026',
        'compare_title': 'Vertaa samankaltaisiin maihin',
        'compare_btn': 'Vertaa muihin maihin',
        'footer_copy': '© 2026 NetSalaire. Verolaskelmat ovat arvioita tiedotustarkoituksiin.',
        'faq': 'UKK',
        'legal': 'Oikeudellinen ilmoitus',
        'privacy': 'Tietosuoja',
        'lang_native': 'Suomi',
        'lang_flag': '🇫🇮',
        'simulator_link': 'Laskuri',
        'net': 'Netto',
    },
    'el': {
        'title': 'Υπολογισμός Φόρου {country} 2026 - Δωρεάν Υπολογισμός',
        'meta_desc': 'Υπολογίστε τους φόρους σας στην {country} δωρεάν. Λεπτομερής προσομοίωση με φόρο εισοδήματος και κοινωνικές εισφορές. Κλίμακες 2026.',
        'h1': 'Υπολογισμός Φόρου {country}',
        'h1_year': '2026',
        'subtitle': 'Υπολογίστε τους φόρους σας στην {country}: Φόρος εισοδήματος + Κοινωνικές εισφορές',
        'monthly_income': 'Μηνιαίο Εισόδημα',
        'annual_income': 'Ετήσιο Εισόδημα',
        'income_tax': 'Φόρος Εισοδήματος',
        'effective_rate': 'Πραγματικός συντελεστής',
        'social_contributions': 'Κοινωνικές Εισφορές',
        'employee_share': '~{rate}% (εργαζόμενος)',
        'net_annual': 'Ετήσιο Καθαρό Εισόδημα',
        'net_monthly': 'Μηνιαίο',
        'income_breakdown': 'Κατανομή του εισοδήματός σας',
        'net_label': 'Καθαρό εισόδημα',
        'tax_label': 'Φόροι',
        'social_label': 'Εισφορές',
        'total_tax_burden': 'Συνολικό Φορολογικό Βάρος',
        'total_effective_rate': 'Συνολικός πραγματικός συντελεστής',
        'tax_brackets': 'Φορολογικές Κλίμακες {country} 2026',
        'compare_title': 'Σύγκριση με παρόμοιες χώρες',
        'compare_btn': 'Σύγκριση με άλλες χώρες',
        'footer_copy': '© 2026 NetSalaire. Οι φορολογικοί υπολογισμοί είναι εκτιμήσεις για ενημερωτικούς σκοπούς.',
        'faq': 'FAQ',
        'legal': 'Νομική σημείωση',
        'privacy': 'Απόρρητο',
        'lang_native': 'Ελληνικά',
        'lang_flag': '<iconify-icon icon="circle-flags:gr" width="16"></iconify-icon>',
        'simulator_link': 'Υπολογιστής',
        'net': 'Καθαρά',
    },
    'pl': {
        'title': 'Kalkulator Podatkowy {country} 2026 - Bezpłatne Obliczenie',
        'meta_desc': 'Oblicz swoje podatki w {country} za darmo. Szczegółowa symulacja z podatkiem dochodowym i składkami społecznymi. Stawki 2026.',
        'h1': 'Kalkulator Podatkowy {country}',
        'h1_year': '2026',
        'subtitle': 'Oblicz swoje podatki w {country}: Podatek dochodowy + Składki społeczne',
        'monthly_income': 'Dochód Miesięczny',
        'annual_income': 'Dochód Roczny',
        'income_tax': 'Podatek Dochodowy',
        'effective_rate': 'Stawka efektywna',
        'social_contributions': 'Składki Społeczne',
        'employee_share': '~{rate}% (pracownik)',
        'net_annual': 'Roczny Dochód Netto',
        'net_monthly': 'Miesięcznie',
        'income_breakdown': 'Podział Twojego dochodu',
        'net_label': 'Dochód netto',
        'tax_label': 'Podatki',
        'social_label': 'Składki',
        'total_tax_burden': 'Całkowite Obciążenie Podatkowe',
        'total_effective_rate': 'Całkowita stawka efektywna',
        'tax_brackets': 'Stawki Podatkowe {country} 2026',
        'compare_title': 'Porównaj z podobnymi krajami',
        'compare_btn': 'Porównaj z innymi krajami',
        'footer_copy': '© 2026 NetSalaire. Obliczenia podatkowe są szacunkami w celach informacyjnych.',
        'faq': 'FAQ',
        'legal': 'Informacje prawne',
        'privacy': 'Prywatność',
        'lang_native': 'Polski',
        'lang_flag': '🇵🇱',
        'simulator_link': 'Kalkulator',
        'net': 'Netto',
    },
    'cs': {
        'title': 'Daňový Kalkulátor {country} 2026 - Bezplatný Výpočet',
        'meta_desc': 'Vypočítejte si daně v {country} zdarma. Podrobná simulace s daní z příjmu a sociálním pojištěním. Sazby 2026.',
        'h1': 'Daňový Kalkulátor {country}',
        'h1_year': '2026',
        'subtitle': 'Vypočítejte si daně v {country}: Daň z příjmu + Sociální pojištění',
        'monthly_income': 'Měsíční Příjem',
        'annual_income': 'Roční Příjem',
        'income_tax': 'Daň z Příjmu',
        'effective_rate': 'Efektivní sazba',
        'social_contributions': 'Sociální Pojištění',
        'employee_share': '~{rate}% (zaměstnanec)',
        'net_annual': 'Roční Čistý Příjem',
        'net_monthly': 'Měsíčně',
        'income_breakdown': 'Rozložení vašeho příjmu',
        'net_label': 'Čistý příjem',
        'tax_label': 'Daně',
        'social_label': 'Pojištění',
        'total_tax_burden': 'Celkové Daňové Zatížení',
        'total_effective_rate': 'Celková efektivní sazba',
        'tax_brackets': 'Daňové Sazby {country} 2026',
        'compare_title': 'Srovnat s podobnými zeměmi',
        'compare_btn': 'Srovnat s jinými zeměmi',
        'footer_copy': '© 2026 NetSalaire. Daňové výpočty jsou odhady pro informační účely.',
        'faq': 'FAQ',
        'legal': 'Právní informace',
        'privacy': 'Ochrana soukromí',
        'lang_native': 'Čeština',
        'lang_flag': '<iconify-icon icon="circle-flags:cz" width="16"></iconify-icon>',
        'simulator_link': 'Kalkulátor',
        'net': 'Čistý',
    },
    'hu': {
        'title': 'Adókalkulátor {country} 2026 - Ingyenes Számítás',
        'meta_desc': 'Számítsa ki adóit {country} ingyenesen. Részletes szimuláció jövedelemadóval és társadalombiztosítási járulékokkal. 2026-os kulcsok.',
        'h1': 'Adókalkulátor {country}',
        'h1_year': '2026',
        'subtitle': 'Számítsa ki adóit {country}: Jövedelemadó + Társadalombiztosítás',
        'monthly_income': 'Havi Jövedelem',
        'annual_income': 'Éves Jövedelem',
        'income_tax': 'Jövedelemadó',
        'effective_rate': 'Effektív adókulcs',
        'social_contributions': 'TB Járulékok',
        'employee_share': '~{rate}% (munkavállaló)',
        'net_annual': 'Éves Nettó Jövedelem',
        'net_monthly': 'Havonta',
        'income_breakdown': 'Jövedelmed megoszlása',
        'net_label': 'Nettó jövedelem',
        'tax_label': 'Adók',
        'social_label': 'Járulékok',
        'total_tax_burden': 'Összes Adóteher',
        'total_effective_rate': 'Összes effektív adókulcs',
        'tax_brackets': 'Adókulcsok {country} 2026',
        'compare_title': 'Összehasonlítás hasonló országokkal',
        'compare_btn': 'Összehasonlítás más országokkal',
        'footer_copy': '© 2026 NetSalaire. Az adószámítások tájékoztató jellegű becslések.',
        'faq': 'GYIK',
        'legal': 'Jogi nyilatkozat',
        'privacy': 'Adatvédelem',
        'lang_native': 'Magyar',
        'lang_flag': '🇭🇺',
        'simulator_link': 'Kalkulátor',
        'net': 'Nettó',
    },
    'ro': {
        'title': 'Calculator Impozit {country} 2026 - Calcul Gratuit',
        'meta_desc': 'Calculați-vă impozitele în {country} gratuit. Simulare detaliată cu impozit pe venit și contribuții sociale. Cote 2026.',
        'h1': 'Calculator Impozit {country}',
        'h1_year': '2026',
        'subtitle': 'Calculați-vă impozitele în {country}: Impozit pe venit + Contribuții sociale',
        'monthly_income': 'Venit Lunar',
        'annual_income': 'Venit Anual',
        'income_tax': 'Impozit pe Venit',
        'effective_rate': 'Rata efectivă',
        'social_contributions': 'Contribuții Sociale',
        'employee_share': '~{rate}% (angajat)',
        'net_annual': 'Venit Net Anual',
        'net_monthly': 'Lunar',
        'income_breakdown': 'Distribuția venitului dvs.',
        'net_label': 'Venit net',
        'tax_label': 'Impozite',
        'social_label': 'Contribuții',
        'total_tax_burden': 'Sarcina Fiscală Totală',
        'total_effective_rate': 'Rata efectivă totală',
        'tax_brackets': 'Cote de Impozitare {country} 2026',
        'compare_title': 'Comparați cu țări similare',
        'compare_btn': 'Comparați cu alte țări',
        'footer_copy': '© 2026 NetSalaire. Calculele fiscale sunt estimări în scop informativ.',
        'faq': 'FAQ',
        'legal': 'Mențiuni legale',
        'privacy': 'Confidențialitate',
        'lang_native': 'Română',
        'lang_flag': '🇷🇴',
        'simulator_link': 'Calculator',
        'net': 'Net',
    },
    'hr': {
        'title': 'Porezni Kalkulator {country} 2026 - Besplatno Izračunavanje',
        'meta_desc': 'Izračunajte svoje poreze u {country} besplatno. Detaljna simulacija s porezom na dohodak i socijalnim doprinosima. Stope 2026.',
        'h1': 'Porezni Kalkulator {country}',
        'h1_year': '2026',
        'subtitle': 'Izračunajte svoje poreze u {country}: Porez na dohodak + Socijalni doprinosi',
        'monthly_income': 'Mjesečni Prihod',
        'annual_income': 'Godišnji Prihod',
        'income_tax': 'Porez na Dohodak',
        'effective_rate': 'Efektivna stopa',
        'social_contributions': 'Socijalni Doprinosi',
        'employee_share': '~{rate}% (zaposlenik)',
        'net_annual': 'Godišnji Neto Prihod',
        'net_monthly': 'Mjesečno',
        'income_breakdown': 'Raspodjela vašeg prihoda',
        'net_label': 'Neto prihod',
        'tax_label': 'Porezi',
        'social_label': 'Doprinosi',
        'total_tax_burden': 'Ukupno Porezno Opterećenje',
        'total_effective_rate': 'Ukupna efektivna stopa',
        'tax_brackets': 'Porezne Stope {country} 2026',
        'compare_title': 'Usporedite sa sličnim zemljama',
        'compare_btn': 'Usporedite s drugim zemljama',
        'footer_copy': '© 2026 NetSalaire. Porezni izračuni su procjene u informativne svrhe.',
        'faq': 'FAQ',
        'legal': 'Pravne informacije',
        'privacy': 'Privatnost',
        'lang_native': 'Hrvatski',
        'lang_flag': '🇭🇷',
        'simulator_link': 'Kalkulator',
        'net': 'Neto',
    },
    'tr': {
        'title': 'Vergi Hesaplama {country} 2026 - Ücretsiz Hesaplama',
        'meta_desc': '{country} vergilerinizi ücretsiz hesaplayın. Gelir vergisi ve sosyal güvenlik primleri ile detaylı simülasyon. 2026 oranları.',
        'h1': 'Vergi Hesaplama {country}',
        'h1_year': '2026',
        'subtitle': '{country} vergilerinizi hesaplayın: Gelir vergisi + Sosyal güvenlik primleri',
        'monthly_income': 'Aylık Gelir',
        'annual_income': 'Yıllık Gelir',
        'income_tax': 'Gelir Vergisi',
        'effective_rate': 'Efektif oran',
        'social_contributions': 'Sosyal Güvenlik Primleri',
        'employee_share': '~{rate}% (çalışan)',
        'net_annual': 'Yıllık Net Gelir',
        'net_monthly': 'Aylık',
        'income_breakdown': 'Gelirinizin dağılımı',
        'net_label': 'Net gelir',
        'tax_label': 'Vergiler',
        'social_label': 'Primler',
        'total_tax_burden': 'Toplam Vergi Yükü',
        'total_effective_rate': 'Toplam efektif oran',
        'tax_brackets': 'Vergi Oranları {country} 2026',
        'compare_title': 'Benzer ülkelerle karşılaştırın',
        'compare_btn': 'Diğer ülkelerle karşılaştırın',
        'footer_copy': '© 2026 NetSalaire. Vergi hesaplamaları bilgilendirme amaçlı tahminlerdir.',
        'faq': 'SSS',
        'legal': 'Yasal bilgiler',
        'privacy': 'Gizlilik',
        'lang_native': 'Türkçe',
        'lang_flag': '🇹🇷',
        'simulator_link': 'Hesaplama',
        'net': 'Net',
    },
    'ja': {
        'title': '税金計算 {country} 2026 - 無料計算',
        'meta_desc': '{country}の税金を無料で計算。所得税と社会保険料の詳細シミュレーション。2026年の税率。',
        'h1': '税金計算 {country}',
        'h1_year': '2026',
        'subtitle': '{country}の税金を計算：所得税 + 社会保険料',
        'monthly_income': '月収',
        'annual_income': '年収',
        'income_tax': '所得税',
        'effective_rate': '実効税率',
        'social_contributions': '社会保険料',
        'employee_share': '~{rate}%（従業員）',
        'net_annual': '年間手取り',
        'net_monthly': '月額',
        'income_breakdown': '収入の内訳',
        'net_label': '手取り',
        'tax_label': '税金',
        'social_label': '社会保険',
        'total_tax_burden': '合計税負担',
        'total_effective_rate': '合計実効税率',
        'tax_brackets': '税率 {country} 2026',
        'compare_title': '類似国と比較',
        'compare_btn': '他の国と比較',
        'footer_copy': '© 2026 NetSalaire. 税計算は情報提供目的の推定値です。',
        'faq': 'FAQ',
        'legal': '法的情報',
        'privacy': 'プライバシー',
        'lang_native': '日本語',
        'lang_flag': '🇯🇵',
        'simulator_link': '計算機',
        'net': '手取り',
    },
    'ko': {
        'title': '세금 계산기 {country} 2026 - 무료 계산',
        'meta_desc': '{country}의 세금을 무료로 계산하세요. 소득세와 사회보험료의 상세 시뮬레이션. 2026년 세율.',
        'h1': '세금 계산기 {country}',
        'h1_year': '2026',
        'subtitle': '{country} 세금 계산: 소득세 + 사회보험료',
        'monthly_income': '월 소득',
        'annual_income': '연 소득',
        'income_tax': '소득세',
        'effective_rate': '실효세율',
        'social_contributions': '사회보험료',
        'employee_share': '~{rate}% (근로자)',
        'net_annual': '연간 순소득',
        'net_monthly': '월간',
        'income_breakdown': '소득 분배',
        'net_label': '순소득',
        'tax_label': '세금',
        'social_label': '보험료',
        'total_tax_burden': '총 세금 부담',
        'total_effective_rate': '총 실효세율',
        'tax_brackets': '세율 {country} 2026',
        'compare_title': '유사 국가와 비교',
        'compare_btn': '다른 국가와 비교',
        'footer_copy': '© 2026 NetSalaire. 세금 계산은 정보 제공 목적의 추정치입니다.',
        'faq': 'FAQ',
        'legal': '법적 고지',
        'privacy': '개인정보',
        'lang_native': '한국어',
        'lang_flag': '<iconify-icon icon="circle-flags:kr" width="16"></iconify-icon>',
        'simulator_link': '계산기',
        'net': '순',
    },
    'zh': {
        'title': '税收计算器 {country} 2026 - 免费计算',
        'meta_desc': '免费计算{country}的税收。包含所得税和社会保险的详细模拟。2026年税率。',
        'h1': '税收计算器 {country}',
        'h1_year': '2026',
        'subtitle': '计算{country}税收：所得税 + 社会保险',
        'monthly_income': '月收入',
        'annual_income': '年收入',
        'income_tax': '所得税',
        'effective_rate': '实际税率',
        'social_contributions': '社会保险',
        'employee_share': '~{rate}%（员工）',
        'net_annual': '年净收入',
        'net_monthly': '月度',
        'income_breakdown': '收入分配',
        'net_label': '净收入',
        'tax_label': '税金',
        'social_label': '社保',
        'total_tax_burden': '总税负',
        'total_effective_rate': '总实际税率',
        'tax_brackets': '税率 {country} 2026',
        'compare_title': '与类似国家比较',
        'compare_btn': '与其他国家比较',
        'footer_copy': '© 2026 NetSalaire. 税收计算为信息参考目的的估算值。',
        'faq': '常见问题',
        'legal': '法律声明',
        'privacy': '隐私政策',
        'lang_native': '中文',
        'lang_flag': '<iconify-icon icon="circle-flags:cn" width="16"></iconify-icon>',
        'simulator_link': '计算器',
        'net': '净',
    },
    'th': {
        'title': 'คำนวณภาษี {country} 2026 - คำนวณฟรี',
        'meta_desc': 'คำนวณภาษีของคุณใน{country}ฟรี การจำลองโดยละเอียดพร้อมภาษีเงินได้และเงินสมทบประกันสังคม อัตราภาษี 2026',
        'h1': 'คำนวณภาษี {country}',
        'h1_year': '2026',
        'subtitle': 'คำนวณภาษีของคุณใน{country}: ภาษีเงินได้ + เงินสมทบประกันสังคม',
        'monthly_income': 'รายได้รายเดือน',
        'annual_income': 'รายได้รายปี',
        'income_tax': 'ภาษีเงินได้',
        'effective_rate': 'อัตราภาษีที่แท้จริง',
        'social_contributions': 'เงินสมทบประกันสังคม',
        'employee_share': '~{rate}% (ลูกจ้าง)',
        'net_annual': 'รายได้สุทธิรายปี',
        'net_monthly': 'รายเดือน',
        'income_breakdown': 'การกระจายรายได้ของคุณ',
        'net_label': 'รายได้สุทธิ',
        'tax_label': 'ภาษี',
        'social_label': 'ประกันสังคม',
        'total_tax_burden': 'ภาระภาษีรวม',
        'total_effective_rate': 'อัตราภาษีรวมที่แท้จริง',
        'tax_brackets': 'อัตราภาษี {country} 2026',
        'compare_title': 'เปรียบเทียบกับประเทศที่คล้ายกัน',
        'compare_btn': 'เปรียบเทียบกับประเทศอื่น',
        'footer_copy': '© 2026 NetSalaire. การคำนวณภาษีเป็นการประมาณการเพื่อวัตถุประสงค์ในการให้ข้อมูล',
        'faq': 'FAQ',
        'legal': 'ข้อมูลทางกฎหมาย',
        'privacy': 'ความเป็นส่วนตัว',
        'lang_native': 'ไทย',
        'lang_flag': '<iconify-icon icon="circle-flags:th" width="16"></iconify-icon>',
        'simulator_link': 'เครื่องคำนวณ',
        'net': 'สุทธิ',
    },
    'ms': {
        'title': 'Kalkulator Cukai {country} 2026 - Pengiraan Percuma',
        'meta_desc': 'Kira cukai anda di {country} secara percuma. Simulasi terperinci dengan cukai pendapatan dan caruman sosial. Kadar 2026.',
        'h1': 'Kalkulator Cukai {country}',
        'h1_year': '2026',
        'subtitle': 'Kira cukai anda di {country}: Cukai pendapatan + Caruman sosial',
        'monthly_income': 'Pendapatan Bulanan',
        'annual_income': 'Pendapatan Tahunan',
        'income_tax': 'Cukai Pendapatan',
        'effective_rate': 'Kadar efektif',
        'social_contributions': 'Caruman Sosial',
        'employee_share': '~{rate}% (pekerja)',
        'net_annual': 'Pendapatan Bersih Tahunan',
        'net_monthly': 'Bulanan',
        'income_breakdown': 'Pecahan pendapatan anda',
        'net_label': 'Pendapatan bersih',
        'tax_label': 'Cukai',
        'social_label': 'Caruman',
        'total_tax_burden': 'Jumlah Beban Cukai',
        'total_effective_rate': 'Jumlah kadar efektif',
        'tax_brackets': 'Kadar Cukai {country} 2026',
        'compare_title': 'Bandingkan dengan negara serupa',
        'compare_btn': 'Bandingkan dengan negara lain',
        'footer_copy': '© 2026 NetSalaire. Pengiraan cukai adalah anggaran untuk tujuan maklumat.',
        'faq': 'FAQ',
        'legal': 'Maklumat undang-undang',
        'privacy': 'Privasi',
        'lang_native': 'Bahasa Melayu',
        'lang_flag': '🇲🇾',
        'simulator_link': 'Kalkulator',
        'net': 'Bersih',
    },
    'id': {
        'title': 'Kalkulator Pajak {country} 2026 - Perhitungan Gratis',
        'meta_desc': 'Hitung pajak Anda di {country} secara gratis. Simulasi terperinci dengan pajak penghasilan dan iuran sosial. Tarif 2026.',
        'h1': 'Kalkulator Pajak {country}',
        'h1_year': '2026',
        'subtitle': 'Hitung pajak Anda di {country}: Pajak penghasilan + Iuran sosial',
        'monthly_income': 'Penghasilan Bulanan',
        'annual_income': 'Penghasilan Tahunan',
        'income_tax': 'Pajak Penghasilan',
        'effective_rate': 'Tarif efektif',
        'social_contributions': 'Iuran Sosial',
        'employee_share': '~{rate}% (karyawan)',
        'net_annual': 'Penghasilan Bersih Tahunan',
        'net_monthly': 'Bulanan',
        'income_breakdown': 'Rincian penghasilan Anda',
        'net_label': 'Penghasilan bersih',
        'tax_label': 'Pajak',
        'social_label': 'Iuran',
        'total_tax_burden': 'Total Beban Pajak',
        'total_effective_rate': 'Total tarif efektif',
        'tax_brackets': 'Tarif Pajak {country} 2026',
        'compare_title': 'Bandingkan dengan negara serupa',
        'compare_btn': 'Bandingkan dengan negara lain',
        'footer_copy': '© 2026 NetSalaire. Perhitungan pajak adalah estimasi untuk tujuan informasi.',
        'faq': 'FAQ',
        'legal': 'Informasi hukum',
        'privacy': 'Privasi',
        'lang_native': 'Bahasa Indonesia',
        'lang_flag': '🇮🇩',
        'simulator_link': 'Kalkulator',
        'net': 'Bersih',
    },
    'vi': {
        'title': 'Tính Thuế {country} 2026 - Tính Miễn Phí',
        'meta_desc': 'Tính thuế của bạn tại {country} miễn phí. Mô phỏng chi tiết với thuế thu nhập và bảo hiểm xã hội. Biểu thuế 2026.',
        'h1': 'Tính Thuế {country}',
        'h1_year': '2026',
        'subtitle': 'Tính thuế của bạn tại {country}: Thuế thu nhập + Bảo hiểm xã hội',
        'monthly_income': 'Thu Nhập Hàng Tháng',
        'annual_income': 'Thu Nhập Hàng Năm',
        'income_tax': 'Thuế Thu Nhập',
        'effective_rate': 'Thuế suất thực tế',
        'social_contributions': 'Bảo Hiểm Xã Hội',
        'employee_share': '~{rate}% (người lao động)',
        'net_annual': 'Thu Nhập Ròng Hàng Năm',
        'net_monthly': 'Hàng tháng',
        'income_breakdown': 'Phân bổ thu nhập của bạn',
        'net_label': 'Thu nhập ròng',
        'tax_label': 'Thuế',
        'social_label': 'Bảo hiểm',
        'total_tax_burden': 'Tổng Gánh Nặng Thuế',
        'total_effective_rate': 'Tổng thuế suất thực tế',
        'tax_brackets': 'Biểu Thuế {country} 2026',
        'compare_title': 'So sánh với các quốc gia tương tự',
        'compare_btn': 'So sánh với các quốc gia khác',
        'footer_copy': '© 2026 NetSalaire. Các tính toán thuế là ước tính mang tính chất tham khảo.',
        'faq': 'FAQ',
        'legal': 'Thông tin pháp lý',
        'privacy': 'Quyền riêng tư',
        'lang_native': 'Tiếng Việt',
        'lang_flag': '🇻🇳',
        'simulator_link': 'Máy tính',
        'net': 'Ròng',
    },
}

# Google Fonts for special scripts
SPECIAL_FONTS = {
    'ar': 'Noto+Sans+Arabic:wght@300;400;500;600;700',
    'ja': 'Noto+Sans+JP:wght@300;400;500;600;700',
    'ko': 'Noto+Sans+KR:wght@300;400;500;600;700',
    'zh': 'Noto+Sans+SC:wght@300;400;500;600;700',
    'th': 'Noto+Sans+Thai:wght@300;400;500;600;700',
}

FONT_FAMILIES = {
    'ar': "'Noto Sans Arabic', 'Inter', sans-serif",
    'ja': "'Noto Sans JP', 'Inter', sans-serif",
    'ko': "'Noto Sans KR', 'Inter', sans-serif",
    'zh': "'Noto Sans SC', 'Inter', sans-serif",
    'th': "'Noto Sans Thai', 'Inter', sans-serif",
}

# Locale codes for toLocaleString
LOCALE_MAP = {
    'de': 'de-DE', 'es': 'es-ES', 'pt': 'pt-PT', 'nl': 'nl-NL',
    'ar': 'ar-SA', 'it': 'it-IT', 'sv': 'sv-SE', 'no': 'nb-NO',
    'da': 'da-DK', 'fi': 'fi-FI', 'el': 'el-GR', 'pl': 'pl-PL',
    'cs': 'cs-CZ', 'hu': 'hu-HU', 'ro': 'ro-RO', 'hr': 'hr-HR',
    'tr': 'tr-TR', 'ja': 'ja-JP', 'ko': 'ko-KR', 'zh': 'zh-CN',
    'th': 'th-TH', 'ms': 'ms-MY', 'id': 'id-ID', 'vi': 'vi-VN',
}

# Comparison links per country (fr_slug -> list of (fr_slug, native_name) for similar countries)
COMPARISONS = {
    'allemagne': [('belgique', 'Belgien'), ('pays-bas', 'Niederlande'), ('autriche', '\u00d6sterreich'), ('suisse', 'Schweiz')],
    'autriche': [('allemagne', 'Deutschland'), ('suisse', 'Schweiz'), ('hongrie', 'Ungarn'), ('tchequie', 'Tschechien')],
    'suisse': [('allemagne', 'Deutschland'), ('autriche', '\u00d6sterreich'), ('italie', 'Italien'), ('france', 'Frankreich')],
    'espagne': [('portugal', 'Portugal'), ('italie', 'Italia'), ('france', 'Francia'), ('mexique', 'M\u00e9xico')],
    'mexique': [('colombie', 'Colombia'), ('chili', 'Chile'), ('perou', 'Per\u00fa'), ('argentine', 'Argentina')],
    'argentine': [('chili', 'Chile'), ('colombie', 'Colombia'), ('bresil', 'Brasil'), ('perou', 'Per\u00fa')],
    'chili': [('argentine', 'Argentina'), ('perou', 'Per\u00fa'), ('colombie', 'Colombia'), ('mexique', 'M\u00e9xico')],
    'colombie': [('mexique', 'M\u00e9xico'), ('perou', 'Per\u00fa'), ('chili', 'Chile'), ('argentine', 'Argentina')],
    'perou': [('colombie', 'Colombia'), ('chili', 'Chile'), ('mexique', 'M\u00e9xico'), ('argentine', 'Argentina')],
    'portugal': [('espagne', 'Espa\u00f1a'), ('bresil', 'Brasil'), ('france', 'Fran\u00e7a'), ('italie', 'It\u00e1lia')],
    'bresil': [('portugal', 'Portugal'), ('argentine', 'Argentina'), ('mexique', 'M\u00e9xico'), ('colombie', 'Col\u00f4mbia')],
    'pays-bas': [('belgique', 'Belgi\u00eb'), ('allemagne', 'Duitsland'), ('luxembourg', 'Luxemburg'), ('royaume-uni', 'VK')],
    'belgique': [('pays-bas', 'Nederland'), ('allemagne', 'Duitsland'), ('luxembourg', 'Luxemburg'), ('france', 'Frankrijk')],
    'arabie-saoudite': [('dubai', '\u062f\u0628\u064a'), ('qatar', '\u0642\u0637\u0631'), ('koweit', '\u0627\u0644\u0643\u0648\u064a\u062a'), ('egypte', '\u0645\u0635\u0631')],
    'dubai': [('arabie-saoudite', '\u0627\u0644\u0633\u0639\u0648\u062f\u064a\u0629'), ('qatar', '\u0642\u0637\u0631'), ('koweit', '\u0627\u0644\u0643\u0648\u064a\u062a'), ('egypte', '\u0645\u0635\u0631')],
    'qatar': [('dubai', '\u062f\u0628\u064a'), ('arabie-saoudite', '\u0627\u0644\u0633\u0639\u0648\u062f\u064a\u0629'), ('koweit', '\u0627\u0644\u0643\u0648\u064a\u062a'), ('egypte', '\u0645\u0635\u0631')],
    'koweit': [('dubai', '\u062f\u0628\u064a'), ('arabie-saoudite', '\u0627\u0644\u0633\u0639\u0648\u062f\u064a\u0629'), ('qatar', '\u0642\u0637\u0631'), ('egypte', '\u0645\u0635\u0631')],
    'egypte': [('arabie-saoudite', '\u0627\u0644\u0633\u0639\u0648\u062f\u064a\u0629'), ('dubai', '\u062f\u0628\u064a'), ('turquie', '\u062a\u0631\u0643\u064a\u0627'), ('qatar', '\u0642\u0637\u0631')],
    'italie': [('espagne', 'Spagna'), ('france', 'Francia'), ('allemagne', 'Germania'), ('suisse', 'Svizzera')],
    'suede': [('norvege', 'Norge'), ('danemark', 'Danmark'), ('finlande', 'Finland'), ('allemagne', 'Tyskland')],
    'norvege': [('suede', 'Sverige'), ('danemark', 'Danmark'), ('finlande', 'Finland'), ('royaume-uni', 'Storbritannia')],
    'danemark': [('suede', 'Sverige'), ('norvege', 'Norge'), ('finlande', 'Finland'), ('allemagne', 'Tyskland')],
    'finlande': [('suede', 'Sverige'), ('norvege', 'Norge'), ('danemark', 'Danmark'), ('estonie', 'Viro')],
    'grece': [('italie', '\u0399\u03c4\u03b1\u03bb\u03af\u03b1'), ('turquie', '\u03a4\u03bf\u03c5\u03c1\u03ba\u03af\u03b1'), ('espagne', '\u0399\u03c3\u03c0\u03b1\u03bd\u03af\u03b1'), ('portugal', '\u03a0\u03bf\u03c1\u03c4\u03bf\u03b3\u03b1\u03bb\u03af\u03b1')],
    'pologne': [('tchequie', 'Czechy'), ('allemagne', 'Niemcy'), ('hongrie', 'W\u0119gry'), ('roumanie', 'Rumunia')],
    'tchequie': [('pologne', 'Polsko'), ('allemagne', 'N\u011bmecko'), ('autriche', 'Rakousko'), ('hongrie', 'Ma\u010farsko')],
    'hongrie': [('pologne', 'Lengyelorsz\u00e1g'), ('tchequie', 'Csehorsz\u00e1g'), ('roumanie', 'Rom\u00e1nia'), ('croatie', 'Horv\u00e1torsz\u00e1g')],
    'roumanie': [('hongrie', 'Ungaria'), ('pologne', 'Polonia'), ('croatie', 'Croa\u021bia'), ('grece', 'Grecia')],
    'croatie': [('hongrie', 'Ma\u0111arska'), ('italie', 'Italija'), ('autriche', 'Austrija'), ('roumanie', 'Rumunjska')],
    'turquie': [('grece', 'Yunanistan'), ('egypte', 'M\u0131s\u0131r'), ('roumanie', 'Romanya'), ('allemagne', 'Almanya')],
    'japon': [('coree-du-sud', '\u97d3\u56fd'), ('chine', '\u4e2d\u56fd'), ('singapour', '\u30b7\u30f3\u30ac\u30dd\u30fc\u30eb'), ('australie', '\u30aa\u30fc\u30b9\u30c8\u30e9\u30ea\u30a2')],
    'coree-du-sud': [('japon', '\u65e5\u672c'), ('chine', '\u4e2d\u56fd'), ('singapour', '\u49f1\u52a0\u5761'), ('australie', '\ud638\uc8fc')],
    'chine': [('japon', '\u65e5\u672c'), ('coree-du-sud', '\u97e9\u56fd'), ('singapour', '\u65b0\u52a0\u5761'), ('hong-kong', '\u9999\u6e2f')],
    'thailande': [('malaisie', '\u0e21\u0e32\u0e40\u0e25\u0e40\u0e0b\u0e35\u0e22'), ('indonesie', '\u0e2d\u0e34\u0e19\u0e42\u0e14\u0e19\u0e35\u0e40\u0e0b\u0e35\u0e22'), ('vietnam', '\u0e40\u0e27\u0e35\u0e22\u0e14\u0e19\u0e32\u0e21'), ('philippines', '\u0e1f\u0e34\u0e25\u0e34\u0e1b\u0e1b\u0e34\u0e19\u0e2a\u0e4c')],
    'malaisie': [('indonesie', 'Indonesia'), ('thailande', 'Thailand'), ('singapour', 'Singapura'), ('philippines', 'Filipina')],
    'indonesie': [('malaisie', 'Malaysia'), ('thailande', 'Thailand'), ('philippines', 'Filipina'), ('vietnam', 'Vietnam')],
    'vietnam': [('thailande', 'Th\u00e1i Lan'), ('indonesie', 'Indonesia'), ('malaisie', 'Malaysia'), ('philippines', 'Philippines')],
}

# ============================================================
# MEGA-MENU UI TRANSLATIONS (6 strings per language)
# ============================================================
MENU_UI = {
    'de': {'all_countries': 'Alle Länder', 'europe': 'Europa', 'americas': 'Amerika', 'asia_pacific': 'Asien-Pazifik', 'middle_east_africa': 'Nahost & Afrika', 'compare_all': 'Alle Länder vergleichen'},
    'es': {'all_countries': 'Todos los países', 'europe': 'Europa', 'americas': 'Américas', 'asia_pacific': 'Asia-Pacífico', 'middle_east_africa': 'Oriente Medio y África', 'compare_all': 'Comparar todos los países'},
    'pt': {'all_countries': 'Todos os países', 'europe': 'Europa', 'americas': 'Américas', 'asia_pacific': 'Ásia-Pacífico', 'middle_east_africa': 'Oriente Médio e África', 'compare_all': 'Comparar todos os países'},
    'nl': {'all_countries': 'Alle landen', 'europe': 'Europa', 'americas': "Amerika's", 'asia_pacific': 'Azië-Pacific', 'middle_east_africa': 'Midden-Oosten & Afrika', 'compare_all': 'Alle landen vergelijken'},
    'ar': {'all_countries': 'جميع الدول', 'europe': 'أوروبا', 'americas': 'الأمريكتين', 'asia_pacific': 'آسيا والمحيط الهادئ', 'middle_east_africa': 'الشرق الأوسط وأفريقيا', 'compare_all': 'مقارنة جميع الدول'},
    'it': {'all_countries': 'Tutti i paesi', 'europe': 'Europa', 'americas': 'Americhe', 'asia_pacific': 'Asia-Pacifico', 'middle_east_africa': 'Medio Oriente e Africa', 'compare_all': 'Confronta tutti i paesi'},
    'sv': {'all_countries': 'Alla länder', 'europe': 'Europa', 'americas': 'Amerika', 'asia_pacific': 'Asien-Stillahavsområdet', 'middle_east_africa': 'Mellanöstern & Afrika', 'compare_all': 'Jämför alla länder'},
    'no': {'all_countries': 'Alle land', 'europe': 'Europa', 'americas': 'Amerika', 'asia_pacific': 'Asia-Stillehavet', 'middle_east_africa': 'Midtøsten & Afrika', 'compare_all': 'Sammenlign alle land'},
    'da': {'all_countries': 'Alle lande', 'europe': 'Europa', 'americas': 'Amerika', 'asia_pacific': 'Asien-Stillehavet', 'middle_east_africa': 'Mellemøsten & Afrika', 'compare_all': 'Sammenlign alle lande'},
    'fi': {'all_countries': 'Kaikki maat', 'europe': 'Eurooppa', 'americas': 'Amerikka', 'asia_pacific': 'Aasia-Tyynenmeri', 'middle_east_africa': 'Lähi-itä & Afrikka', 'compare_all': 'Vertaa kaikkia maita'},
    'el': {'all_countries': 'Όλες οι χώρες', 'europe': 'Ευρώπη', 'americas': 'Αμερική', 'asia_pacific': 'Ασία-Ειρηνικός', 'middle_east_africa': 'Μέση Ανατολή & Αφρική', 'compare_all': 'Σύγκριση όλων των χωρών'},
    'pl': {'all_countries': 'Wszystkie kraje', 'europe': 'Europa', 'americas': 'Ameryka', 'asia_pacific': 'Azja-Pacyfik', 'middle_east_africa': 'Bliski Wschód i Afryka', 'compare_all': 'Porównaj wszystkie kraje'},
    'cs': {'all_countries': 'Všechny země', 'europe': 'Evropa', 'americas': 'Amerika', 'asia_pacific': 'Asie-Pacifik', 'middle_east_africa': 'Blízký východ a Afrika', 'compare_all': 'Porovnat všechny země'},
    'hu': {'all_countries': 'Összes ország', 'europe': 'Európa', 'americas': 'Amerika', 'asia_pacific': 'Ázsia-Csendes-óceán', 'middle_east_africa': 'Közel-Kelet és Afrika', 'compare_all': 'Összes ország összehasonlítása'},
    'ro': {'all_countries': 'Toate țările', 'europe': 'Europa', 'americas': 'Americi', 'asia_pacific': 'Asia-Pacific', 'middle_east_africa': 'Orientul Mijlociu și Africa', 'compare_all': 'Comparați toate țările'},
    'hr': {'all_countries': 'Sve zemlje', 'europe': 'Europa', 'americas': 'Amerika', 'asia_pacific': 'Azija-Pacifik', 'middle_east_africa': 'Bliski istok i Afrika', 'compare_all': 'Usporedite sve zemlje'},
    'tr': {'all_countries': 'Tüm ülkeler', 'europe': 'Avrupa', 'americas': 'Amerika', 'asia_pacific': 'Asya-Pasifik', 'middle_east_africa': 'Orta Doğu ve Afrika', 'compare_all': 'Tüm ülkeleri karşılaştırın'},
    'ja': {'all_countries': 'すべての国', 'europe': 'ヨーロッパ', 'americas': 'アメリカ', 'asia_pacific': 'アジア太平洋', 'middle_east_africa': '中東・アフリカ', 'compare_all': 'すべての国を比較'},
    'ko': {'all_countries': '모든 국가', 'europe': '유럽', 'americas': '아메리카', 'asia_pacific': '아시아 태평양', 'middle_east_africa': '중동 및 아프리카', 'compare_all': '모든 국가 비교'},
    'zh': {'all_countries': '所有国家', 'europe': '欧洲', 'americas': '美洲', 'asia_pacific': '亚太地区', 'middle_east_africa': '中东和非洲', 'compare_all': '比较所有国家'},
    'th': {'all_countries': 'ทุกประเทศ', 'europe': 'ยุโรป', 'americas': 'อเมริกา', 'asia_pacific': 'เอเชียแปซิฟิก', 'middle_east_africa': 'ตะวันออกกลางและแอฟริกา', 'compare_all': 'เปรียบเทียบทุกประเทศ'},
    'ms': {'all_countries': 'Semua negara', 'europe': 'Eropah', 'americas': 'Amerika', 'asia_pacific': 'Asia-Pasifik', 'middle_east_africa': 'Timur Tengah & Afrika', 'compare_all': 'Bandingkan semua negara'},
    'id': {'all_countries': 'Semua negara', 'europe': 'Eropa', 'americas': 'Amerika', 'asia_pacific': 'Asia-Pasifik', 'middle_east_africa': 'Timur Tengah & Afrika', 'compare_all': 'Bandingkan semua negara'},
    'vi': {'all_countries': 'Tất cả quốc gia', 'europe': 'Châu Âu', 'americas': 'Châu Mỹ', 'asia_pacific': 'Châu Á - Thái Bình Dương', 'middle_east_africa': 'Trung Đông & Châu Phi', 'compare_all': 'So sánh tất cả quốc gia'},
}

# ============================================================
# MEGA-MENU COUNTRIES BY REGION
# Each entry: (flag_emoji, en_name, en_slug, fr_slug, native_lang_or_none, native_country_slug, native_page_slug)
# native_lang_or_none is set if this country has a native page
# ============================================================
# Build a lookup from COUNTRIES for quick access
_NATIVE_LOOKUP = {}
for _c in COUNTRIES:
    _NATIVE_LOOKUP[_c[2]] = (_c[0], _c[3], _c[4])  # en_slug -> (lang, native_country_slug, native_page_slug)

MEGA_MENU_REGIONS = [
    ('europe', [
        ('<iconify-icon icon="circle-flags:fr" width="16"></iconify-icon>', 'France', 'france', 'france'),
        ('<iconify-icon icon="circle-flags:es" width="16"></iconify-icon>', 'Spain', 'spain', 'espagne'),
        ('<iconify-icon icon="circle-flags:gb" width="16"></iconify-icon>', 'United Kingdom', 'uk', 'royaume-uni'),
        ('<iconify-icon icon="circle-flags:de" width="16"></iconify-icon>', 'Germany', 'germany', 'allemagne'),
        ('<iconify-icon icon="circle-flags:it" width="16"></iconify-icon>', 'Italy', 'italy', 'italie'),
        ('<iconify-icon icon="circle-flags:nl" width="16"></iconify-icon>', 'Netherlands', 'netherlands', 'pays-bas'),
        ('🇨🇭', 'Switzerland', 'switzerland', 'suisse'),
        ('<iconify-icon icon="circle-flags:pt" width="16"></iconify-icon>', 'Portugal', 'portugal', 'portugal'),
        ('<iconify-icon icon="circle-flags:be" width="16"></iconify-icon>', 'Belgium', 'belgium', 'belgique'),
        ('<iconify-icon icon="circle-flags:lu" width="16"></iconify-icon>', 'Luxembourg', 'luxembourg', 'luxembourg'),
        ('🇦🇹', 'Austria', 'austria', 'autriche'),
        ('<iconify-icon icon="circle-flags:ie" width="16"></iconify-icon>', 'Ireland', 'ireland', 'irlande'),
        ('🇸🇪', 'Sweden', 'sweden', 'suede'),
        ('🇳🇴', 'Norway', 'norway', 'norvege'),
        ('<iconify-icon icon="circle-flags:dk" width="16"></iconify-icon>', 'Denmark', 'denmark', 'danemark'),
        ('🇫🇮', 'Finland', 'finland', 'finlande'),
        ('<iconify-icon icon="circle-flags:gr" width="16"></iconify-icon>', 'Greece', 'greece', 'grece'),
        ('🇵🇱', 'Poland', 'poland', 'pologne'),
        ('<iconify-icon icon="circle-flags:cz" width="16"></iconify-icon>', 'Czech Republic', 'czech-republic', 'tchequie'),
        ('🇭🇺', 'Hungary', 'hungary', 'hongrie'),
        ('🇷🇴', 'Romania', 'romania', 'roumanie'),
        ('🇭🇷', 'Croatia', 'croatia', 'croatie'),
        ('🇹🇷', 'Turkey', 'turkey', 'turquie'),
    ]),
    ('americas', [
        ('<iconify-icon icon="circle-flags:us" width="16"></iconify-icon>', 'USA', 'usa', 'usa'),
        ('🇨🇦', 'Canada', 'canada', 'canada'),
        ('🇧🇷', 'Brazil', 'brazil', 'bresil'),
        ('<iconify-icon icon="circle-flags:mx" width="16"></iconify-icon>', 'Mexico', 'mexico', 'mexique'),
        ('🇦🇷', 'Argentina', 'argentina', 'argentine'),
        ('🇨🇱', 'Chile', 'chile', 'chili'),
        ('🇨🇴', 'Colombia', 'colombia', 'colombie'),
        ('🇵🇪', 'Peru', 'peru', 'perou'),
    ]),
    ('asia_pacific', [
        ('🇯🇵', 'Japan', 'japan', 'japon'),
        ('<iconify-icon icon="circle-flags:kr" width="16"></iconify-icon>', 'South Korea', 'south-korea', 'coree-du-sud'),
        ('<iconify-icon icon="circle-flags:cn" width="16"></iconify-icon>', 'China', 'china', 'chine'),
        ('🇸🇬', 'Singapore', 'singapore', 'singapour'),
        ('🇦🇺', 'Australia', 'australia', 'australie'),
        ('🇭🇰', 'Hong Kong', 'hong-kong', 'hong-kong'),
        ('🇮🇳', 'India', 'india', 'inde'),
        ('🇳🇿', 'New Zealand', 'new-zealand', 'nouvelle-zelande'),
        ('🇮🇩', 'Indonesia', 'indonesia', 'indonesie'),
        ('🇲🇾', 'Malaysia', 'malaysia', 'malaisie'),
        ('<iconify-icon icon="circle-flags:th" width="16"></iconify-icon>', 'Thailand', 'thailand', 'thailande'),
        ('🇵🇰', 'Pakistan', 'pakistan', 'pakistan'),
        ('🇵🇭', 'Philippines', 'philippines', 'philippines'),
        ('🇻🇳', 'Vietnam', 'vietnam', 'vietnam'),
    ]),
    ('middle_east_africa', [
        ('<iconify-icon icon="circle-flags:ma" width="16"></iconify-icon>', 'Morocco', 'morocco', 'maroc'),
        ('🇦🇪', 'UAE', 'dubai', 'dubai'),
        ('🇸🇦', 'Saudi Arabia', 'saudi-arabia', 'arabie-saoudite'),
        ('🇶🇦', 'Qatar', 'qatar', 'qatar'),
        ('🇰🇼', 'Kuwait', 'kuwait', 'koweit'),
        ('🇪🇬', 'Egypt', 'egypt', 'egypte'),
        ('🇿🇦', 'South Africa', 'south-africa', 'afrique-du-sud'),
    ]),
]


def _get_country_link(en_slug, current_lang):
    """Get the best URL for a country in the mega-menu.

    Logic:
    - If the country has a native page in current_lang -> use native URL
    - Otherwise -> use EN URL (universally understood)
    """
    native = _NATIVE_LOOKUP.get(en_slug)
    if native and native[0] == current_lang:
        # Same language as the native page -> use native URL
        lang_code, native_slug, native_page = native
        return f'/{lang_code}/{native_slug}/{native_page}/'
    # Fallback to EN
    return f'/en/{en_slug}/income-tax/'


def _get_country_display_name(en_name, en_slug, current_lang):
    """Get display name for a country in the mega-menu.

    Logic:
    - If the country has a native page in current_lang -> use native name
    - Otherwise -> use English name (universally recognizable)
    """
    native = _NATIVE_LOOKUP.get(en_slug)
    if native and native[0] == current_lang:
        # Find native country name from COUNTRIES
        for c in COUNTRIES:
            if c[2] == en_slug and c[0] == current_lang:
                return c[5]  # country_name_native
    return en_name


def build_mega_menu_desktop(lang):
    """Build the desktop mega-menu HTML for native pages."""
    menu_ui = MENU_UI[lang]
    html = ''

    for region_key, countries in MEGA_MENU_REGIONS:
        region_name = menu_ui[region_key]
        html += f'<div class="text-xs font-semibold text-slate-400 uppercase tracking-wider mega-country-title">{region_name}</div>\n'
        html += '<div class="grid grid-cols-2 mega-country-grid" style="column-gap: 2rem; row-gap: 0.25rem;">\n'
        for flag_emoji, en_name, en_slug, fr_slug in countries:
            url = _get_country_link(en_slug, lang)
            display = _get_country_display_name(en_name, en_slug, lang)
            html += f'                                <a href="{url}" class="flex items-center gap-2 px-2 py-1.5 text-sm text-slate-600 hover:bg-slate-50 hover:text-slate-900 rounded-md transition-colors"><span>{flag_emoji}</span> {display}</a>\n'
        html += '                            </div>\n'

    return html


def build_mega_menu_mobile(lang):
    """Build the mobile mega-menu HTML for native pages."""
    menu_ui = MENU_UI[lang]
    html = ''

    for region_key, countries in MEGA_MENU_REGIONS:
        region_name = menu_ui[region_key]
        html += f'                        <div>\n'
        html += f'                            <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">{region_name}</div>\n'
        html += f'                            <div class="grid grid-cols-2 gap-1 mega-country-grid">\n'
        for flag_emoji, en_name, en_slug, fr_slug in countries:
            url = _get_country_link(en_slug, lang)
            display = _get_country_display_name(en_name, en_slug, lang)
            html += f'                                <a href="{url}" class="text-sm text-slate-600 hover:text-slate-900 py-1">{flag_emoji} {display}</a>\n'
        html += f'                            </div>\n'
        html += f'                        </div>\n'

    return html


# ============================================================
# EXTRACTION FUNCTIONS
# ============================================================

def extract_script_block(html_content):
    """Extract the main calculator <script> block from FR page."""
    # Find the last <script> block (the calculator one, not GA or JSON-LD)
    pattern = r'<script>\s*(?://[^\n]*\n\s*)?(?:const BRACKETS|// .* tax|function )'
    matches = list(re.finditer(pattern, html_content))
    if not matches:
        # Try broader pattern
        all_scripts = re.findall(r'<script>(.*?)</script>', html_content, re.DOTALL)
        for script in all_scripts:
            if 'BRACKETS' in script or 'calculate()' in script or 'IS_TAX_FREE' in script:
                return script.strip()
        return None

    # Get the full script from the last match
    last_match = matches[-1]
    start = last_match.start()
    # Find the opening <script> tag before this
    script_start = html_content.rfind('<script>', 0, start + 10)
    script_end = html_content.find('</script>', start)
    if script_start >= 0 and script_end >= 0:
        return html_content[script_start + len('<script>'):script_end].strip()
    return None


def extract_brackets_section(html_content):
    """Extract the tax brackets display section from FR page."""
    pattern = r'(<div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 md:p-8">\s*<h2 class="text-lg font-semibold.*?Baremes.*?</div>\s*</div>)'
    match = re.search(pattern, html_content, re.DOTALL)
    if match:
        return match.group(1)
    return None


def extract_guide_section(html_content):
    """Extract the fiscal guide section from FR page."""
    # Find the guide section - it's the div after brackets with prose content
    pattern = r'(<!-- Comprendre.*?</div>\s*</div>)'
    match = re.search(pattern, html_content, re.DOTALL)
    if match:
        return match.group(1)
    # Alternative: find the guide by its structure
    pattern2 = r'(<div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 md:p-8 mt-6">\s*<h2 class="text-xl font-bold.*?Guide.*?)(<!-- Comparer avec|<div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 md:p-8 mt-6">\s*<h3)'
    match2 = re.search(pattern2, html_content, re.DOTALL)
    if match2:
        guide = match2.group(1).rstrip()
        # Close any unclosed divs
        open_divs = guide.count('<div') - guide.count('</div')
        guide += '</div>' * max(0, open_divs)
        return guide
    return None


def extract_comparisons_section(html_content):
    """Extract the comparison links section from FR page."""
    pattern = r'(<!-- Comparer avec des pays similaires -->.*?</div>\s*</div>\s*</div>)'
    match = re.search(pattern, html_content, re.DOTALL)
    if match:
        return match.group(1)
    # Alternative pattern
    pattern2 = r'(<div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 md:p-8 mt-6">\s*<h3 class="text-lg font-semibold.*?Comparer avec.*?</div>\s*</div>\s*</div>)'
    match2 = re.search(pattern2, html_content, re.DOTALL)
    if match2:
        return match2.group(1)
    return None


def adapt_script_locale(script_content, lang):
    """Replace toLocaleString locale in calculator script."""
    locale = LOCALE_MAP.get(lang, 'en-US')
    # Replace existing toLocaleString calls with new locale
    adapted = re.sub(
        r"toLocaleString\(['\"][a-z]{2}-[A-Z]{2}['\"]\)",
        f"toLocaleString('{locale}')",
        script_content
    )
    # Also replace bare toLocaleString() calls
    adapted = re.sub(
        r"\.toLocaleString\(\)",
        f".toLocaleString('{locale}')",
        adapted
    )
    return adapted


# ============================================================
# HTML GENERATION FUNCTIONS
# ============================================================

def build_head(lang, country_name, country_slug_native, page_slug, fr_slug, en_slug, currency, text_dir, flag_icon):
    """Build the <head> section."""
    ui = UI[lang]
    title = ui['title'].format(country=country_name)
    desc = ui['meta_desc'].format(country=country_name)
    native_url = f'{SITE_URL}/{lang}/{country_slug_native}/{page_slug}/'
    fr_url = f'{SITE_URL}/fr/{fr_slug}/simulateur-impot/'
    en_url = f'{SITE_URL}/en/{en_slug}/income-tax/'

    dir_attr = f' dir="rtl"' if text_dir == 'rtl' else ''

    # Font links
    font_links = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">'
    if lang in SPECIAL_FONTS:
        font_links += f'\n    <link href="https://fonts.googleapis.com/css2?family={SPECIAL_FONTS[lang]}&display=swap" rel="stylesheet">'

    font_family_style = ''
    if lang in FONT_FAMILIES:
        font_family_style = f' style="font-family: {FONT_FAMILIES[lang]}"'

    rtl_css = ''
    if text_dir == 'rtl':
        rtl_css = """
    <style>
        .rtl-flip { direction: rtl; }
        input[type="number"] { direction: ltr; text-align: right; }
        .flex { direction: rtl; }
        .grid { direction: rtl; }
    </style>"""

    return f'''<!DOCTYPE html>
<html lang="{lang}" class="scroll-smooth"{dir_attr}>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        function loadGA() {{
            if (window.gaLoaded) return;
            window.gaLoaded = true;
            var script = document.createElement('script');
            script.src = 'https://www.googletagmanager.com/gtag/js?id=G-Z328SB8DZ8';
            script.async = true;
            document.head.appendChild(script);
            gtag('js', new Date());
            gtag('config', 'G-Z328SB8DZ8');
        }}
        ['scroll', 'click', 'touchstart', 'keydown'].forEach(function(evt) {{
            window.addEventListener(evt, loadGA, {{once: true, passive: true}});
        }});
        setTimeout(loadGA, 3000);
    </script>

    <title>{title}</title>
    <meta name="description" content="{desc}">

    <link rel="canonical" href="{native_url}">
    <link rel="alternate" hreflang="{lang}" href="{native_url}">
    <link rel="alternate" hreflang="fr" href="{fr_url}">
    <link rel="alternate" hreflang="en" href="{en_url}">
    <link rel="alternate" hreflang="x-default" href="{en_url}">

    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{native_url}">
    <meta property="og:site_name" content="NetSalaire">

    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "{title}",
        "url": "{native_url}",
        "inLanguage": "{lang}",
        "applicationCategory": "FinanceApplication",
        "operatingSystem": "Web",
        "offers": {{ "@type": "Offer", "price": "0", "priceCurrency": "{currency}" }}
    }}
    </script>

    <link rel="icon" type="image/png" sizes="48x48" href="/assets/images/favicon-48.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    {font_links}
    <link href="/assets/css/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="/assets/css/style.css">
    <script src="https://code.iconify.design/3/3.1.0/iconify.min.js"></script>
    <script defer src="https://code.iconify.design/iconify-icon/2.3.0/iconify-icon.min.js"></script>

    <style>
        input[type="range"] {{
            -webkit-appearance: none;
            appearance: none;
            background: #e2e8f0;
            border-radius: 8px;
            height: 8px;
        }}
        input[type="range"]::-webkit-slider-thumb {{
            -webkit-appearance: none;
            appearance: none;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: #4f46e5;
            cursor: pointer;
            border: 3px solid white;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        }}
        input[type="range"]::-moz-range-thumb {{
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: #4f46e5;
            cursor: pointer;
            border: 3px solid white;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        }}
        .result-card {{ transition: all 0.3s ease; }}
        .result-card:hover {{ transform: translateY(-2px); box-shadow: 0 8px 25px -5px rgba(0,0,0,0.1); }}
    </style>{rtl_css}
</head>'''


def build_navbar(lang, country_name, flag, fr_slug, en_slug, country_slug_native, page_slug, flag_icon):
    """Build full navbar with mega-menu and language switcher."""
    ui = UI[lang]
    menu_ui = MENU_UI[lang]
    fr_url = f'/fr/{fr_slug}/simulateur-impot/'
    en_url = f'/en/{en_slug}/income-tax/'
    native_url = f'/{lang}/{country_slug_native}/{page_slug}/'
    text_dir = 'rtl' if lang == 'ar' else 'ltr'

    # Build mega-menu content
    mega_desktop = build_mega_menu_desktop(lang)
    mega_mobile = build_mega_menu_mobile(lang)

    # Compare all link
    compare_url = '/en/global-comparison/'
    compare_text = menu_ui['compare_all']

    return f'''
<body class="bg-slate-50 font-sans antialiased">

    <!-- Navbar -->
    <nav class="fixed top-0 w-full z-50 border-b border-slate-200 bg-white/80 backdrop-blur-md">
        <div class="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
            <a href="/en/" class="flex items-center gap-2 group">
                <div class="w-8 h-8 bg-slate-900 rounded flex items-center justify-center text-white font-semibold tracking-tighter shadow-md group-hover:bg-indigo-600 transition-colors duration-300">
                    N.
                </div>
                <span class="font-semibold tracking-tight text-slate-900">NetSalaire</span>
            </a>
            <!-- Desktop Menu -->
            <div class="hidden md:flex items-center gap-8 text-sm font-medium text-slate-600">
                <!-- Mega-menu All Countries -->
                <div class="relative group">
                    <button class="hover:text-slate-900 transition-colors flex items-center gap-1.5 py-2 text-sm font-medium text-slate-600">
                        <iconify-icon icon="lucide:globe" width="16"></iconify-icon> {menu_ui['all_countries']}
                        <iconify-icon icon="lucide:chevron-down" width="14" class="text-slate-400 group-hover:text-slate-600 transition-transform group-hover:rotate-180"></iconify-icon>
                    </button>
                    <div class="absolute top-full {"left" if text_dir == "rtl" else "right"}-0 pt-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
                        <div class="bg-white border border-slate-200 rounded-xl shadow-xl mega-country-container" style="width: 600px; max-height: 75vh; overflow-y: auto;">
                            {mega_desktop}
                            <div class="border-t border-slate-100 pt-3">
                                <a href="{compare_url}" class="flex items-center gap-2 text-sm font-medium text-indigo-600 hover:text-indigo-700 transition-colors">
                                    <iconify-icon icon="lucide:bar-chart-3" width="16"></iconify-icon> {compare_text} →
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
                <a href="/en/faq/" class="hover:text-slate-900 transition-colors">FAQ</a>
            </div>
            <div class="flex items-center gap-3">
                <!-- Language Switcher -->
                <div class="relative">
                    <button onclick="document.getElementById('lang-dropdown-page').classList.toggle('hidden')" class="flex items-center gap-1.5 px-2.5 py-1.5 text-xs font-medium text-slate-600 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 border border-slate-200 rounded-full transition-all" title="Language">
                        <span class="lang-flag">{ui['lang_flag']}</span>
                        <iconify-icon icon="lucide:chevron-down" width="14"></iconify-icon>
                    </button>
                    <div id="lang-dropdown-page" class="hidden absolute top-full right-0 mt-2 bg-white border border-slate-200 rounded-lg shadow-lg min-w-[160px] py-1 z-50">
                        <a href="{native_url}" class="w-full flex items-center gap-2 px-3 py-2 text-sm text-slate-700 bg-slate-50 transition-colors">
                            <span>{ui['lang_flag']}</span> {ui['lang_native']}
                        </a>
                        <a href="{fr_url}" class="w-full flex items-center gap-2 px-3 py-2 text-sm text-slate-700 hover:bg-slate-50 transition-colors">
                            <iconify-icon icon="circle-flags:fr" width="16"></iconify-icon> Français
                        </a>
                        <a href="{en_url}" class="w-full flex items-center gap-2 px-3 py-2 text-sm text-slate-700 hover:bg-slate-50 transition-colors">
                            <iconify-icon icon="circle-flags:gb" width="16"></iconify-icon> English
                        </a>
                    </div>
                </div>
                <!-- Mobile Menu Button -->
                <button onclick="document.getElementById('mobile-menu').classList.toggle('hidden')" class="md:hidden p-2 text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-lg transition-colors">
                    <iconify-icon icon="lucide:menu" width="24"></iconify-icon>
                </button>
            </div>
        </div>
        <!-- Mobile Menu (Accordions) -->
        <div id="mobile-menu" class="hidden md:hidden bg-white border-t border-slate-200">
            <div class="px-6 py-4 space-y-1">
                <!-- All Countries Accordion -->
                <div>
                    <button onclick="this.nextElementSibling.classList.toggle('hidden'); this.querySelector('.chevron-icon').classList.toggle('rotate-180')" class="w-full flex items-center justify-between py-3 text-sm font-semibold text-slate-900">
                        <span class="flex items-center gap-2">
                            <iconify-icon icon="lucide:globe" width="18"></iconify-icon> {menu_ui['all_countries']}
                        </span>
                        <iconify-icon icon="lucide:chevron-down" width="16" class="chevron-icon text-slate-400 transition-transform duration-200"></iconify-icon>
                    </button>
                    <div class="hidden pl-4 pb-3 space-y-3">
{mega_mobile}
                        <div class="border-t border-slate-100 pt-2">
                            <a href="{compare_url}" class="flex items-center gap-2 text-sm font-medium text-indigo-600">
                                {compare_text} →
                            </a>
                        </div>
                    </div>
                </div>
                <!-- FAQ -->
                <div class="border-t border-slate-100">
                    <a href="/en/faq/" class="flex items-center gap-2 py-3 text-sm font-semibold text-slate-900">
                        <iconify-icon icon="lucide:help-circle" width="18"></iconify-icon> FAQ
                    </a>
                </div>
                <!-- Mobile Language Links -->
                <div class="border-t border-slate-100 pt-3 pb-2 flex flex-wrap gap-2">
                    <a href="{native_url}" class="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium bg-slate-100 border border-slate-200 rounded-full text-slate-700">
                        <span>{ui['lang_flag']}</span> {ui['lang_native']}
                    </a>
                    <a href="{fr_url}" class="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium hover:bg-slate-50 border border-slate-200 rounded-full text-slate-600">
                        <iconify-icon icon="circle-flags:fr" width="16"></iconify-icon> Français
                    </a>
                    <a href="{en_url}" class="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium hover:bg-slate-50 border border-slate-200 rounded-full text-slate-600">
                        <iconify-icon icon="circle-flags:gb" width="16"></iconify-icon> English
                    </a>
                </div>
            </div>
        </div>
    </nav>'''


def build_hero(lang, country_name, flag):
    """Build the hero/header section."""
    ui = UI[lang]
    h1 = ui['h1'].format(country=country_name)
    subtitle = ui['subtitle'].format(country=country_name)

    return f'''
    <main class="pt-24 pb-16 px-4">
        <div class="max-w-4xl mx-auto">

            <div class="text-center mb-10">
                <div class="inline-flex items-center gap-2 rounded-full bg-yellow-50 border border-yellow-300 px-4 py-1.5 mb-4">
                    <span class="text-2xl">{flag}</span>
                    <span class="text-sm font-medium text-yellow-800">{country_name}</span>
                </div>
                <h1 class="text-3xl md:text-4xl font-bold text-slate-900 mb-3">
                    {h1} <span class="text-indigo-600">{ui['h1_year']}</span>
                </h1>
                <p class="text-slate-500 max-w-xl mx-auto">{subtitle}</p>
            </div>'''


def build_calculator_form(lang, currency):
    """Build the calculator form with translated labels."""
    ui = UI[lang]

    return f'''
            <div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 md:p-8 mb-6">
                <div class="mb-8">
                    <div class="grid grid-cols-2 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-2">{ui['monthly_income']}</label>
                            <div class="relative">
                                <input type="number" id="income-monthly" value="5000" min="0" max="10000000"
                                       class="w-full text-right rounded-lg border-0 py-3 pl-3 pr-14 text-slate-900 ring-1 ring-slate-200 focus:ring-2 focus:ring-indigo-500 text-lg font-semibold">
                                <span class="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 text-sm">{currency}</span>
                            </div>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-2">{ui['annual_income']}</label>
                            <div class="relative">
                                <input type="number" id="income-annual" value="60000" min="0" max="10000000"
                                       class="w-full text-right rounded-lg border-0 py-3 pl-3 pr-14 text-slate-900 ring-1 ring-slate-200 focus:ring-2 focus:ring-indigo-500 text-lg font-semibold">
                                <span class="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 text-sm">{currency}</span>
                            </div>
                        </div>
                    </div>
                    <input type="range" id="income-slider" min="0" max="300000" step="1000" value="60000"
                           class="w-full h-3 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-indigo-600 touch-pan-x"
                           style="-webkit-appearance: none; padding: 8px 0;">
                    <p class="text-xs text-slate-400 mt-2 text-right"><span id="conv-gross-usd">~$0</span></p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                    <div class="result-card bg-gradient-to-br from-indigo-50 to-white rounded-xl border border-indigo-100 p-5">
                        <div class="flex items-center gap-2 mb-3">
                            <div class="w-8 h-8 bg-indigo-100 rounded-lg flex items-center justify-center">
                                <iconify-icon icon="lucide:landmark" class="text-indigo-600" width="18"></iconify-icon>
                            </div>
                            <span class="text-sm font-medium text-slate-700">{ui['income_tax']}</span>
                        </div>
                        <p class="text-2xl font-bold text-indigo-600" id="income-tax">0 {currency}</p>
                        <p class="text-xs text-slate-500 mt-1">{ui['effective_rate']}: <span id="tax-rate">0%</span></p>
                    </div>
                    <div class="result-card bg-gradient-to-br from-amber-50 to-white rounded-xl border border-amber-100 p-5">
                        <div class="flex items-center gap-2 mb-3">
                            <div class="w-8 h-8 bg-amber-100 rounded-lg flex items-center justify-center">
                                <iconify-icon icon="lucide:shield" class="text-amber-600" width="18"></iconify-icon>
                            </div>
                            <span class="text-sm font-medium text-slate-700">{ui['social_contributions']}</span>
                        </div>
                        <p class="text-2xl font-bold text-amber-600" id="social-tax">0 {currency}</p>
                        <p class="text-xs text-slate-500 mt-1">{ui['employee_share']}</p>
                    </div>
                    <div class="result-card bg-gradient-to-br from-emerald-50 to-white rounded-xl border border-emerald-200 p-5">
                        <div class="flex items-center gap-2 mb-3">
                            <div class="w-8 h-8 bg-emerald-100 rounded-lg flex items-center justify-center">
                                <iconify-icon icon="lucide:wallet" class="text-emerald-600" width="18"></iconify-icon>
                            </div>
                            <span class="text-sm font-medium text-slate-700">{ui['net_annual']}</span>
                        </div>
                        <p class="text-2xl font-bold text-emerald-600" id="net-income">0 {currency}</p>
                        <p class="text-xs text-slate-500 mt-1">{ui['net_monthly']}: <span id="net-monthly" class="font-medium">0 {currency}</span></p>
                    </div>
                </div>

                <div class="rounded-xl border border-slate-200 bg-gradient-to-br from-slate-50 to-white p-5">
                    <h3 class="text-sm font-semibold text-slate-900 mb-4">{ui['income_breakdown']}</h3>
                    <div class="flex items-center gap-6">
                        <div class="relative h-28 w-28 flex-shrink-0">
                            <div id="chart-donut" class="absolute inset-0 rounded-full transition-all duration-500" style="background: conic-gradient(#10b981 0% 60%, #6366f1 60% 80%, #f59e0b 80% 100%);"></div>
                            <div class="absolute inset-3 rounded-full bg-white flex items-center justify-center flex-col shadow-inner">
                                <span class="text-xs text-slate-400">{ui['net']}</span>
                                <span id="chart-percent" class="text-lg font-bold text-emerald-600">0%</span>
                            </div>
                        </div>
                        <div class="flex-grow space-y-3">
                            <div class="flex justify-between items-center">
                                <div class="flex items-center gap-2">
                                    <span class="h-3 w-3 rounded-full bg-emerald-500"></span>
                                    <span class="text-sm text-slate-600">{ui['net_label']}</span>
                                </div>
                                <span class="text-sm font-semibold text-slate-900" id="legend-net">0%</span>
                            </div>
                            <div class="flex justify-between items-center">
                                <div class="flex items-center gap-2">
                                    <span class="h-3 w-3 rounded-full bg-indigo-500"></span>
                                    <span class="text-sm text-slate-600">{ui['tax_label']}</span>
                                </div>
                                <span class="text-sm font-medium text-slate-500" id="legend-tax">0%</span>
                            </div>
                            <div class="flex justify-between items-center">
                                <div class="flex items-center gap-2">
                                    <span class="h-3 w-3 rounded-full bg-amber-500"></span>
                                    <span class="text-sm text-slate-600">{ui['social_label']}</span>
                                </div>
                                <span class="text-sm font-medium text-slate-500" id="legend-social">0%</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="bg-slate-50 rounded-xl p-4 mt-4">
                    <div class="flex justify-between items-center mb-2">
                        <span class="text-sm font-medium text-slate-600">{ui['total_tax_burden']}</span>
                        <span class="text-lg font-bold text-slate-900" id="total-tax">0 {currency}</span>
                    </div>
                    <div class="h-3 bg-slate-200 rounded-full overflow-hidden">
                        <div class="h-full bg-gradient-to-r from-indigo-500 to-amber-500 rounded-full transition-all duration-300" id="tax-bar" style="width: 0%"></div>
                    </div>
                    <p class="text-xs text-slate-500 mt-2 text-right">{ui['total_effective_rate']}: <span id="total-rate" class="font-medium">0%</span></p>
                </div>
            </div>'''


def build_brackets_section(lang, country_name, brackets_html):
    """Build tax brackets section with translated title."""
    ui = UI[lang]
    title = ui['tax_brackets'].format(country=country_name)

    if not brackets_html:
        return ''

    # Replace French title with translated one
    result = re.sub(
        r'Baremes\s+\w+\s+2026',
        title,
        brackets_html
    )
    return '\n\n            ' + result


def build_guide_section(guide_html):
    """Include the guide section as-is from FR (content stays in French for now, main value is the calculator)."""
    if not guide_html:
        return ''
    return '\n\n            ' + guide_html


def build_comparisons(lang, fr_slug, country_slug_native, page_slug):
    """Build comparison section with native-language links."""
    ui = UI[lang]
    comps = COMPARISONS.get(fr_slug, [])
    if not comps:
        return ''

    links = ''
    for comp_fr_slug, comp_name in comps:
        links += f'''
                    <a href="/fr/{comp_fr_slug}/simulateur-impot/" class="flex items-center gap-2 p-3 bg-white rounded-lg border border-slate-200 hover:border-indigo-300 hover:bg-indigo-50 transition-colors text-sm font-medium text-slate-700 hover:text-indigo-700">
                        <iconify-icon icon="lucide:calculator" width="16" class="text-indigo-500"></iconify-icon>
                        {ui['simulator_link']} {comp_name}
                    </a>'''

    return f'''

            <div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 md:p-8 mt-6">
                <h3 class="text-lg font-semibold text-slate-900 mb-3 flex items-center gap-2">
                    <iconify-icon icon="lucide:git-compare" width="20" class="text-indigo-500"></iconify-icon>
                    {ui['compare_title']}
                </h3>
                <div class="grid grid-cols-2 gap-3">{links}
                </div>
            </div>'''


def build_compare_button(lang):
    """Build the 'compare with other countries' button."""
    ui = UI[lang]
    return f'''

            <div class="mt-8 text-center">
                <a href="/en/global-comparison/" class="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-full font-medium transition-colors">
                    <iconify-icon icon="lucide:globe" width="18"></iconify-icon>
                    {ui['compare_btn']}
                </a>
            </div>'''


def build_footer(lang):
    """Build the footer section with links to EN pages (universal)."""
    ui = UI[lang]
    return f'''
        </div>
    </main>

    <footer class="bg-slate-900 text-slate-400 py-8 px-4">
        <div class="max-w-4xl mx-auto text-center text-sm">
            <p>{ui['footer_copy']}</p>
            <div class="flex justify-center gap-4 mt-4">
                <a href="/en/faq/" class="hover:text-white transition-colors">{ui['faq']}</a>
                <a href="/en/legal/" class="hover:text-white transition-colors">{ui['legal']}</a>
                <a href="/en/privacy/" class="hover:text-white transition-colors">{ui['privacy']}</a>
            </div>
        </div>
    </footer>'''


# ============================================================
# MAIN GENERATOR
# ============================================================

def generate_page(country_tuple):
    """Generate a single native-language page."""
    lang, fr_slug, en_slug, country_slug_native, page_slug, country_name, flag, currency, flag_icon, text_dir = country_tuple

    # Read FR source page
    fr_path = os.path.join(BASE_DIR, 'fr', fr_slug, 'simulateur-impot', 'index.html')
    if not os.path.exists(fr_path):
        # Try alternative path for France/Morocco
        fr_path = os.path.join(BASE_DIR, 'fr', fr_slug, 'simulateur-impot-revenu', 'index.html')
    if not os.path.exists(fr_path):
        print(f"  SKIP (FR source not found): {fr_slug}")
        return False

    with open(fr_path, 'r', encoding='utf-8') as f:
        fr_html = f.read()

    # Extract calculator JS
    script_content = extract_script_block(fr_html)
    if not script_content:
        print(f"  SKIP (no script found): {fr_slug}")
        return False

    # Adapt locale
    script_content = adapt_script_locale(script_content, lang)

    # Extract brackets section
    brackets_html = extract_brackets_section(fr_html)

    # Extract guide section
    guide_html = extract_guide_section(fr_html)

    # Get social rate from script for employee_share label
    social_rate_match = re.search(r'SOCIAL_RATE\s*=\s*([\d.]+)', script_content)
    social_rate_pct = '20'
    if social_rate_match:
        social_rate_pct = str(round(float(social_rate_match.group(1)) * 100, 1))

    # Format the employee_share string
    ui = UI[lang]
    ui['employee_share'] = ui['employee_share'].format(rate=social_rate_pct)

    # Build page
    html_parts = []
    html_parts.append(build_head(lang, country_name, country_slug_native, page_slug, fr_slug, en_slug, currency, text_dir, flag_icon))
    html_parts.append(build_navbar(lang, country_name, flag, fr_slug, en_slug, country_slug_native, page_slug, flag_icon))
    html_parts.append(build_hero(lang, country_name, flag))
    html_parts.append(build_calculator_form(lang, currency))
    html_parts.append(build_brackets_section(lang, country_name, brackets_html))
    html_parts.append(build_guide_section(guide_html))
    html_parts.append(build_comparisons(lang, fr_slug, country_slug_native, page_slug))
    html_parts.append(build_compare_button(lang))
    html_parts.append(build_footer(lang))
    html_parts.append(f'''

    <script>
        {script_content}
    </script>
</body>
</html>
''')

    full_html = ''.join(html_parts)

    # Write output file
    out_dir = os.path.join(BASE_DIR, lang, country_slug_native, page_slug)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'index.html')

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    return True


def update_hreflang_tags():
    """Add hreflang tags to existing FR and EN pages pointing to native versions."""
    print("\n--- Updating hreflang tags on FR/EN pages ---")
    updated = 0

    for country in COUNTRIES:
        lang, fr_slug, en_slug, country_slug_native, page_slug = country[:5]
        native_url = f'{SITE_URL}/{lang}/{country_slug_native}/{page_slug}/'
        hreflang_tag = f'<link rel="alternate" hreflang="{lang}" href="{native_url}">'

        # Update FR page
        fr_path = os.path.join(BASE_DIR, 'fr', fr_slug, 'simulateur-impot', 'index.html')
        if not os.path.exists(fr_path):
            fr_path = os.path.join(BASE_DIR, 'fr', fr_slug, 'simulateur-impot-revenu', 'index.html')

        for page_path in [fr_path, os.path.join(BASE_DIR, 'en', en_slug, 'income-tax', 'index.html')]:
            if os.path.exists(page_path):
                with open(page_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Check if hreflang already exists
                if f'hreflang="{lang}"' in content:
                    continue

                # Insert after the last hreflang tag
                insertion_point = content.rfind('<link rel="alternate" hreflang=')
                if insertion_point >= 0:
                    # Find end of that line
                    end_of_line = content.find('\n', insertion_point)
                    if end_of_line >= 0:
                        content = content[:end_of_line + 1] + '    ' + hreflang_tag + '\n' + content[end_of_line + 1:]
                        with open(page_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        updated += 1

    print(f"  Updated {updated} files with hreflang tags")


def main():
    print(f"Generating native-language pages...")
    print(f"Source directory: {BASE_DIR}")
    print(f"Countries to process: {len(COUNTRIES)}\n")

    success = 0
    skipped = 0

    for country in COUNTRIES:
        lang, fr_slug, en_slug, country_slug_native, page_slug, country_name = country[:6]
        rel_path = f'{lang}/{country_slug_native}/{page_slug}/index.html'

        if generate_page(country):
            print(f"  OK: {rel_path}")
            success += 1
        else:
            skipped += 1

    print(f"\nGeneration complete! Created: {success}, Skipped: {skipped}")

    # Update hreflang tags
    update_hreflang_tags()

    print("\nDone!")


if __name__ == '__main__':
    main()
