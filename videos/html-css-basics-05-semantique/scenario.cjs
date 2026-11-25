/**
 * Live coding « Ranger une page en balises sémantiques, et voir son plan »
 * (lab html-css-basics, étape 05). VS Code, navigateur et vrais DevTools à
 * droite (devtools: true) pour l'arbre d'accessibilité.
 *
 * Numéros de ligne : ceux de club.html (voir CLUB_DIV dans ../lab-files.cjs).
 * Chaque remplacement sélectionne le mot div (colonne exacte) et le retape.
 */
const { stepFiles, CLUB_DIV } = require('../lab-files.cjs');
const DIR = 'byte-layers/web/basics';
const URL = (home) => `file://${home}/${DIR}/club.html`;

/** Ligne n, colonne c : sélectionne « div » et tape le nouveau nom. */
async function swap(ctx, n, c, name) {
  await ctx.goLine(`${n}:${c}`);
  for (let i = 0; i < 3; i++) await ctx.key('Shift+ArrowRight');
  await ctx.pause(350);
  await ctx.type(name, 75);
  await ctx.pause(450);
}
const save = async (ctx) => { await ctx.pause(300); await ctx.key('Meta+S'); await ctx.pause(700); };

module.exports = {
  name: 'html-css-basics-05-semantique',
  recorder: 'vscode',
  title: 'Les bases HTML et CSS',
  subtitle: '05 · Les balises sémantiques',
  folder: DIR,
  files: stepFiles(5),
  devtools: true,
  segments: [
    {
      id: 'intro',
      say: "Bienvenue dans ce live coding Byte Layers. Étape 5 du lab : ranger une page en balises sémantiques. À l'écran, rien ne change. Mais les outils de développement montrent le plan que le navigateur construit, et ce plan, lui, change.",
      run: async ({ moveTo, pause }) => { await pause(1000); await moveTo(500, 300, 900); },
    },
    {
      id: 'creer',
      say: "Je crée club point html, et je colle la page donnée par l'étape : le blog d'un club de randonnée, construit entièrement en div. J'enregistre.",
      run: async (ctx) => {
        await ctx.newFile('club.html');
        await ctx.paste(CLUB_DIV);
        await ctx.pause(600);
        await ctx.key('Meta+S');
        await ctx.pause(400);
        await ctx.key('Meta+ArrowUp');
        await ctx.pause(1500);
      },
    },
    {
      id: 'avant',
      scene: 'browser',
      say: "J'ouvre la page, et les outils de développement. Dans l'onglet Elements, le volet Accessibility, et l'interrupteur Show accessibility tree : à la place du code, le plan que lit un lecteur d'écran. Des titres, heading. Un paragraphe, une liste. Mais aucune zone : les huit div ne produisent rien.",
      run: async ({ site, dt, home, open, openDevtools, point, click, pause }) => {
        await open(URL(home));
        await pause(800);
        await openDevtools();
        await pause(600);
        await click(dt.getByRole('tab', { name: 'Accessibility' }), { hold: 800 });
        await click(dt.getByRole('switch', { name: /accessibility tree/i }).or(dt.getByRole('checkbox', { name: /accessibility tree/i })).first(), { hold: 1800 });
        await point(dt.getByText('heading', { exact: true }).first(), { hold: 1800 });
        await point(dt.getByText('paragraph', { exact: true }).first(), { hold: 1300 });
        await point(dt.getByText('list', { exact: true }).first(), { hold: 2500 });
      },
    },
    {
      id: 'header',
      say: "Retour dans le code. Le premier bloc, le nom du club avec son menu, devient header. Je descends jusqu'à sa balise fermante, que l'indentation aide à trouver. Mais d'abord, le bloc du menu, à l'intérieur : nav, et sa fermante, nav. Puis la fermante du header. J'enregistre.",
      run: async (ctx) => {
        await swap(ctx, 8, 4, 'header');
        await ctx.pointLine(18, { hold: 900 });
        await swap(ctx, 11, 6, 'nav');
        await swap(ctx, 17, 7, 'nav');
        await swap(ctx, 18, 5, 'header');
        await save(ctx);
      },
    },
    {
      id: 'pareil',
      scene: 'browser',
      say: "Je recharge : la page n'a pas bougé d'un pixel. Si quelque chose s'était déplacé, une ouvrante et sa fermante ne se correspondraient plus.",
      run: async ({ site, reload, point, pause }) => {
        await pause(300);
        await reload();
        await pause(900);
        await point(site.locator('h1'), { hold: 1800 });
        await point(site.locator('ul'), { hold: 1800 });
      },
    },
    {
      id: 'main',
      say: "Le bloc suivant contient tout le contenu : main. Les deux récits deviennent deux article. Le div qui les groupe reste un div : c'est le seul, il servira à la mise en page. L'encadré, Le saviez-vous, devient aside. Et la fermante du main. J'enregistre.",
      run: async (ctx) => {
        await swap(ctx, 20, 4, 'main');
        await swap(ctx, 23, 8, 'article');
        await swap(ctx, 26, 9, 'article');
        await swap(ctx, 27, 8, 'article');
        await swap(ctx, 30, 9, 'article');
        await ctx.pointLine(22, { hold: 1500 });
        await swap(ctx, 33, 6, 'aside');
        await swap(ctx, 36, 7, 'aside');
        await swap(ctx, 37, 5, 'main');
        await save(ctx);
      },
    },
    {
      id: 'footer',
      say: "Dernier bloc, le copyright : footer. J'enregistre.",
      run: async (ctx) => {
        await swap(ctx, 39, 4, 'footer');
        await swap(ctx, 41, 5, 'footer');
        await save(ctx);
      },
    },
    {
      id: 'apres',
      scene: 'browser',
      say: "Je recharge. À l'écran, toujours rien de changé. Dans l'arbre, de nouvelles zones : banner pour le header, navigation, main, deux article, complementary pour l'aside, et contentinfo pour le footer. C'est le plan qu'un lecteur d'écran propose pour sauter directement au menu, ou au contenu principal.",
      run: async ({ dt, reload, point, pause }) => {
        await pause(300);
        await reload();
        await pause(2000);
        for (const [role, hold] of [['banner', 1500], ['navigation', 1300], ['main', 1300], ['article', 1300], ['complementary', 1500], ['contentinfo', 2000]]) {
          await point(dt.getByText(role, { exact: true }).first(), { hold });
        }
      },
    },
    {
      id: 'outro',
      say: "Six balises qui nomment leurs zones, un seul div, et une page identique à l'œil. Le bouton Verify de l'étape compte les balises. À vous de jouer !",
      run: async (ctx) => {
        await ctx.key('Meta+ArrowUp');
        await ctx.pause(600);
        await ctx.pointLine(8, { hold: 1200 });
        await ctx.pointLine(20, { hold: 1200 });
        await ctx.pointLine(22, { hold: 1500 });
      },
    },
  ],
};
