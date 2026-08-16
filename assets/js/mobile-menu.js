/* Mobile Menu - Country search & toggle */
(function() {
    var countries = [
        { name: 'Allemagne', flag: '\u{1F1E9}\u{1F1EA}', url: '/fr/allemagne/simulateur-impot/', region: 'europe' },
        { name: 'Belgique', flag: '\u{1F1E7}\u{1F1EA}', url: '/fr/belgique/simulateur-impot/', region: 'europe' },
        { name: 'Danemark', flag: '\u{1F1E9}\u{1F1F0}', url: '/fr/danemark/simulateur-impot/', region: 'europe' },
        { name: 'Espagne', flag: '\u{1F1EA}\u{1F1F8}', url: '/fr/espagne/simulateur-impot/', region: 'europe' },
        { name: 'Grece', flag: '\u{1F1EC}\u{1F1F7}', url: '/fr/grece/simulateur-impot/', region: 'europe' },
        { name: 'Irlande', flag: '\u{1F1EE}\u{1F1EA}', url: '/fr/irlande/simulateur-impot/', region: 'europe' },
        { name: 'Italie', flag: '\u{1F1EE}\u{1F1F9}', url: '/fr/italie/simulateur-impot/', region: 'europe' },
        { name: 'Luxembourg', flag: '\u{1F1F1}\u{1F1FA}', url: '/fr/luxembourg/simulateur-impot/', region: 'europe' },
        { name: 'Pays-Bas', flag: '\u{1F1F3}\u{1F1F1}', url: '/fr/pays-bas/simulateur-impot/', region: 'europe' },
        { name: 'Portugal', flag: '\u{1F1F5}\u{1F1F9}', url: '/fr/portugal/simulateur-impot/', region: 'europe' },
        { name: 'Tchequie', flag: '\u{1F1E8}\u{1F1FF}', url: '/fr/tchequie/simulateur-impot/', region: 'europe' },
        { name: 'USA', flag: '\u{1F1FA}\u{1F1F8}', url: '/fr/usa/simulateur-impot/', region: 'americas' },
        { name: 'Mexique', flag: '\u{1F1F2}\u{1F1FD}', url: '/fr/mexique/simulateur-impot/', region: 'americas' },
        { name: 'Chine', flag: '\u{1F1E8}\u{1F1F3}', url: '/fr/chine/simulateur-impot/', region: 'asia' },
        { name: 'Coree du Sud', flag: '\u{1F1F0}\u{1F1F7}', url: '/fr/coree-du-sud/simulateur-impot/', region: 'asia' },
        { name: 'Thailande', flag: '\u{1F1F9}\u{1F1ED}', url: '/fr/thailande/simulateur-impot/', region: 'asia' }
    ];

    var regionLabels = {
        europe: '\u{1F30D} Europe',
        americas: '\u{1F30E} Ameriques',
        asia: '\u{1F30F} Asie'
    };

    var mobileList = document.getElementById('mobile-country-list');
    var mobileSearch = document.getElementById('mobile-country-search');
    var mobileNoResults = document.getElementById('mobile-no-results');

    function normalize(str) {
        return str.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    }

    function renderMobileCountries(filter) {
        filter = filter || '';
        var norm = normalize(filter);
        var filtered = countries.filter(function(c) { return normalize(c.name).indexOf(norm) !== -1; });

        if (filtered.length === 0) {
            if (mobileList) mobileList.innerHTML = '';
            if (mobileNoResults) mobileNoResults.classList.remove('hidden');
            return;
        }
        if (mobileNoResults) mobileNoResults.classList.add('hidden');

        var groups = {};
        filtered.forEach(function(c) {
            if (!groups[c.region]) groups[c.region] = [];
            groups[c.region].push(c);
        });

        var regionOrder = ['europe', 'americas', 'asia'];
        var html = '';
        regionOrder.forEach(function(region) {
            if (!groups[region]) return;
            html += '<div><div class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1.5 px-1">' + regionLabels[region] + '</div><div class="grid grid-cols-2 gap-0.5">';
            groups[region].forEach(function(c) {
                html += '<a href="' + c.url + '" class="flex items-center gap-1.5 text-sm text-slate-600 hover:text-slate-900 hover:bg-slate-50 py-1.5 px-2 rounded-lg transition-colors"><span>' + c.flag + '</span> ' + c.name + '</a>';
            });
            html += '</div></div>';
        });
        if (mobileList) mobileList.innerHTML = html;
    }

    if (mobileSearch) {
        mobileSearch.addEventListener('input', function() { renderMobileCountries(mobileSearch.value); });
    }
    renderMobileCountries();

    // Mobile menu toggle - CSS-driven via style.css (#mobile-menu.open)
    var mobileMenu = document.getElementById('mobile-menu');
    var mobileMenuBtn = document.getElementById('mobile-menu-btn');
    var menuOpen = false;

    // Prevent background scroll on touch devices when menu is open
    function preventBgScroll(e) {
        if (!mobileMenu.contains(e.target)) {
            e.preventDefault();
        }
    }

    function openMenu() {
        menuOpen = true;
        mobileMenu.classList.add('open');
        document.documentElement.classList.add('menu-open');
        document.addEventListener('touchmove', preventBgScroll, { passive: false });
    }

    function closeMenu() {
        menuOpen = false;
        mobileMenu.classList.remove('open');
        document.documentElement.classList.remove('menu-open');
        document.removeEventListener('touchmove', preventBgScroll);
    }

    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            if (menuOpen) {
                closeMenu();
            } else {
                openMenu();
            }
        });
    }
})();
