/**
 * Live coding « Habiller une page en CSS, puis poser ses propres accroches »
 * (lab html-css-basics, étape 06). VS Code, navigateur et vrais DevTools
 * (devtools: true) pour le panneau Styles.
 *
 * Numéros de ligne de mediatheque.css : body 1-6, h1 8-10 (color ligne 9),
 * h2 12-15, .intro 17-19, #presentation 21-23, a 25-28, footer 30-33.
 * mediatheque.html : <header> ligne 9, son « > » en colonne 10.
 */
const { stepFiles, MEDIA_HTML, MEDIA_CSS, MEDIA_BANNIERE } = require('../lab-files.cjs');
const DIR = 'byte-layers/web/basics';
const URL = (home) => `file://${home}/${DIR}/mediatheque.html`;

// La feuille, découpée comme dans la vidéo : body, titres, classe et id, liens et pied.
const parts = MEDIA_CSS.split('\n\n');
const BODY = parts[0] + '\n\n';
const TITRES = parts[1] + '\n\n' + parts[2] + '\n\n';
const ACCROCHES = parts[3] + '\n\n' + parts[4] + '\n\n';
const FIN = parts[5] + '\n\n' + parts[6];
const [BAN, BAN_H1] = MEDIA_BANNIERE.trim().split('\n\n');

async function select(ctx, n, c, len) {
  await ctx.goLine(`${n}:${c}`);
  for (let i = 0; i < len; i++) await ctx.key('Shift+ArrowRight');
  await ctx.pause(300);
}
const save = async (ctx) => { await ctx.pause(300); await ctx.key('Meta+S'); await ctx.pause(700); };
/** Outil « Select an element » des DevTools, puis clic sur l'élément de la page. */
async function inspect({ dt, click }, locator, hold = 1200) {
  await click(dt.getByRole('button', { name: /Select an element/ }).first(), { hold: 400 });
  await click(locator, { hold });
}
/** Recharge la page, après un temps. */
async function reload({ reload, pause }) { await pause(300); await reload(); await pause(900); }

module.exports = {
  name: 'html-css-basics-06-css',
  recorder: 'vscode',
  title: 'Les bases HTML et CSS',
  subtitle: '06 · Habiller une page en CSS',
  folder: DIR,
  files: stepFiles(6),
  devtools: true,
  segments: [
    {
      id: 'intro',
      say: "Bienvenue dans ce live coding Byte Layers. Étape 6 du lab : habiller en CSS la page d'une médiathèque, lire ses règles dans l'inspecteur, puis créer soi-même une accroche, une classe, quand le HTML n'en offre pas.",
      run: async ({ moveTo, pause }) => { await pause(1000); await moveTo(500, 300, 900); },
    },
    {
      id: 'fichiers',
      say: "Je crée mediatheque point html, et je colle la page donnée par l'étape. Sa balise link cite une feuille, mediatheque point css. Je crée ce fichier à côté, vide pour l'instant.",
      run: async (ctx) => {
        await ctx.newFile('mediatheque.html');
        await ctx.paste(MEDIA_HTML);
        await ctx.pause(500);
        await ctx.key('Meta+S');
        await ctx.pause(300);
        await ctx.pointLine(6, { hold: 1500 });
        await ctx.newFile('mediatheque.css');
        await save(ctx);
      },
    },
    {
      id: 'defaut',
      scene: 'browser',
      say: "Dans le navigateur, la page a l'apparence par défaut : une police à empattements, des liens bleus soulignés.",
      run: async ({ site, home, open, point, pause }) => {
        await open(URL(home));
        await pause(1200);
        await point(site.locator('h1'), { hold: 1500 });
        await point(site.locator('nav a').first(), { hold: 1800 });
      },
    },
    {
      id: 'body',
      say: "Première règle, body. Une police sans empattements, avec des replis : si system-ui manque, Segoe UI, et en dernier recours, n'importe quelle sans-serif. Un interligne de 1,6. Un texte gris foncé sur un fond presque blanc.",
      run: async (ctx) => { await ctx.typeCode(BODY, { delay: 30, linePause: 150 }); await save(ctx); },
    },
    {
      id: 'police',
      scene: 'browser',
      say: "Je recharge : toute la page change de police, parce que le texte hérite de la police du body.",
      run: async (ctx) => { await reload(ctx); await ctx.point(ctx.site.locator('p').first(), { hold: 2200 }); },
    },
    {
      id: 'titres',
      say: "Les titres : h1 en bleu foncé, h2 en bleu plus vif, et centré. Puis la classe intro, avec un point devant : en gras. Et l'id presentation, avec un dièse : un fond blanc.",
      run: async (ctx) => { await ctx.typeCode(TITRES + ACCROCHES, { delay: 30, linePause: 150 }); await save(ctx); },
    },
    {
      id: 'classe',
      scene: 'browser',
      say: "Je recharge. Les deux paragraphes intro passent en gras. Mais seule la section Bienvenue a un fond blanc : une classe vise tous les éléments qui la portent, un id un seul.",
      run: async (ctx) => {
        await reload(ctx);
        await ctx.point(ctx.site.locator('.intro').nth(0), { hold: 1300 });
        await ctx.point(ctx.site.locator('.intro').nth(1), { hold: 1500 });
        await ctx.point(ctx.site.locator('#presentation h2'), { hold: 2000 });
      },
    },
    {
      id: 'liens',
      say: "Les liens, sans soulignement et en bleu. Le pied de page, centré, en 14 pixels. J'enregistre.",
      run: async (ctx) => { await ctx.typeCode(FIN, { delay: 30, linePause: 150 }); await save(ctx); },
    },
    {
      id: 'styles',
      scene: 'browser',
      say: "Je recharge, et j'ouvre l'inspecteur sur un paragraphe en gras. Le panneau Styles liste les règles qui s'appliquent : ma règle intro, avec le fichier et le numéro de ligne. Et plus bas, Inherited from body : la police vient du body.",
      run: async (ctx) => {
        const { site, dt, point, openDevtools } = ctx;
        await reload(ctx);
        await openDevtools();
        await inspect(ctx, site.locator('.intro').first());
        await point(dt.getByText('.intro', { exact: true }).first(), { hold: 2000 });
        await point(dt.getByText(/mediatheque\.css:\d+/).first(), { hold: 1500 });
        await point(dt.getByText(/Inherited from/).first(), { hold: 2500 });
      },
    },
    {
      id: 'faute',
      say: "Une faute exprès, dans la règle h1 : colr au lieu de color. J'enregistre.",
      run: async (ctx) => {
        await select(ctx, 9, 3, 5);
        await ctx.type('colr', 90);
        await save(ctx);
      },
    },
    {
      id: 'barree',
      scene: 'browser',
      say: "Je recharge, et j'inspecte le titre : la déclaration est barrée, avec un triangle d'avertissement. Le navigateur ne connaît pas cette propriété, il l'ignore sans rien dire à la page.",
      run: async (ctx) => {
        await reload(ctx);
        await inspect(ctx, ctx.site.locator('h1'));
        await ctx.point(ctx.dt.getByText('colr', { exact: true }).first(), { hold: 3000 });
      },
    },
    {
      id: 'corriger',
      say: "Je corrige, et j'enregistre. Maintenant, la bannière. On veut un bandeau bleu foncé pour l'en-tête, et aucune classe ne permet de le viser. Je la crée : dans le HTML, class égale banniere, dans la balise ouvrante du header.",
      run: async (ctx) => {
        await select(ctx, 9, 3, 4);
        await ctx.type('color', 90);
        await save(ctx);
        await ctx.openFile('mediatheque.html');
        await ctx.goLine('9:10');
        await ctx.type(' class="banniere"', 65);
        await save(ctx);
      },
    },
    {
      id: 'banniere',
      say: "Dans le CSS, la règle point banniere : un fond bleu foncé, un texte blanc, 30 pixels d'espace intérieur, texte centré. J'enregistre les deux fichiers.",
      run: async (ctx) => {
        await ctx.openFile('mediatheque.css');
        await ctx.key('Meta+ArrowDown');
        await ctx.key('Enter');
        await ctx.typeCode(BAN + '\n', { delay: 30, linePause: 150 });
        await save(ctx);
      },
    },
    {
      id: 'invisible',
      scene: 'browser',
      say: "Je recharge. Le bandeau est là, mais le titre reste bleu foncé, donc invisible. La règle h1 vise l'élément lui-même : elle l'emporte sur la couleur héritée de la bannière.",
      run: async (ctx) => {
        await reload(ctx);
        await ctx.point(ctx.site.locator('header'), { hold: 1500 });
        await ctx.point(ctx.site.locator('h1'), { hold: 2500 });
      },
    },
    {
      id: 'h1',
      say: "J'ajoute une règle point banniere h1 : les h1 à l'intérieur de la bannière, en blanc. J'enregistre.",
      run: async (ctx) => { await ctx.key('Enter'); await ctx.typeCode(BAN_H1 + '\n', { delay: 30, linePause: 150 }); await save(ctx); },
    },
    {
      id: 'blanc',
      scene: 'browser',
      say: "Je recharge : le titre est blanc sur le bandeau.",
      run: async (ctx) => { await reload(ctx); await ctx.point(ctx.site.locator('h1'), { hold: 2000 }); },
    },
    {
      id: 'typo',
      say: "Dernier essai, la panne la plus fréquente : dans le HTML, banniere avec un seul n. J'enregistre.",
      run: async (ctx) => {
        await ctx.openFile('mediatheque.html');
        await ctx.goLine('9:21');
        await ctx.pause(300);
        await ctx.key('Delete');
        await save(ctx);
      },
    },
    {
      id: 'disparu',
      scene: 'browser',
      say: "Je recharge : le bandeau a disparu, sans aucun message. Les deux fichiers sont valides, ils ne se parlent plus. J'inspecte l'en-tête : la règle banniere n'est plus dans le panneau Styles.",
      run: async (ctx) => {
        await reload(ctx);
        await ctx.point(ctx.site.locator('header'), { hold: 1500 });
        await inspect(ctx, ctx.site.locator('header p'), 600);
        await ctx.click(ctx.dt.getByText('header', { exact: true }).first(), { hold: 2500 });
      },
    },
    {
      id: 'outro',
      say: "Je remets le bon nom, et j'enregistre. Une classe se crée des deux côtés, avec le même nom. À vous de jouer !",
      run: async (ctx) => {
        await ctx.goLine('9:20');
        await ctx.type('n', 120);
        await ctx.pause(400);
        await ctx.pointLine(9, { hold: 1200 });
        await save(ctx);
        await ctx.pause(600);
      },
    },
  ],
};
