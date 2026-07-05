#!/usr/bin/env python3
"""
3 corrections:
1. Fix "N." text logo in footer → replace with favicon.svg img
2. Update root index.html with language-based redirect
3. Add "Countries" section to all footers
"""

import os
import re
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# TRANSLATIONS
# ============================================================
TRANSLATIONS = {
    'en': {'europe': 'Europe', 'mideast': 'Middle East', 'americas': 'Americas & Asia',
           'france': 'France', 'germany': 'Germany', 'spain': 'Spain', 'italy': 'Italy',
           'portugal': 'Portugal', 'switzerland': 'Switzerland', 'belgium': 'Belgium',
           'morocco': 'Morocco', 'uae': 'UAE', 'saudi': 'Saudi Arabia', 'qatar': 'Qatar',
           'usa': 'USA', 'brazil': 'Brazil', 'india': 'India', 'singapore': 'Singapore',
           'countries': 'Countries', 'copyright': 'Tax calculations are estimates for informational purposes only.',
           'faq': 'FAQ', 'legal': 'Legal', 'privacy': 'Privacy'},
    'fr': {'europe': 'Europe', 'mideast': 'Moyen-Orient', 'americas': 'Amériques & Asie',
           'france': 'France', 'germany': 'Allemagne', 'spain': 'Espagne', 'italy': 'Italie',
           'portugal': 'Portugal', 'switzerland': 'Suisse', 'belgium': 'Belgique',
           'morocco': 'Maroc', 'uae': 'EAU', 'saudi': 'Arabie Saoudite', 'qatar': 'Qatar',
           'usa': 'USA', 'brazil': 'Brésil', 'india': 'Inde', 'singapore': 'Singapour',
           'countries': 'Pays', 'copyright': 'Les calculs fiscaux sont des estimations à titre indicatif.',
           'faq': 'FAQ', 'legal': 'Mentions légales', 'privacy': 'Confidentialité'},
    'es': {'europe': 'Europa', 'mideast': 'Oriente Medio', 'americas': 'Américas y Asia',
           'france': 'Francia', 'germany': 'Alemania', 'spain': 'España', 'italy': 'Italia',
           'portugal': 'Portugal', 'switzerland': 'Suiza', 'belgium': 'Bélgica',
           'morocco': 'Marruecos', 'uae': 'EAU', 'saudi': 'Arabia Saudí', 'qatar': 'Catar',
           'usa': 'EE.UU.', 'brazil': 'Brasil', 'india': 'India', 'singapore': 'Singapur',
           'countries': 'Países', 'copyright': 'Los cálculos fiscales son estimaciones informativas.',
           'faq': 'FAQ', 'legal': 'Aviso legal', 'privacy': 'Privacidad'},
    'pt': {'europe': 'Europa', 'mideast': 'Oriente Médio', 'americas': 'Américas e Ásia',
           'france': 'França', 'germany': 'Alemanha', 'spain': 'Espanha', 'italy': 'Itália',
           'portugal': 'Portugal', 'switzerland': 'Suíça', 'belgium': 'Bélgica',
           'morocco': 'Marrocos', 'uae': 'EAU', 'saudi': 'Arábia Saudita', 'qatar': 'Catar',
           'usa': 'EUA', 'brazil': 'Brasil', 'india': 'Índia', 'singapore': 'Singapura',
           'countries': 'Países', 'copyright': 'Os cálculos fiscais são estimativas informativas.',
           'faq': 'FAQ', 'legal': 'Aviso legal', 'privacy': 'Privacidade'},
    'de': {'europe': 'Europa', 'mideast': 'Naher Osten', 'americas': 'Amerika & Asien',
           'france': 'Frankreich', 'germany': 'Deutschland', 'spain': 'Spanien', 'italy': 'Italien',
           'portugal': 'Portugal', 'switzerland': 'Schweiz', 'belgium': 'Belgien',
           'morocco': 'Marokko', 'uae': 'VAE', 'saudi': 'Saudi-Arabien', 'qatar': 'Katar',
           'usa': 'USA', 'brazil': 'Brasilien', 'india': 'Indien', 'singapore': 'Singapur',
           'countries': 'Länder', 'copyright': 'Steuerberechnungen sind Schätzungen zu Informationszwecken.',
           'faq': 'FAQ', 'legal': 'Impressum', 'privacy': 'Datenschutz'},
    'nl': {'europe': 'Europa', 'mideast': 'Midden-Oosten', 'americas': 'Amerika & Azië',
           'france': 'Frankrijk', 'germany': 'Duitsland', 'spain': 'Spanje', 'italy': 'Italië',
           'portugal': 'Portugal', 'switzerland': 'Zwitserland', 'belgium': 'België',
           'morocco': 'Marokko', 'uae': 'VAE', 'saudi': 'Saoedi-Arabië', 'qatar': 'Qatar',
           'usa': 'VS', 'brazil': 'Brazilië', 'india': 'India', 'singapore': 'Singapore',
           'countries': 'Landen', 'copyright': 'Belastingberekeningen zijn schattingen ter informatie.',
           'faq': 'FAQ', 'legal': 'Juridisch', 'privacy': 'Privacy'},
    'ar': {'europe': 'أوروبا', 'mideast': 'الشرق الأوسط', 'americas': 'الأمريكتين وآسيا',
           'france': 'فرنسا', 'germany': 'ألمانيا', 'spain': 'إسبانيا', 'italy': 'إيطاليا',
           'portugal': 'البرتغال', 'switzerland': 'سويسرا', 'belgium': 'بلجيكا',
           'morocco': 'المغرب', 'uae': 'الإمارات', 'saudi': 'السعودية', 'qatar': 'قطر',
           'usa': 'أمريكا', 'brazil': 'البرازيل', 'india': 'الهند', 'singapore': 'سنغافورة',
           'countries': 'الدول', 'copyright': 'الحسابات الضريبية تقديرات إرشادية.',
           'faq': 'FAQ', 'legal': 'قانوني', 'privacy': 'الخصوصية'},
    'it': {'europe': 'Europa', 'mideast': 'Medio Oriente', 'americas': 'Americhe e Asia',
           'france': 'Francia', 'germany': 'Germania', 'spain': 'Spagna', 'italy': 'Italia',
           'portugal': 'Portogallo', 'switzerland': 'Svizzera', 'belgium': 'Belgio',
           'morocco': 'Marocco', 'uae': 'EAU', 'saudi': 'Arabia Saudita', 'qatar': 'Qatar',
           'usa': 'USA', 'brazil': 'Brasile', 'india': 'India', 'singapore': 'Singapore',
           'countries': 'Paesi', 'copyright': 'I calcoli fiscali sono stime a scopo informativo.',
           'faq': 'FAQ', 'legal': 'Note legali', 'privacy': 'Privacy'},
    'sv': {'europe': 'Europa', 'mideast': 'Mellanöstern', 'americas': 'Amerika & Asien',
           'france': 'Frankrike', 'germany': 'Tyskland', 'spain': 'Spanien', 'italy': 'Italien',
           'portugal': 'Portugal', 'switzerland': 'Schweiz', 'belgium': 'Belgien',
           'morocco': 'Marocko', 'uae': 'Förenade Arabemiraten', 'saudi': 'Saudiarabien', 'qatar': 'Qatar',
           'usa': 'USA', 'brazil': 'Brasilien', 'india': 'Indien', 'singapore': 'Singapore',
           'countries': 'Länder', 'copyright': 'Skatteberäkningar är uppskattningar i informationssyfte.',
           'faq': 'FAQ', 'legal': 'Juridisk', 'privacy': 'Integritet'},
    'no': {'europe': 'Europa', 'mideast': 'Midtøsten', 'americas': 'Amerika og Asia',
           'france': 'Frankrike', 'germany': 'Tyskland', 'spain': 'Spania', 'italy': 'Italia',
           'portugal': 'Portugal', 'switzerland': 'Sveits', 'belgium': 'Belgia',
           'morocco': 'Marokko', 'uae': 'UAE', 'saudi': 'Saudi-Arabia', 'qatar': 'Qatar',
           'usa': 'USA', 'brazil': 'Brasil', 'india': 'India', 'singapore': 'Singapore',
           'countries': 'Land', 'copyright': 'Skatteberegninger er estimater kun til informasjonsformål.',
           'faq': 'FAQ', 'legal': 'Juridisk', 'privacy': 'Personvern'},
    'da': {'europe': 'Europa', 'mideast': 'Mellemøsten', 'americas': 'Amerika og Asien',
           'france': 'Frankrig', 'germany': 'Tyskland', 'spain': 'Spanien', 'italy': 'Italien',
           'portugal': 'Portugal', 'switzerland': 'Schweiz', 'belgium': 'Belgien',
           'morocco': 'Marokko', 'uae': 'UAE', 'saudi': 'Saudi-Arabien', 'qatar': 'Qatar',
           'usa': 'USA', 'brazil': 'Brasilien', 'india': 'Indien', 'singapore': 'Singapore',
           'countries': 'Lande', 'copyright': 'Skatteberegninger er estimater til informationsformål.',
           'faq': 'FAQ', 'legal': 'Juridisk', 'privacy': 'Privatliv'},
    'fi': {'europe': 'Eurooppa', 'mideast': 'Lähi-itä', 'americas': 'Amerikka ja Aasia',
           'france': 'Ranska', 'germany': 'Saksa', 'spain': 'Espanja', 'italy': 'Italia',
           'portugal': 'Portugali', 'switzerland': 'Sveitsi', 'belgium': 'Belgia',
           'morocco': 'Marokko', 'uae': 'UAE', 'saudi': 'Saudi-Arabia', 'qatar': 'Qatar',
           'usa': 'USA', 'brazil': 'Brasilia', 'india': 'Intia', 'singapore': 'Singapore',
           'countries': 'Maat', 'copyright': 'Verolaskelmat ovat arvioita tiedoksi.',
           'faq': 'FAQ', 'legal': 'Oikeudellinen', 'privacy': 'Tietosuoja'},
    'el': {'europe': 'Ευρώπη', 'mideast': 'Μέση Ανατολή', 'americas': 'Αμερική & Ασία',
           'france': 'Γαλλία', 'germany': 'Γερμανία', 'spain': 'Ισπανία', 'italy': 'Ιταλία',
           'portugal': 'Πορτογαλία', 'switzerland': 'Ελβετία', 'belgium': 'Βέλγιο',
           'morocco': 'Μαρόκο', 'uae': 'ΗΑΕ', 'saudi': 'Σαουδική Αραβία', 'qatar': 'Κατάρ',
           'usa': 'ΗΠΑ', 'brazil': 'Βραζιλία', 'india': 'Ινδία', 'singapore': 'Σιγκαπούρη',
           'countries': 'Χώρες', 'copyright': 'Οι φορολογικοί υπολογισμοί είναι εκτιμήσεις ενημερωτικού χαρακτήρα.',
           'faq': 'FAQ', 'legal': 'Νομικά', 'privacy': 'Απόρρητο'},
    'pl': {'europe': 'Europa', 'mideast': 'Bliski Wschód', 'americas': 'Ameryki i Azja',
           'france': 'Francja', 'germany': 'Niemcy', 'spain': 'Hiszpania', 'italy': 'Włochy',
           'portugal': 'Portugalia', 'switzerland': 'Szwajcaria', 'belgium': 'Belgia',
           'morocco': 'Maroko', 'uae': 'ZEA', 'saudi': 'Arabia Saudyjska', 'qatar': 'Katar',
           'usa': 'USA', 'brazil': 'Brazylia', 'india': 'Indie', 'singapore': 'Singapur',
           'countries': 'Kraje', 'copyright': 'Obliczenia podatkowe są szacunkami informacyjnymi.',
           'faq': 'FAQ', 'legal': 'Prawne', 'privacy': 'Prywatność'},
    'cs': {'europe': 'Evropa', 'mideast': 'Blízký východ', 'americas': 'Amerika a Asie',
           'france': 'Francie', 'germany': 'Německo', 'spain': 'Španělsko', 'italy': 'Itálie',
           'portugal': 'Portugalsko', 'switzerland': 'Švýcarsko', 'belgium': 'Belgie',
           'morocco': 'Maroko', 'uae': 'SAE', 'saudi': 'Saúdská Arábie', 'qatar': 'Katar',
           'usa': 'USA', 'brazil': 'Brazílie', 'india': 'Indie', 'singapore': 'Singapur',
           'countries': 'Země', 'copyright': 'Daňové výpočty jsou informativní odhady.',
           'faq': 'FAQ', 'legal': 'Právní', 'privacy': 'Soukromí'},
    'hu': {'europe': 'Európa', 'mideast': 'Közel-Kelet', 'americas': 'Amerika és Ázsia',
           'france': 'Franciaország', 'germany': 'Németország', 'spain': 'Spanyolország', 'italy': 'Olaszország',
           'portugal': 'Portugália', 'switzerland': 'Svájc', 'belgium': 'Belgium',
           'morocco': 'Marokkó', 'uae': 'EAE', 'saudi': 'Szaúd-Arábia', 'qatar': 'Katar',
           'usa': 'USA', 'brazil': 'Brazília', 'india': 'India', 'singapore': 'Szingapúr',
           'countries': 'Országok', 'copyright': 'Az adószámítások tájékoztató jellegű becslések.',
           'faq': 'FAQ', 'legal': 'Jogi', 'privacy': 'Adatvédelem'},
    'ro': {'europe': 'Europa', 'mideast': 'Orientul Mijlociu', 'americas': 'Americi și Asia',
           'france': 'Franța', 'germany': 'Germania', 'spain': 'Spania', 'italy': 'Italia',
           'portugal': 'Portugalia', 'switzerland': 'Elveția', 'belgium': 'Belgia',
           'morocco': 'Maroc', 'uae': 'EAU', 'saudi': 'Arabia Saudită', 'qatar': 'Qatar',
           'usa': 'SUA', 'brazil': 'Brazilia', 'india': 'India', 'singapore': 'Singapore',
           'countries': 'Țări', 'copyright': 'Calculele fiscale sunt estimări informative.',
           'faq': 'FAQ', 'legal': 'Legal', 'privacy': 'Confidențialitate'},
    'hr': {'europe': 'Europa', 'mideast': 'Bliski istok', 'americas': 'Amerika i Azija',
           'france': 'Francuska', 'germany': 'Njemačka', 'spain': 'Španjolska', 'italy': 'Italija',
           'portugal': 'Portugal', 'switzerland': 'Švicarska', 'belgium': 'Belgija',
           'morocco': 'Maroko', 'uae': 'UAE', 'saudi': 'Saudijska Arabija', 'qatar': 'Katar',
           'usa': 'SAD', 'brazil': 'Brazil', 'india': 'Indija', 'singapore': 'Singapur',
           'countries': 'Zemlje', 'copyright': 'Porezni izračuni su informativne procjene.',
           'faq': 'FAQ', 'legal': 'Pravno', 'privacy': 'Privatnost'},
    'tr': {'europe': 'Avrupa', 'mideast': 'Orta Doğu', 'americas': 'Amerika ve Asya',
           'france': 'Fransa', 'germany': 'Almanya', 'spain': 'İspanya', 'italy': 'İtalya',
           'portugal': 'Portekiz', 'switzerland': 'İsviçre', 'belgium': 'Belçika',
           'morocco': 'Fas', 'uae': 'BAE', 'saudi': 'Suudi Arabistan', 'qatar': 'Katar',
           'usa': 'ABD', 'brazil': 'Brezilya', 'india': 'Hindistan', 'singapore': 'Singapur',
           'countries': 'Ülkeler', 'copyright': 'Vergi hesaplamaları bilgilendirme amaçlı tahminlerdir.',
           'faq': 'FAQ', 'legal': 'Yasal', 'privacy': 'Gizlilik'},
    'ja': {'europe': 'ヨーロッパ', 'mideast': '中東', 'americas': 'アメリカ・アジア',
           'france': 'フランス', 'germany': 'ドイツ', 'spain': 'スペイン', 'italy': 'イタリア',
           'portugal': 'ポルトガル', 'switzerland': 'スイス', 'belgium': 'ベルギー',
           'morocco': 'モロッコ', 'uae': 'UAE', 'saudi': 'サウジアラビア', 'qatar': 'カタール',
           'usa': 'アメリカ', 'brazil': 'ブラジル', 'india': 'インド', 'singapore': 'シンガポール',
           'countries': '国一覧', 'copyright': '税額計算は情報提供を目的とした概算です。',
           'faq': 'FAQ', 'legal': '法的情報', 'privacy': 'プライバシー'},
    'ko': {'europe': '유럽', 'mideast': '중동', 'americas': '아메리카 & 아시아',
           'france': '프랑스', 'germany': '독일', 'spain': '스페인', 'italy': '이탈리아',
           'portugal': '포르투갈', 'switzerland': '스위스', 'belgium': '벨기에',
           'morocco': '모로코', 'uae': 'UAE', 'saudi': '사우디아라비아', 'qatar': '카타르',
           'usa': '미국', 'brazil': '브라질', 'india': '인도', 'singapore': '싱가포르',
           'countries': '국가', 'copyright': '세금 계산은 참고용 추정치입니다.',
           'faq': 'FAQ', 'legal': '법적 고지', 'privacy': '개인정보'},
    'zh': {'europe': '欧洲', 'mideast': '中东', 'americas': '美洲与亚洲',
           'france': '法国', 'germany': '德国', 'spain': '西班牙', 'italy': '意大利',
           'portugal': '葡萄牙', 'switzerland': '瑞士', 'belgium': '比利时',
           'morocco': '摩洛哥', 'uae': '阿联酋', 'saudi': '沙特阿拉伯', 'qatar': '卡塔尔',
           'usa': '美国', 'brazil': '巴西', 'india': '印度', 'singapore': '新加坡',
           'countries': '国家', 'copyright': '税务计算仅为信息性估算。',
           'faq': 'FAQ', 'legal': '法律声明', 'privacy': '隐私'},
    'th': {'europe': 'ยุโรป', 'mideast': 'ตะวันออกกลาง', 'americas': 'อเมริกาและเอเชีย',
           'france': 'ฝรั่งเศส', 'germany': 'เยอรมนี', 'spain': 'สเปน', 'italy': 'อิตาลี',
           'portugal': 'โปรตุเกส', 'switzerland': 'สวิตเซอร์แลนด์', 'belgium': 'เบลเยียม',
           'morocco': 'โมร็อกโก', 'uae': 'ยูเออี', 'saudi': 'ซาอุดีอาระเบีย', 'qatar': 'กาตาร์',
           'usa': 'สหรัฐฯ', 'brazil': 'บราซิล', 'india': 'อินเดีย', 'singapore': 'สิงคโปร์',
           'countries': 'ประเทศ', 'copyright': 'การคำนวณภาษีเป็นเพียงการประมาณการ',
           'faq': 'FAQ', 'legal': 'กฎหมาย', 'privacy': 'ความเป็นส่วนตัว'},
    'ms': {'europe': 'Eropah', 'mideast': 'Timur Tengah', 'americas': 'Amerika & Asia',
           'france': 'Perancis', 'germany': 'Jerman', 'spain': 'Sepanyol', 'italy': 'Itali',
           'portugal': 'Portugal', 'switzerland': 'Switzerland', 'belgium': 'Belgium',
           'morocco': 'Maghribi', 'uae': 'UAE', 'saudi': 'Arab Saudi', 'qatar': 'Qatar',
           'usa': 'AS', 'brazil': 'Brazil', 'india': 'India', 'singapore': 'Singapura',
           'countries': 'Negara', 'copyright': 'Pengiraan cukai adalah anggaran untuk tujuan maklumat.',
           'faq': 'FAQ', 'legal': 'Undang-undang', 'privacy': 'Privasi'},
    'id': {'europe': 'Eropa', 'mideast': 'Timur Tengah', 'americas': 'Amerika & Asia',
           'france': 'Prancis', 'germany': 'Jerman', 'spain': 'Spanyol', 'italy': 'Italia',
           'portugal': 'Portugal', 'switzerland': 'Swiss', 'belgium': 'Belgia',
           'morocco': 'Maroko', 'uae': 'UAE', 'saudi': 'Arab Saudi', 'qatar': 'Qatar',
           'usa': 'AS', 'brazil': 'Brasil', 'india': 'India', 'singapore': 'Singapura',
           'countries': 'Negara', 'copyright': 'Perhitungan pajak adalah perkiraan untuk tujuan informasi.',
           'faq': 'FAQ', 'legal': 'Hukum', 'privacy': 'Privasi'},
    'vi': {'europe': 'Châu Âu', 'mideast': 'Trung Đông', 'americas': 'Châu Mỹ & Châu Á',
           'france': 'Pháp', 'germany': 'Đức', 'spain': 'Tây Ban Nha', 'italy': 'Ý',
           'portugal': 'Bồ Đào Nha', 'switzerland': 'Thụy Sĩ', 'belgium': 'Bỉ',
           'morocco': 'Ma-rốc', 'uae': 'UAE', 'saudi': 'Ả Rập Xê-út', 'qatar': 'Qatar',
           'usa': 'Mỹ', 'brazil': 'Brazil', 'india': 'Ấn Độ', 'singapore': 'Singapore',
           'countries': 'Quốc gia', 'copyright': 'Tính toán thuế chỉ mang tính ước lượng tham khảo.',
           'faq': 'FAQ', 'legal': 'Pháp lý', 'privacy': 'Quyền riêng tư'},
}

# Country link URLs by page language
COUNTRY_URLS_FR = {
    'france': '/fr/france/simulateur-impot-revenu/',
    'germany': '/fr/allemagne/simulateur-impot/',
    'spain': '/fr/espagne/simulateur-impot/',
    'italy': '/fr/italie/simulateur-impot/',
    'portugal': '/fr/portugal/simulateur-impot/',
    'switzerland': '/fr/suisse/simulateur-impot/',
    'belgium': '/fr/belgique/simulateur-impot/',
    'morocco': '/fr/maroc/simulateur-impot-revenu/',
    'uae': '/fr/dubai/simulateur-impot/',
    'saudi': '/fr/arabie-saoudite/simulateur-impot/',
    'qatar': '/fr/qatar/simulateur-impot/',
    'usa': '/fr/usa/simulateur-impot/',
    'brazil': '/fr/bresil/simulateur-impot/',
    'india': '/fr/inde/simulateur-impot/',
    'singapore': '/fr/singapour/simulateur-impot/',
}

COUNTRY_URLS_EN = {
    'france': '/en/france/income-tax/',
    'germany': '/en/germany/income-tax/',
    'spain': '/en/spain/income-tax/',
    'italy': '/en/italy/income-tax/',
    'portugal': '/en/portugal/income-tax/',
    'switzerland': '/en/switzerland/income-tax/',
    'belgium': '/en/belgium/income-tax/',
    'morocco': '/en/morocco/income-tax/',
    'uae': '/en/dubai/income-tax/',
    'saudi': '/en/saudi-arabia/income-tax/',
    'qatar': '/en/qatar/income-tax/',
    'usa': '/en/usa/income-tax/',
    'brazil': '/en/brazil/income-tax/',
    'india': '/en/india/income-tax/',
    'singapore': '/en/singapore/income-tax/',
}

FOOTER_LINKS_FR = {'faq': '/fr/faq/', 'legal': '/fr/mentions-legales/', 'privacy': '/fr/politique-confidentialite/'}
FOOTER_LINKS_EN = {'faq': '/en/faq/', 'legal': '/en/legal-notice/', 'privacy': '/en/privacy-policy/'}

NATIVE_LANGS = ['ar', 'cs', 'da', 'de', 'el', 'es', 'fi', 'hr', 'hu',
                'id', 'it', 'ja', 'ko', 'ms', 'nl', 'no', 'pl', 'pt',
                'ro', 'sv', 'th', 'tr', 'vi', 'zh']
ALL_LANGS = ['en', 'fr'] + NATIVE_LANGS


def detect_lang(filepath):
    rel = os.path.relpath(filepath, BASE_DIR).replace('\\', '/')
    parts = rel.split('/')
    if parts[0] in ALL_LANGS:
        return parts[0]
    return None


def get_translations(lang):
    return TRANSLATIONS.get(lang, TRANSLATIONS['en'])


def get_country_urls(lang):
    if lang == 'fr':
        return COUNTRY_URLS_FR
    return COUNTRY_URLS_EN


def get_footer_links(lang):
    if lang == 'fr':
        return FOOTER_LINKS_FR
    return FOOTER_LINKS_EN


def build_countries_dark(lang):
    """Build countries section HTML for dark footer (Pattern 2)."""
    t = get_translations(lang)
    urls = get_country_urls(lang)
    link_cls = 'hover:text-white transition-colors'

    europe_links = ''.join(
        f'\n                        <li><a href="{urls[k]}" class="{link_cls}">{t[k]}</a></li>'
        for k in ['france', 'germany', 'spain', 'italy', 'portugal', 'switzerland', 'belgium']
    )
    mideast_links = ''.join(
        f'\n                        <li><a href="{urls[k]}" class="{link_cls}">{t[k]}</a></li>'
        for k in ['morocco', 'uae', 'saudi', 'qatar']
    )
    americas_links = ''.join(
        f'\n                        <li><a href="{urls[k]}" class="{link_cls}">{t[k]}</a></li>'
        for k in ['usa', 'brazil', 'india', 'singapore']
    )

    return f'''        <div class="grid grid-cols-2 md:grid-cols-3 gap-6 mb-6">
                <div>
                    <p class="text-slate-300 font-semibold mb-2 text-xs uppercase tracking-wider">{t['europe']}</p>
                    <ul class="space-y-1">{europe_links}
                    </ul>
                </div>
                <div>
                    <p class="text-slate-300 font-semibold mb-2 text-xs uppercase tracking-wider">{t['mideast']}</p>
                    <ul class="space-y-1">{mideast_links}
                    </ul>
                </div>
                <div>
                    <p class="text-slate-300 font-semibold mb-2 text-xs uppercase tracking-wider">{t['americas']}</p>
                    <ul class="space-y-1">{americas_links}
                    </ul>
                </div>
            </div>'''


def build_countries_light(lang):
    """Build countries section HTML for light footer (Pattern 1)."""
    t = get_translations(lang)
    urls = get_country_urls(lang)
    link_cls = 'hover:text-slate-900 transition-colors'

    europe_links = ''.join(
        f'\n                        <li><a href="{urls[k]}" class="{link_cls}">{t[k]}</a></li>'
        for k in ['france', 'germany', 'spain', 'italy', 'portugal', 'switzerland', 'belgium']
    )
    mideast_links = ''.join(
        f'\n                        <li><a href="{urls[k]}" class="{link_cls}">{t[k]}</a></li>'
        for k in ['morocco', 'uae', 'saudi', 'qatar']
    )
    americas_links = ''.join(
        f'\n                        <li><a href="{urls[k]}" class="{link_cls}">{t[k]}</a></li>'
        for k in ['usa', 'brazil', 'india', 'singapore']
    )

    return f'''            <div class="grid grid-cols-2 md:grid-cols-3 gap-6 pt-6 mt-2 border-t border-slate-200">
                <div>
                    <p class="font-semibold text-slate-900 mb-2 text-sm">{t['europe']}</p>
                    <ul class="space-y-1 text-sm text-slate-500">{europe_links}
                    </ul>
                </div>
                <div>
                    <p class="font-semibold text-slate-900 mb-2 text-sm">{t['mideast']}</p>
                    <ul class="space-y-1 text-sm text-slate-500">{mideast_links}
                    </ul>
                </div>
                <div>
                    <p class="font-semibold text-slate-900 mb-2 text-sm">{t['americas']}</p>
                    <ul class="space-y-1 text-sm text-slate-500">{americas_links}
                    </ul>
                </div>
            </div>'''


def build_countries_custom(lang):
    """Build countries section for Pattern 3 (custom CSS footer)."""
    t = get_translations(lang)
    urls = get_country_urls(lang)

    europe_links = ''.join(
        f'\n                        <li><a href="{urls[k]}">{t[k]}</a></li>'
        for k in ['france', 'germany', 'spain', 'italy', 'portugal', 'switzerland', 'belgium']
    )
    mideast_links = ''.join(
        f'\n                        <li><a href="{urls[k]}">{t[k]}</a></li>'
        for k in ['morocco', 'uae', 'saudi', 'qatar']
    )
    americas_links = ''.join(
        f'\n                        <li><a href="{urls[k]}">{t[k]}</a></li>'
        for k in ['usa', 'brazil', 'india', 'singapore']
    )

    return f'''            <div class="footer-grid" style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.1);">
                <div>
                    <h4>{t['europe']}</h4>
                    <ul>{europe_links}
                    </ul>
                </div>
                <div>
                    <h4>{t['mideast']}</h4>
                    <ul>{mideast_links}
                    </ul>
                </div>
                <div>
                    <h4>{t['americas']}</h4>
                    <ul>{americas_links}
                    </ul>
                </div>
            </div>'''


def process_dark_footer(content, lang):
    """Process Pattern 2: simple dark footer."""
    # Match the entire dark footer
    pattern = re.compile(
        r'(<footer class="bg-slate-900 text-slate-400 py-8 px-4">\s*'
        r'<div class="max-w-4xl mx-auto text-center text-sm">)'
        r'(.*?)'
        r'(</div>\s*</footer>)',
        re.DOTALL
    )

    match = pattern.search(content)
    if not match:
        return content, False

    countries_html = build_countries_dark(lang)
    t = get_translations(lang)
    fl = get_footer_links(lang)

    # Extract existing copyright text
    copyright_match = re.search(r'<p>(©.*?)</p>', match.group(2))
    copyright_text = copyright_match.group(1) if copyright_match else f'© 2026 NetSalaire. {t["copyright"]}'

    new_footer = f'''<footer class="bg-slate-900 text-slate-400 py-8 px-4">
        <div class="max-w-4xl mx-auto text-sm">
{countries_html}
            <div class="border-t border-slate-700 pt-4 text-center">
                <p>{copyright_text}</p>
                <div class="flex justify-center gap-4 mt-2">
                    <a href="{fl['faq']}" class="hover:text-white transition-colors">{t['faq']}</a>
                    <a href="{fl['legal']}" class="hover:text-white transition-colors">{t['legal']}</a>
                    <a href="{fl['privacy']}" class="hover:text-white transition-colors">{t['privacy']}</a>
                </div>
            </div>
        </div>
    </footer>'''

    new_content = content[:match.start()] + new_footer + content[match.end():]
    return new_content, True


def process_rich_footer(content, lang):
    """Process Pattern 1: rich white footer."""
    changed = False

    # Fix "N." logo in footer
    old_logo = '<div class="w-6 h-6 bg-slate-900 rounded flex items-center justify-center text-white text-xs font-bold">N.</div>'
    new_logo = '<img src="/favicon.svg" alt="NetSalaire" class="w-6 h-6">'
    if old_logo in content:
        content = content.replace(old_logo, new_logo)
        changed = True

    # Insert countries section before the copyright separator
    insert_marker = '<div class="pt-8 border-t border-slate-200'
    if insert_marker in content:
        countries_html = build_countries_light(lang)
        content = content.replace(insert_marker, countries_html + '\n            ' + insert_marker)
        changed = True

    return content, changed


def process_custom_footer(content, lang):
    """Process Pattern 3: custom CSS footer (en/france/income-tax/)."""
    insert_marker = '<div class="footer-bottom">'
    if insert_marker not in content:
        return content, False

    countries_html = build_countries_custom(lang)
    content = content.replace(insert_marker, countries_html + '\n            ' + insert_marker)
    return content, True


def process_file(filepath):
    lang = detect_lang(filepath)
    if not lang:
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changed = False

    # Detect footer pattern and process
    if 'class="footer">' in content and 'footer-grid' in content:
        # Pattern 3: custom CSS footer
        content, changed = process_custom_footer(content, lang)
    elif 'py-12 px-6 border-t border-slate-200 bg-white' in content:
        # Pattern 1: rich white footer
        content, changed = process_rich_footer(content, lang)
    elif 'bg-slate-900 text-slate-400 py-8 px-4' in content:
        # Pattern 2: simple dark footer
        content, changed = process_dark_footer(content, lang)

    if changed and content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def fix_root_redirect():
    """Correction 2: language-based redirect on root index.html."""
    index_path = os.path.join(BASE_DIR, 'index.html')

    new_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="canonical" href="https://netsalaire.com/en/">
    <meta name="description" content="Free income tax calculators for 50+ countries. Simulate your net salary, income tax, and social contributions. Updated 2026 rates.">
    <title>NetSalaire - Free Income Tax Calculator 2026</title>
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <script>
        (function() {
            var lang = (navigator.language || navigator.userLanguage || 'en').toLowerCase();
            var code = lang.split('-')[0];
            var map = {
                fr: '/fr/', pt: '/pt/', es: '/es/', de: '/de/',
                it: '/it/', pl: '/pl/', ro: '/ro/', nl: '/nl/',
                ar: '/ar/', ko: '/ko/', sv: '/sv/',
                ja: '/ja/', zh: '/zh/', tr: '/tr/', da: '/da/',
                fi: '/fi/', no: '/no/', el: '/el/', cs: '/cs/',
                hu: '/hu/', hr: '/hr/', th: '/th/', ms: '/ms/',
                id: '/id/', vi: '/vi/'
            };
            window.location.replace(map[code] || '/en/');
        })();
    </script>
</head>
<body>
    <p>Redirecting... <a href="/en/">Click here</a> if not redirected.</p>
</body>
</html>
'''

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("  Fixed root index.html redirect")


def main():
    # Correction 2: root redirect
    print("=== Correction 2: Root redirect ===")
    fix_root_redirect()

    # Corrections 1 & 3: footer fixes
    print("\n=== Corrections 1 & 3: Footer logo + countries ===")
    html_files = sorted(glob.glob(os.path.join(BASE_DIR, '**', '*.html'), recursive=True))

    modified = []
    skipped = []
    for filepath in html_files:
        rel = os.path.relpath(filepath, BASE_DIR)
        if rel in ('index.html', '404.html') or rel.startswith('admin'):
            continue

        if process_file(filepath):
            modified.append(rel)

    print(f"  Modified: {len(modified)} files")
    if modified:
        for f in modified[:10]:
            print(f"    {f}")
        if len(modified) > 10:
            print(f"    ... and {len(modified) - 10} more")


if __name__ == '__main__':
    main()
