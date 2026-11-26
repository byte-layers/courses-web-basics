/**
 * Live coding « Modifier une page dans l'inspecteur »
 * (lab html-css-basics, étape 02, partie 02.1).
 *
 * Trois retouches sur une vraie page de MDN, une par langage : le texte du
 * titre (HTML, onglet Elements), sa couleur par l'attribut style puis sa
 * taille dans le volet Styles (CSS), une ligne dans la console (JavaScript) ;
 * puis un rechargement qui efface tout.
 *
 * Les DevTools de Chromium sont en anglais : la narration donne les deux noms.
 * Le clic droit « Inspecter » de la page est un menu natif, que Playwright ne
 * filme pas : la vidéo désigne le titre avec l'outil de sélection (la flèche).
 */
const PAGE = 'https://developer.mozilla.org/fr/docs/Web/HTML';

/** La ligne sélectionnée de l'arbre des éléments. */
const selected = (dt) => dt.locator('li.selected').first();

/** Tape lentement, comme une personne. */
async function typeSlow(dt, text, delay = 70) {
  for (const ch of text) { await dt.keyboard.type(ch); await new Promise((r) => setTimeout(r, delay)); }
}

module.exports = {
  name: 'html-css-basics-02-inspecteur',
  title: 'Les bases HTML et CSS',
  subtitle: '02 · Modifier une page dans l’inspecteur',
  devtools: true,
  segments: [
    {
      id: 'intro',
      say: "Bienvenue dans ce live coding Byte Layers. Deuxième étape du lab HTML et CSS : modifier une page qui n'est pas à vous, avec les outils de développement. Trois retouches, une par langage : le texte du titre en HTML, sa couleur et sa taille en CSS, et une ligne de JavaScript dans la console.",
      run: async ({ go, site, moveTo, pause }) => {
        await pause(600);
        await go('https://byte-layers.com/fr/labs/html-css-basics-lab/02-retirer-css-js?stack=html-css', { delay: 18 });
        await moveTo(320, 420, 600);
        await pause(2500);
        for (let i = 0; i < 6; i++) { await site.mouse.wheel(0, 160); await pause(900); }
      },
    },
    {
      id: 'mdn',
      say: "J'ouvre une page de MDN, celle sur le HTML. Son titre, tout en haut : HTML, HyperText Markup Language.",
      run: async ({ go, site, point, pause }) => {
        await pause(1200);
        await go(PAGE, { delay: 40 });
        await pause(600);
        await point(site, site.locator('main h1').first(), { hold: 2500 });
      },
    },
    {
      id: 'inspecter',
      say: "J'ouvre les outils de développement : F12. Je suis dans l'onglet Éléments, Elements en anglais. La flèche, en haut à gauche, sert à désigner un élément de la page. Je clique sur le titre : l'inspecteur le retrouve dans l'arbre de la page. C'est une balise h1. Le plus rapide, d'habitude : un clic droit sur le titre, puis Inspecter.",
      run: async ({ dt, site, openDevtools, click, point, pause }) => {
        await pause(400);
        await openDevtools({ keysMs: 2000 });
        await pause(1200);
        await point(dt, dt.getByRole('tab', { name: 'Elements' }), { hold: 1500 });
        await click(dt, dt.getByLabel('Select an element in the page to inspect it', { exact: true }), { hold: 1500 });
        const h1 = site.locator('main h1').first();
        await point(site, h1, { hold: 1200 });
        await click(site, h1, { hold: 1200 });
        await point(dt, selected(dt), { hold: 3000 });
      },
    },
    {
      id: 'texte',
      say: "Je double-clique sur son texte, dans l'arbre : il devient modifiable. J'écris un autre titre, et Entrée. La page change aussitôt.",
      run: async ({ dt, site, point, pause }) => {
        await pause(400);
        const txt = selected(dt).locator('.webkit-html-text-node').first();
        const c = await point(dt, txt, { hold: 600 });
        await dt.mouse.dblclick(c.local.x, c.local.y);
        await pause(500);
        await dt.keyboard.press('ControlOrMeta+A');
        await typeSlow(dt, 'Mon titre à moi');
        await pause(400);
        await dt.keyboard.press('Enter');
        await pause(600);
        await point(site, site.locator('main h1').first(), { hold: 2000 });
      },
    },
    {
      id: 'couleur',
      say: "Pour la couleur : clic droit sur la balise, Ajouter un attribut, Add attribute. J'écris style égale, entre guillemets, color deux-points deeppink. Entrée : le titre devient rose. L'attribut style porte du CSS, directement dans la balise.",
      run: async ({ dt, site, point, click, pause }) => {
        await pause(300);
        const tag = selected(dt).locator('.webkit-html-tag-name').first();
        const c = await point(dt, tag, { hold: 500 });
        await dt.mouse.click(c.local.x, c.local.y, { button: 'right' });
        await pause(900);
        await click(dt, dt.getByText('Add attribute', { exact: true }), { hold: 600 });
        await typeSlow(dt, 'style="color: deeppink"');
        await pause(500);
        await dt.keyboard.press('Enter');
        await pause(700);
        await point(site, site.locator('main h1').first(), { hold: 2200 });
      },
    },
    {
      id: 'taille',
      say: "Pour la taille, je passe par le volet Styles, sous l'arbre. Son premier bloc, element point style, montre justement cet attribut. Je clique dedans pour ajouter une déclaration : font-size, quatre-vingts pixels. Le titre grossit. Juste en dessous, la règle de MDN pour ce titre : sa font-size est barrée. Elle ne s'applique plus, celle de l'attribut passe avant.",
      run: async ({ dt, site, point, pause }) => {
        await pause(300);
        const section = dt.locator('.styles-section').first();
        await point(dt, section.locator('.selector').first(), { hold: 1800 });
        // Clic sur l'accolade fermante : nouvelle déclaration.
        const close = section.locator('.sidebar-pane-closing-brace').first();
        const c = await point(dt, close, { hold: 500 });
        await dt.mouse.click(c.local.x + 20, c.local.y);
        await pause(500);
        await typeSlow(dt, 'font-size');
        await dt.keyboard.press('Tab');
        await typeSlow(dt, '80px');
        await dt.keyboard.press('Enter');
        await pause(400);
        await dt.keyboard.press('Escape');
        await pause(600);
        await point(site, site.locator('main h1').first(), { hold: 1800 });
        const mdnRule = dt.locator('.styles-section').nth(1);
        await point(dt, mdnRule.locator('.webkit-css-property', { hasText: 'font-size' }).first(), { hold: 5000 });
      },
    },
    {
      id: 'console',
      say: "Le troisième langage, maintenant. L'onglet Console exécute du JavaScript dans la page. J'efface d'abord les messages que la page y a laissés. Puis je tape : document point querySelector, h1, point textContent, égale, Modifié par JavaScript. Entrée : le titre change encore.",
      run: async ({ dt, site, click, point, pause }) => {
        await pause(300);
        await click(dt, dt.getByRole('tab', { name: 'Console' }), { hold: 1200 });
        await click(dt, dt.locator('devtools-button[aria-label="Clear console"]').first(), { hold: 800 });
        await click(dt, dt.locator('#console-prompt'), { hold: 400 });
        await typeSlow(dt, "document.querySelector('h1').textContent = 'Modifié par JavaScript'", 45);
        await pause(500);
        await dt.keyboard.press('Enter');
        await pause(700);
        await point(site, site.locator('main h1').first(), { hold: 2500 });
      },
    },
    {
      id: 'recharger',
      say: "Et maintenant, je recharge la page. Tout est revenu : le texte, la couleur, la taille. Ces retouches n'ont vécu que dans mon navigateur, sur sa copie de la page : le serveur de MDN n'a rien vu. L'inspecteur sert à essayer, pas à enregistrer.",
      run: async ({ site, reload, point, pause }) => {
        await pause(800);
        await reload();
        await pause(1200);
        await point(site, site.locator('main h1').first(), { hold: 3000 });
      },
    },
    {
      id: 'outro',
      say: "La suite de l'étape refait l'expérience sur une page à vous, en trois fichiers, et vous en retirez le CSS, puis le JavaScript, pour voir ce que chacun apporte. À vous de jouer !",
      run: async ({ moveTo, pause }) => { await pause(1000); await moveTo(320, 400, 800); await pause(2000); },
    },
  ],
};
