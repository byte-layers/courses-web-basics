/**
 * Live coding « Des cartes aérées, et le piège de la largeur » (lab
 * html-css-basics, étape 07). VS Code, navigateur et vrais DevTools.
 *
 * La page fait 860 px de large (dtWidth 420) : plus que les 800 px du
 * conteneur, sinon le piège de la largeur ne se voit pas. cartes.css :
 * règle * lignes 1-3 (voir CARTES_CSS dans ../lab-files.cjs).
 */
const { stepFiles, CARTES_HTML, CARTES_CSS } = require('../lab-files.cjs');
const DIR = 'byte-layers/web/basics';
const URL = (home) => `file://${home}/${DIR}/cartes.html`;

const parts = CARTES_CSS.split('\n\n');
const STAR_BODY = parts[0] + '\n\n' + parts[1] + '\n\n';
const CONTENEUR = parts[2] + '\n\n';
const CARTES = parts[3] + '\n\n' + parts[4];

const save = async (ctx) => { await ctx.pause(300); await ctx.key('Meta+S'); await ctx.pause(700); };
async function reload({ reload, pause }) { await pause(300); await reload(); await pause(1000); }
/** Met la règle * (lignes 1 à 3) en commentaire, marques tapées à la main. */
async function commentStar(ctx) {
  await ctx.goLine('1:1');
  await ctx.type('/* ', 110);
  await ctx.goLine(3);
  await ctx.key('End');
  await ctx.type(' */', 110);
  await ctx.pause(600);
}
/** Retire ces marques. */
async function uncommentStar(ctx) {
  await ctx.goLine('1:1');
  for (let i = 0; i < 3; i++) { await ctx.key('Delete'); await ctx.pause(90); }
  await ctx.goLine(3);
  await ctx.key('End');
  for (let i = 0; i < 3; i++) { await ctx.key('Backspace'); await ctx.pause(90); }
  await ctx.pause(600);
}
/** Sélectionne le div.conteneur dans l'arbre des DevTools, onglet Computed. */
async function inspectConteneur({ dt, click, point }) {
  await click(dt.getByText('conteneur', { exact: true }).first(), { hold: 800 });
  await click(dt.getByRole('tab', { name: 'Computed' }), { hold: 1000 });
}

module.exports = {
  name: 'html-css-basics-07-largeur',
  recorder: 'vscode',
  title: 'Les bases HTML et CSS',
  subtitle: '07 · Le piège de la largeur',
  folder: DIR,
  files: stepFiles(7),
  devtools: true,
  dtWidth: 420,
  segments: [
    {
      id: 'intro',
      say: "Bienvenue dans ce live coding Byte Layers. Dernière étape du lab : transformer trois blocs collés en cartes aérées, voir le modèle de boîte dans l'inspecteur, et mesurer le piège de la largeur.",
      run: async ({ moveTo, pause }) => { await pause(1000); await moveTo(500, 300, 900); },
    },
    {
      id: 'fichiers',
      say: "Je crée cartes point html et je colle la page de l'étape : un conteneur, et trois cartes. La troisième porte deux classes : carte, et une variante, carte tiret tiret mise-en-avant. Puis cartes point css, vide.",
      run: async (ctx) => {
        await ctx.newFile('cartes.html');
        await ctx.paste(CARTES_HTML);
        await ctx.pause(500);
        await ctx.key('Meta+S');
        await ctx.pause(300);
        await ctx.pointLine(22, { hold: 1800 });
        await ctx.newFile('cartes.css');
        await save(ctx);
      },
    },
    {
      id: 'colles',
      scene: 'browser',
      say: "Sans feuille de style, les trois blocs sont collés les uns aux autres.",
      run: async ({ site, home, open, point, pause }) => {
        await open(URL(home));
        await pause(1200);
        await point(site.locator('.carte').nth(1), { hold: 2000 });
      },
    },
    {
      id: 'regles',
      say: "J'écris la feuille. La règle étoile, pour tous les éléments : box-sizing border-box. Le body : une police avec repli, un fond gris bleuté, et margin zéro, qui retire la marge que le navigateur met autour de la page.",
      run: async (ctx) => { await ctx.typeCode(STAR_BODY, { delay: 28, linePause: 150 }); },
    },
    {
      id: 'conteneur',
      say: "Le conteneur : au plus 800 pixels de large, avec max-width. Margin zéro auto : l'espace restant se répartit à gauche et à droite, et le bloc se centre. Et 20 pixels d'espace intérieur.",
      run: async (ctx) => { await ctx.typeCode(CONTENEUR, { delay: 28, linePause: 150 }); },
    },
    {
      id: 'cartes',
      say: "La carte : un fond blanc, une bordure, du padding dedans, et une marge dessous, dehors. La variante ne change que ce qui la distingue : un fond bleuté, et une bordure gauche épaisse. J'enregistre.",
      run: async (ctx) => { await ctx.typeCode(CARTES, { delay: 28, linePause: 150 }); await save(ctx); },
    },
    {
      id: 'aerees',
      scene: 'browser',
      say: "Je recharge : trois cartes blanches, séparées par le gris de la page, et la troisième, bleutée, avec un trait sur son bord gauche seulement.",
      run: async (ctx) => {
        await reload(ctx);
        await ctx.point(ctx.site.locator('.carte').nth(0), { hold: 1500 });
        await ctx.point(ctx.site.locator('.carte').nth(2), { hold: 2000 });
      },
    },
    {
      id: 'boite',
      scene: 'browser',
      say: "J'ouvre l'inspecteur, et je sélectionne le conteneur. L'onglet Computed montre sa boîte en couches : le contenu au centre, puis le padding, la bordure, la marge. Je survole chaque couche : la page la surligne. Le contenu fait 760 pixels, plus 20 de padding de chaque côté : 800.",
      run: async (ctx) => {
        const { dt, openDevtools, point } = ctx;
        await openDevtools();
        await inspectConteneur(ctx);
        for (const [label, hold] of [['margin', 1300], ['border', 1000], ['padding', 1500]]) {
          await point(dt.getByText(label, { exact: true }).first(), { hold });
        }
        await point(dt.getByText(/^760(\.\d+)?\s*×/).first(), { hold: 3000 });
      },
    },
    {
      id: 'commenter',
      say: "Le piège. Je mets la règle étoile en commentaire : barre oblique étoile avant, étoile barre oblique après. Le raccourci Commande barre oblique fait la même chose. J'enregistre.",
      run: async (ctx) => { await commentStar(ctx); await save(ctx); },
    },
    {
      id: 'piege',
      scene: 'browser',
      say: "Je recharge : les cartes ont grandi. Je réinspecte le conteneur : 800 pixels de contenu, et les 40 de padding ajoutés autour. Il mesure 840 pixels. Sans border-box, max-width ne règle que le contenu.",
      run: async (ctx) => {
        await reload(ctx);
        await ctx.point(ctx.site.locator('.carte').nth(0), { hold: 1200 });
        await inspectConteneur(ctx);
        await ctx.point(ctx.dt.getByText(/^800(\.\d+)?\s*×/).first(), { hold: 2000 });
        await ctx.point(ctx.dt.getByText('padding', { exact: true }).first(), { hold: 2200 });
      },
    },
    {
      id: 'retablir',
      say: "Je retire les marques de commentaire, et j'enregistre.",
      run: async (ctx) => { await uncommentStar(ctx); await save(ctx); },
    },
    {
      id: 'revenu',
      scene: 'browser',
      say: "Je recharge : le conteneur revient à 800 pixels. C'est la fin du lab : vous savez écrire une page, lui donner du sens et l'habiller. À vous de jouer !",
      run: async (ctx) => {
        await reload(ctx);
        await inspectConteneur(ctx);
        await ctx.point(ctx.dt.getByText(/^760(\.\d+)?\s*×/).first(), { hold: 3000 });
      },
    },
  ],
};
