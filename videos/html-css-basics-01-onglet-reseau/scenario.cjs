/**
 * Live coding « Lire les requêtes d'une page dans l'onglet Réseau »
 * (lab html-css-basics, étape 01, parties 01.2 et 01.3).
 *
 * Scène : barre d'adresse + page à gauche, vrais DevTools de Chromium à
 * droite (voir ../record.cjs). Les DevTools de Chromium sont en anglais : la
 * narration donne les deux noms, comme le lab.
 */
const MDN = 'https://developer.mozilla.org/fr/';

/** Remonte la liste des requêtes tout en haut (elle suit les dernières lignes). */
async function gridTop({ dt, moveTo, pause }) {
  await moveTo(640 + 300, 480, 400);
  for (let i = 0; i < 8; i++) { await dt.mouse.wheel(0, -900); await pause(60); }
  await pause(400);
}
const rows = (dt) => dt.locator('tr.data-grid-data-grid-node');

module.exports = {
  name: 'html-css-basics-01-onglet-reseau',
  title: 'Les bases HTML et CSS',
  subtitle: '01 · L’onglet Réseau',
  disableCache: true,
  segments: [
    {
      id: 'intro',
      say: "Bienvenue dans ce live coding Byte Layers. Première étape du lab HTML et CSS : lire les requêtes d'une page dans l'onglet Réseau des outils de développement. On va voir la requête de la page elle-même, et trois codes de statut : 200, 404 et 301.",
      // Pendant l'intro, la page de l'étape sur le site, qu'on fait défiler.
      run: async ({ go, site, moveTo, pause }) => {
        await pause(600);
        await go('https://byte-layers.com/fr/labs/html-css-basics-lab/01-onglet-reseau?stack=html-css', { delay: 18 });
        await moveTo(320, 420, 600);
        await pause(2500);
        for (let i = 0; i < 6; i++) { await site.mouse.wheel(0, 160); await pause(900); }
      },
    },
    {
      id: 'mdn',
      say: "Dans le navigateur, j'ouvre la page d'accueil de MDN, la documentation du web que citent tous les bits du cours.",
      run: async ({ go, pause }) => { await pause(1500); await go(MDN); },
    },
    {
      id: 'devtools',
      say: "J'ouvre les outils de développement : F12, ou Commande Option I sur Mac. Le panneau s'ouvre, ici à droite. Je clique sur l'onglet Réseau, Network en anglais. Il est vide : il n'enregistre les requêtes qu'une fois ouvert. Alors je recharge la page, en forçant : Commande Maj R. Le navigateur redemande tout au serveur.",
      run: async ({ dt, openDevtools, click, moveTo, pulse, reload, pause }) => {
        await pause(800);
        await openDevtools({ keysMs: 2200 });
        await pause(1500);
        await click(dt, dt.getByRole('tab', { name: 'Network' }), { hold: 800 });
        // La liste vide.
        await moveTo(640 + 320, 470, 650);
        await pulse();
        await pause(7500);
        await reload({ withKeys: ['⌘', '⇧', 'R'] });
        await pause(1500);
      },
    },
    {
      id: 'colonnes',
      say: "Une ligne par requête, et chaque colonne répond à une question. Le nom : le chemin demandé. Le statut : le code de la réponse. Le type : ce qu'elle contient, document pour le HTML, stylesheet pour le CSS, script, des images. Et la taille, le poids de la réponse.",
      run: async ({ dt, point, pause }) => {
        await pause(2200);
        await point(dt, dt.getByRole('columnheader', { name: /^Name/ }), { hold: 1600 });
        await point(dt, dt.getByRole('columnheader', { name: /^Status/ }), { hold: 1600 });
        await point(dt, dt.getByRole('columnheader', { name: /^Type/ }), { hold: 4500 });
        await point(dt, dt.getByRole('columnheader', { name: /^Size/ }), { hold: 1500 });
      },
    },
    {
      id: 'premiere',
      say: "Je remonte tout en haut. La première ligne, de type document, c'est la page elle-même : la requête décrite dans le bit. Toutes les autres sont venues après, parce que le navigateur a trouvé leurs adresses dans ce HTML. En bas du panneau, le nombre total de requêtes, pour une seule page.",
      run: async (ctx) => {
        const { dt, point, pause } = ctx;
        await gridTop(ctx);
        await point(dt, rows(dt).filter({ hasText: 'document' }).first().locator('td').first(), { hold: 3500 });
        await point(dt, rows(dt).nth(4).locator('td').nth(2), { hold: 3500 });
        await point(dt, dt.getByText(/^\d+ requests?$/), { hold: 2000 });
      },
    },
    {
      id: 'entetes',
      say: "Je clique sur cette première ligne. Un volet affiche les en-têtes, Headers en anglais. On y retrouve la méthode, GET, et le code de statut, 200. Plus bas, dans les en-têtes de la réponse, content-type : text slash html. C'est bien une page HTML.",
      run: async ({ dt, click, point, pause }) => {
        await click(dt, rows(dt).filter({ hasText: 'document' }).first().locator('td').first(), { hold: 1800 });
        await point(dt, dt.getByText('Request Method').first(), { hold: 1500 });
        await point(dt, dt.getByText('Status Code').first(), { hold: 2000 });
        const ct = dt.getByText(/^content-type$/i).last();
        await ct.scrollIntoViewIfNeeded();
        await pause(400);
        await point(dt, ct, { hold: 2500 });
      },
    },
    {
      id: 'erreur404',
      say: "Maintenant, une page qui n'existe pas. Je tape son adresse. MDN affiche sa page introuvable, et la première ligne de l'onglet Réseau porte le code 404.",
      run: async (ctx) => {
        const { dt, go, point, pause } = ctx;
        await pause(1200);
        await go('https://developer.mozilla.org/fr/page-qui-n-existe-pas', { delay: 40 });
        await pause(800);
        await gridTop(ctx);
        await point(dt, rows(dt).first().locator('td').nth(1), { hold: 2500 });
      },
    },
    {
      id: 'redirection',
      // Le lab fait cocher Keep log puis retaper l'adresse ; dans Chromium, les
      // lignes 301 restent visibles sans la case, et le second passage montre
      // un 307 (HSTS). La vidéo montre ce qui se passe vraiment : un seul passage.
      say: "Dernier essai : wikipedia point org, en http, et pas en https. Regardez la barre d'adresse : elle a changé toute seule, en https, avec www devant. L'onglet Réseau dit pourquoi. La première ligne porte le code 301 : une redirection, la ressource a déménagé. Le navigateur suit la nouvelle adresse, et arrive enfin sur www point wikipedia point org, avec un 200.",
      run: async (ctx) => {
        const { bar, dt, go, point, pause } = ctx;
        await go('http://wikipedia.org');
        await pause(1500);
        await point(bar, bar.locator('#url'), { hold: 3500 });
        await gridTop(ctx);
        await point(dt, rows(dt).first().locator('td').nth(1), { hold: 3500 });
        const www = rows(dt).filter({ hasText: 'www.wikipedia.org' }).first();
        await point(dt, www.locator('td').first(), { hold: 1500 });
        await point(dt, www.locator('td').nth(1), { hold: 2000 });
      },
    },
    {
      id: 'outro',
      say: "Il reste à noter tout ça dans le fichier notes point txt, dans VS Code : page égale 200, introuvable 404, redirection 301, et le nombre de requêtes de MDN. Le bouton Verify du lab contrôle vos notes. À vous de jouer !",
      run: async ({ moveTo, pause }) => { await pause(1000); await moveTo(320, 400, 800); await pause(2000); },
    },
  ],
};
