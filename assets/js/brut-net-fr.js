/*
 * Moteur brut → net France (secteur privé), paramètres 2026.
 * Utilisé par /fr/france/simulateur-salaire-brut-net/ et vérifié par scripts/test-brut-net-fr.mjs.
 *
 * Même calcul que celui de salairebrutonet.com (mêmes taux, même ordre), repris ici sans
 * dépendance entre les deux sites. Le calcul se fait sur l'année : plafond annuel de la
 * Sécurité sociale, ce qui revient au calcul mensuel × 12 pour un salaire régulier.
 *
 * Sources (relevées le 2026-10-31) :
 *  - taux salariaux : service-public.gouv.fr F2302 « Cotisations salariales » (vérifié le
 *    1er janvier 2026) : vieillesse 6,90 % jusqu'au plafond + 0,40 % sur la totalité ;
 *    Agirc-Arrco 3,15 % (tranche 1) et 8,64 % (tranche 2, de 1 à 8 plafonds) ; CEG 0,86 % (T1)
 *    et 1,08 % (T2) ; CET 0,14 % sur T1 + T2 dès que le salaire dépasse le plafond ;
 *    APEC 0,024 % jusqu'à 4 plafonds (cadres) ; CSG 9,2 % (dont 2,4 % non déductible) et
 *    CRDS 0,5 % sur 98,25 % du brut jusqu'à 4 plafonds, 100 % au-delà ; aucune cotisation
 *    chômage salariale depuis le 1er octobre 2018. Taux Agirc-Arrco confirmés par
 *    reglementation.agirc-arrco.fr (« Cotisations au régime Agirc-Arrco en 2026 ») ;
 *  - plafond de la Sécurité sociale 2026 : 4 005 € par mois, 48 060 € par an (F2302) ;
 *  - SMIC : service-public.gouv.fr F2300 — 12,31 € brut de l'heure, 1 867,02 € brut par mois
 *    (35 h) depuis le 1er juin 2026, 1 477,93 € net indicatif ;
 *  - impôt (exemples de la page seulement) : barème 2026 sur les revenus 2025, abattement de
 *    10 % (minimum 509 €, maximum 14 555 €), décote 897 € / 45,25 %, une part.
 */
(function (racine) {
    'use strict';

    var P = {
        PSS_ANNUEL: 48060,
        SMIC_HORAIRE: 12.31,
        SMIC_MENSUEL_BRUT: 1867.02,
        VIEILLESSE_PLAFONNEE: 0.069,
        VIEILLESSE_DEPLAFONNEE: 0.004,
        AGIRC_ARRCO_T1: 0.0315,
        AGIRC_ARRCO_T2: 0.0864,
        CEG_T1: 0.0086,
        CEG_T2: 0.0108,
        CET: 0.0014,
        APEC: 0.00024,
        CSG_DEDUCTIBLE: 0.068,
        CSG_NON_DEDUCTIBLE: 0.024,
        CRDS: 0.005,
        ASSIETTE_CSG: 0.9825
    };

    // Cotisations salariales sur un brut annuel. statut : 'cadre' ou 'noncadre'.
    function cotisations(brutAnnuel, statut) {
        var b = Math.max(0, brutAnnuel || 0);
        var pss = P.PSS_ANNUEL;
        var t1 = Math.min(b, pss);
        var t2 = Math.min(Math.max(0, b - pss), 7 * pss);
        var assietteCsg = P.ASSIETTE_CSG * Math.min(b, 4 * pss) + Math.max(0, b - 4 * pss);
        var vieillesse = t1 * P.VIEILLESSE_PLAFONNEE + b * P.VIEILLESSE_DEPLAFONNEE;
        var complementaire = t1 * (P.AGIRC_ARRCO_T1 + P.CEG_T1) + t2 * (P.AGIRC_ARRCO_T2 + P.CEG_T2)
            + (b > pss ? (t1 + t2) * P.CET : 0);
        var apec = statut === 'cadre' ? Math.min(b, 4 * pss) * P.APEC : 0;
        var csgNonDeductible = assietteCsg * P.CSG_NON_DEDUCTIBLE;
        var crds = assietteCsg * P.CRDS;
        var csgCrds = assietteCsg * P.CSG_DEDUCTIBLE + csgNonDeductible + crds;
        return {
            vieillesse: vieillesse,
            complementaire: complementaire,
            apec: apec,
            csgCrds: csgCrds,
            nonDeductible: csgNonDeductible + crds,
            total: vieillesse + complementaire + apec + csgCrds
        };
    }

    function brutVersNet(brutAnnuel, statut) {
        return brutAnnuel - cotisations(brutAnnuel, statut).total;
    }

    // Inverse par dichotomie : le net croît strictement avec le brut.
    function netVersBrut(netAnnuel, statut) {
        if (!(netAnnuel > 0)) return 0;
        var bas = netAnnuel, haut = netAnnuel * 2;
        for (var i = 0; i < 100; i++) {
            var milieu = (bas + haut) / 2;
            if (brutVersNet(milieu, statut) < netAnnuel) bas = milieu; else haut = milieu;
        }
        return (bas + haut) / 2;
    }

    // Impôt annuel d'un célibataire sans enfant (une part), pour les exemples chiffrés.
    function impotAnnuelUnePart(brutAnnuel, statut) {
        var c = cotisations(brutAnnuel, statut);
        var netImposable = brutAnnuel - c.total + c.nonDeductible;
        var revenu = netImposable - Math.min(Math.max(netImposable * 0.1, 509), 14555);
        var tranches = [[11600, 0], [29579, 0.11], [84577, 0.30], [181917, 0.41], [Infinity, 0.45]];
        var impot = 0, bas = 0;
        for (var i = 0; i < tranches.length; i++) {
            if (revenu > bas) impot += (Math.min(revenu, tranches[i][0]) - bas) * tranches[i][1];
            bas = tranches[i][0];
        }
        var decote = 897 - 0.4525 * impot;
        if (decote > 0) impot = Math.max(0, impot - decote);
        return Math.round(impot);
    }

    var api = { P: P, cotisations: cotisations, brutVersNet: brutVersNet, netVersBrut: netVersBrut,
                impotAnnuelUnePart: impotAnnuelUnePart };
    if (typeof module !== 'undefined' && module.exports) module.exports = api;
    racine.BRUT_NET_FR = api;
})(typeof window !== 'undefined' ? window : globalThis);
