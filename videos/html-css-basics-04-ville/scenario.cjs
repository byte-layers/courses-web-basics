/**
 * Live coding « La fiche d'une ville : texte, listes, liens et image »
 * (lab html-css-basics, étape 04). VS Code et navigateur (../record-vscode.cjs).
 *
 * La fenêtre du navigateur est basse (siteHeight), pour que le lien interne
 * fasse défiler la page, comme le lab le conseille. Numéros de ligne : ceux de
 * ville.html à chaque moment du scénario (voir le plan en commentaire).
 */
const { stepFiles, VILLE_SVG } = require('../lab-files.cjs');
const DIR = 'byte-layers/web/basics';
const URL = (home) => `file://${home}/${DIR}/ville.html`;

// Plan de ville.html : 1-9 squelette, h1 et présentation ; 11-16 « À voir » ;
// 18-23 « Bonnes adresses » ; puis </body></html>. Les liens s'ajoutent après
// la ligne 23, l'image après la ligne 9.
const DEBUT = `<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Toulouse</title>
</head>
<body>`;
const TEXTE = `  <h1>Toulouse</h1>
  <p>Toulouse est la <strong>ville rose</strong>, traversée par la Garonne et le <em>canal du Midi</em>.</p>

`;
const LISTES = `  <h2>À voir</h2>
  <ul>
    <li>Le Capitole</li>
    <li>La basilique Saint-Sernin</li>
    <li>Le couvent des Jacobins</li>
  </ul>

  <h2>Bonnes adresses</h2>
  <ol>
    <li>Le Bibent</li>
    <li>Chez Émile</li>
    <li>Le Genty Magre</li>
  </ol>
</body>
</html>`;
const LIENS = `
  <p>
    <a href="https://fr.wikipedia.org/wiki/Toulouse" target="_blank" rel="noopener">Toulouse sur Wikipédia</a> ·
    <a href="#bonnes-adresses">Aller aux bonnes adresses</a> ·
    <a href="mailto:contact@exemple.fr">Nous écrire</a>
  </p>`;
const IMG = '  <img src="images/ville.svg" alt="Un dessin de ville : trois immeubles colorés sous un soleil jaune">';

/** Va en fin de ligne n et ouvre une ligne dessous. */
async function after(ctx, n) { await ctx.goLine(n); await ctx.key('End'); await ctx.key('Enter'); await ctx.pause(200); }
/** Place le curseur ligne n, colonne c, et sélectionne len caractères. */
async function select(ctx, n, c, len) {
  await ctx.goLine(`${n}:${c}`);
  for (let i = 0; i < len; i++) await ctx.key('Shift+ArrowRight');
  await ctx.pause(300);
}

module.exports = {
  name: 'html-css-basics-04-ville',
  recorder: 'vscode',
  title: 'Les bases HTML et CSS',
  subtitle: '04 · La fiche d’une ville',
  folder: DIR,
  files: stepFiles(4),
  siteHeight: 380,
  segments: [
    {
      id: 'intro',
      say: "Bienvenue dans ce live coding Byte Layers. Étape 4 du lab : la fiche d'une ville, avec du texte, deux listes, trois sortes de liens et une image. Le squelette, on sait l'écrire : cette étape porte sur ce qu'on met dans le body.",
      run: async ({ moveTo, pause }) => { await pause(1000); await moveTo(500, 300, 900); },
    },
    {
      id: 'squelette',
      say: "Je crée ville point html, et j'écris le squelette de l'étape précédente, avec un title à mon goût : Toulouse.",
      run: async (ctx) => {
        await ctx.newFile('ville.html');
        await ctx.typeCode(DEBUT + '\n', { delay: 22, linePause: 120 });
      },
    },
    {
      id: 'texte',
      say: "Dans le body : un h1, le nom de la ville. Puis un paragraphe de présentation, avec un mot en strong, mis en valeur, et un autre en em, accentué.",
      run: async (ctx) => {
        await ctx.typeCode(TEXTE, { delay: 40 });
      },
    },
    {
      id: 'listes',
      say: "Un h2, À voir, suivi d'une liste à puces : ul, et un li par monument. Puis un h2, Bonnes adresses, suivi d'une liste numérotée : ol, et trois restaurants. Je ferme le body et le html, et j'enregistre.",
      run: async (ctx) => {
        await ctx.typeCode(LISTES, { delay: 30, linePause: 150 });
        await ctx.pause(400);
        await ctx.key('Meta+S');
        await ctx.pause(700);
      },
    },
    {
      id: 'voir',
      scene: 'browser',
      say: "Dans le navigateur. Le gras pour strong, l'italique pour em. Les puces de la liste ul, et les numéros de la liste ol : je ne les ai pas tapés, le navigateur les calcule.",
      run: async ({ site, home, open, point, pause }) => {
        await open(URL(home));
        await pause(1500);
        await point(site.locator('strong'), { hold: 1500 });
        await point(site.locator('em'), { hold: 1800 });
        await point(site.locator('ul li').first(), { hold: 1800 });
        await point(site.locator('ol li').first(), { hold: 2500 });
      },
    },
    {
      id: 'inserer',
      say: "L'essai qui montre l'intérêt de ol : j'insère un restaurant entre le premier et le deuxième. J'enregistre.",
      run: async (ctx) => {
        await after(ctx, 20);
        await ctx.typeCode('    <li>Le Michel Sarran</li>', { delay: 45 });
        await ctx.pause(400);
        await ctx.key('Meta+S');
        await ctx.pause(600);
      },
    },
    {
      id: 'renumeroter',
      scene: 'browser',
      say: "Je recharge : les numéros se sont recalculés tout seuls. Tapés à la main, il aurait fallu tous les corriger.",
      run: async ({ site, reload, point, pause }) => {
        await pause(300);
        await reload();
        await pause(900);
        await point(site.locator('ol li').nth(1), { hold: 2000 });
        await point(site.locator('ol li').nth(3), { hold: 2000 });
      },
    },
    {
      id: 'liens',
      say: "Je retire ce quatrième restaurant : Commande Maj K. Sous les listes, un paragraphe avec trois liens. Un lien externe, vers Wikipédia, dans un nouvel onglet : target égale underscore blank, et rel égale noopener. Un lien interne, vers le titre Bonnes adresses : href égale dièse bonnes-adresses. Et un lien e-mail, mailto. J'enregistre.",
      run: async (ctx) => {
        await ctx.goLine(21);
        await ctx.pointLine(21, { hold: 800 });
        await ctx.key('Meta+Shift+K');
        await ctx.pause(700);
        await after(ctx, 23);
        await ctx.typeCode(LIENS.slice(1), { delay: 28, linePause: 200 });
        await ctx.pause(500);
        await ctx.key('Meta+S');
        await ctx.pause(600);
      },
    },
    {
      id: 'piege',
      scene: 'browser',
      say: "Ma fenêtre est basse, pour que la page défile. Je recharge, et je clique sur le lien interne. Rien ne se passe : le lien vise un id qui n'existe encore nulle part. C'est le piège du bit.",
      run: async ({ site, reload, click, pause }) => {
        await pause(300);
        await reload();
        await pause(800);
        await site.mouse.wheel(0, 600);
        await pause(800);
        await click(site.locator('a[href="#bonnes-adresses"]'), { hold: 2500 });
      },
    },
    {
      id: 'id',
      say: "Dans la balise ouvrante du h2 Bonnes adresses, j'ajoute id égale bonnes-adresses. J'enregistre.",
      run: async (ctx) => {
        await ctx.goLine('18:6');
                await ctx.type(' id="bonnes-adresses"', 60);
        await ctx.pause(400);
        await ctx.key('Meta+S');
        await ctx.pause(600);
      },
    },
    {
      id: 'saut',
      scene: 'browser',
      say: "Je recharge, et je reclique : la page saute jusqu'au titre, et l'adresse se termine par dièse bonnes-adresses.",
      run: async ({ bar, site, reload, click, point, pause }) => {
        await pause(300);
        await reload();
        await pause(800);
        await site.mouse.wheel(0, 600);
        await pause(800);
        await click(site.locator('a[href="#bonnes-adresses"]'), { hold: 1500 });
        await point(site.locator('#bonnes-adresses'), { hold: 1500 });
        await point(bar.locator('#url'), { hold: 2000 });
      },
    },
    {
      id: 'dossier',
      say: "Maintenant, l'image. On range les images à part : je survole BASICS, icône Nouveau dossier, images. Dedans, un fichier ville point svg, où je colle le dessin donné dans l'étape : une image écrite en texte. J'enregistre.",
      run: async (ctx) => {
        await ctx.newFolder('images');
        await ctx.pause(400);
        await ctx.newFile('ville.svg');
        await ctx.paste(VILLE_SVG);
        await ctx.pause(700);
        await ctx.key('Meta+S');
        await ctx.pause(600);
      },
    },
    {
      id: 'img',
      say: "Retour dans ville point html. Sous la présentation, une balise img. Son src part du dossier de la page : images, slash, ville point svg. Et un texte alternatif, alt, qui décrit ce que montre l'image. J'enregistre.",
      run: async (ctx) => {
        await ctx.openFile('ville.html');
        await after(ctx, 9);
        await ctx.typeCode(IMG, { delay: 32 });
        await ctx.pause(400);
        await ctx.key('Meta+S');
        await ctx.pause(600);
      },
    },
    {
      id: 'dessin',
      scene: 'browser',
      say: "Je recharge, et je remonte en haut : le dessin de ville s'affiche sous la présentation.",
      run: async ({ site, reload, point, pause }) => {
        await pause(300);
        await reload();
        await pause(1000);
        await point(site.locator('img'), { hold: 2500 });
      },
    },
    {
      id: 'essai1',
      say: "Premier essai : j'écris photo à la place de ville dans le chemin, j'enregistre.",
      run: async (ctx) => {
        await select(ctx, 10, 20, 5);
        await ctx.type('photo', 90);
        await ctx.pause(400);
        await ctx.key('Meta+S');
        await ctx.pause(600);
      },
    },
    {
      id: 'alt',
      scene: 'browser',
      say: "Je recharge : l'image a disparu, et le texte alternatif s'affiche à sa place. C'est ce que voit un visiteur dont la connexion a échoué, et ce que lit un lecteur d'écran.",
      run: async ({ site, reload, point, pause }) => {
        await pause(300);
        await reload();
        await pause(1000);
        await point(site.locator('img'), { hold: 3500 });
      },
    },
    {
      id: 'essai2',
      say: "Je remets ville. Deuxième essai : images avec une majuscule, I majuscule. J'enregistre.",
      run: async (ctx) => {
        await select(ctx, 10, 20, 5);
        await ctx.type('ville', 90);
        await ctx.pause(700);
        await select(ctx, 10, 13, 1);
        await ctx.type('I', 90);
        await ctx.pause(400);
        await ctx.key('Meta+S');
        await ctx.pause(600);
      },
    },
    {
      id: 'casse',
      scene: 'browser',
      say: "Je recharge : sur Mac, l'image s'affiche quand même, parce que le disque ignore la casse. Sur un serveur Linux, elle disparaîtrait : le bouton Verify de l'étape se comporte comme lui, et échoue avec ce chemin.",
      run: async ({ site, reload, point, pause }) => {
        await pause(300);
        await reload();
        await pause(1000);
        await point(site.locator('img'), { hold: 3500 });
      },
    },
    {
      id: 'outro',
      say: "Je remets la minuscule, et j'enregistre. La fiche a ses listes, ses trois liens et son image, avec un chemin exact. À vous de jouer !",
      run: async (ctx) => {
        await select(ctx, 10, 13, 1);
        await ctx.type('i', 90);
        await ctx.pause(600);
        await ctx.pointLine(10, { hold: 1200 });
        await ctx.key('Meta+S');
        await ctx.pause(1000);
      },
    },
  ],
};
