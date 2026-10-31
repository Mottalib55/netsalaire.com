#!/usr/bin/env node
/**
 * Tests du moteur brut → net France (assets/js/brut-net-fr.js) et des chiffres cités dans les pages
 * (RECETTE §17.4 et §22). Lancement : npm test.
 *
 * Cas chiffrés (sources relevées le 2026-10-31) :
 *  - SMIC 1 867,02 € brut → 1 477,93 € net : service-public.gouv.fr F2300 (net indicatif) ;
 *  - taux salariaux 2026 : service-public.gouv.fr F2302 ; 2 500 € brut non-cadre →
 *    2 500 × (1 − 11,31 % − 9,70 % × 98,25 %) = 1 978,99 € ; même résultat que salairebrutonet.com ;
 *  - 5 000 € brut : tranche 2 (8,64 % + 1,08 %) et CET 0,14 % au-delà de 4 005 €.
 */
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const racine = join(dirname(fileURLToPath(import.meta.url)), '..');
const require = createRequire(import.meta.url);
const M = require(join(racine, 'assets/js/brut-net-fr.js'));
const echecs = [];
const verifier = (ok, msg) => { if (!ok) echecs.push(msg); };
const netMensuel = (brut, statut) => M.brutVersNet(brut * 12, statut) / 12;
const proche = (a, b, tol = 0.005) => Math.abs(a - b) < tol;

// 1. Moteur
const CAS = [
  [1867.02, 'noncadre', 1477.93],
  [2500, 'noncadre', 1978.99],
  [2500, 'cadre', 1978.39],
  [3000, 'noncadre', 2374.79],
  [3000, 'cadre', 2374.07],
  [5000, 'noncadre', 3962.83],
  [5000, 'cadre', 3961.63],
];
for (const [brut, statut, attendu] of CAS) {
  const net = netMensuel(brut, statut);
  verifier(proche(net, attendu), `moteur : ${brut} € ${statut} → ${net.toFixed(2)} (attendu ${attendu})`);
}
verifier(proche(M.netVersBrut(1978.99 * 12, 'noncadre') / 12, 2500, 0.01), 'moteur : net → brut ne retrouve pas 2 500 €');
verifier(M.P.SMIC_MENSUEL_BRUT === 1867.02, 'paramètres : SMIC mensuel brut différent de 1 867,02 €');
// Impôt d'une personne seule (exemples de la page) : 2 500 € brut → 66 €/mois (même résultat que salairebrutonet.com)
verifier(Math.round(M.impotAnnuelUnePart(30000, 'noncadre') / 12) === 66, 'impôt : 2 500 € brut non-cadre devrait donner 66 €/mois');

// 2. Chiffres cités par la page du simulateur France
const page = readFileSync(join(racine, 'fr/france/simulateur-salaire-brut-net/index.html'), 'utf8').replace(/ |&nbsp;/g, ' ');
const arr = (x) => Math.round(x).toLocaleString('fr-FR').replace(/ | /g, ' ');
const cites = [
  [`2 770 EUR nets à un cadre`, netMensuel(3500, 'cadre')],
  [`près de 1 478 EUR nets`, netMensuel(1867.02, 'noncadre')],
  [`<strong>3 165 € net</strong>`, netMensuel(4000, 'cadre')],
  [`environ 2 968 € net mensuel pour un cadre`, netMensuel(3750, 'cadre')],
  [`>2 770 €</span>`, netMensuel(3500, 'cadre')],
  [`>3 962 €</span>`, netMensuel(5000, 'cadre')],
  [`>1 478 €</span>`, netMensuel(1867.02, 'noncadre')],
  [`>≈ 2 570 €</span>`, netMensuel(3500, 'cadre') - M.impotAnnuelUnePart(42000, 'cadre') / 12],
  [`>≈ 3 428 €</span>`, netMensuel(5000, 'cadre') - M.impotAnnuelUnePart(60000, 'cadre') / 12],
];
for (const [texte, valeur] of cites) {
  const chiffre = texte.match(/\d[\d ]*\d/)[0];
  verifier(page.includes(texte), `page : texte introuvable « ${texte} »`);
  verifier(chiffre === arr(valeur), `page : « ${texte} » alors que le moteur donne ${arr(valeur)}`);
}
verifier(!/COTIS_RATES|0\.22\b/.test(page), 'page : taux forfaitaire encore présent');
verifier(!/detail-chomage/.test(page), 'page : ligne de cotisation chômage salariale encore présente');

// 3. Plus aucune mention « sans pub » tant qu'AdSense est chargé
for (const f of ['fr/index.html', 'fr/faq/index.html']) {
  const s = readFileSync(join(racine, f), 'utf8');
  verifier(!/sans pub/i.test(s), `${f} : mention « sans pub » alors qu'AdSense est chargé`);
}

if (echecs.length) {
  console.log(echecs.map((e) => 'ÉCHEC ' + e).join('\n'));
  process.exit(1);
}
console.log(`OK : ${CAS.length} cas du moteur, ${cites.length} chiffres cités, mentions publicitaires`);
