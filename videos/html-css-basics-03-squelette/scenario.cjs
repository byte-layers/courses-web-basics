/**
 * Live coding « Écrire le squelette d'une page, et casser ses accents »
 * (lab html-css-basics, étape 03). VS Code et navigateur (moteur byte-layers-videos).
 *
 * Le squelette est tapé ligne à ligne, aides de VS Code coupées : ce qui est
 * tapé est exactement le fichier. Sans charset, le Chromium de Playwright
 * devine l'UTF-8 pour un fichier ouvert depuis le disque : la vidéo montre que
 * les accents tiennent ici, et dit qu'ailleurs ils cassent (comme le lab).
 */
const { stepFiles } = require('../lab-files.cjs');
const DIR = 'byte-layers/web/basics';
const URL = (home) => `file://${home}/${DIR}/premiere-page.html`;

module.exports = {
  name: 'html-css-basics-03-squelette',
  recorder: 'vscode',
  title: 'Les bases HTML et CSS',
  subtitle: '03 · Le squelette d’une page',
  folder: DIR,
  files: stepFiles(3),
  segments: [
    {
      id: 'intro',
      say: "Bienvenue dans ce live coding Byte Layers. Étape 3 du lab : écrire le squelette d'une page à la main, sans rien copier, puis voir ce que protège la ligne charset. Dans le dossier basics, il y a déjà la page de l'étape 2.",
      run: async ({ win, point, pause }) => {
        await pause(1500);
        await point(win.locator('.explorer-folders-view .monaco-list-row').first(), { hold: 2500 });
      },
    },
    {
      id: 'fichier',
      say: "Je crée le fichier premiere-page point html. Ligne 1, le doctype : point d'exclamation DOCTYPE html. Rien avant, pas même une ligne vide. Puis la balise html, avec la langue de la page : lang égale fr.",
      run: async ({ newFile, typeCode, pause }) => {
        await newFile('premiere-page.html');
        await pause(600);
        await typeCode('<!DOCTYPE html>\n<html lang="fr">\n', { delay: 70 });
      },
    },
    {
      id: 'head',
      say: "Le head, l'en-tête. D'abord l'encodage : meta charset égale utf-8. Puis le title, Mon premier site. Ce texte doit être différent du titre de la page : on va voir pourquoi.",
      run: async ({ typeCode, pause }) => {
        await pause(300);
        await typeCode('<head>\n  <meta charset="utf-8">\n  <title>Mon premier site</title>\n</head>\n', { delay: 65 });
      },
    },
    {
      id: 'body',
      say: "Le body, ce qui s'affiche. Un h1, exactement Ma première page. Puis un paragraphe qui me présente, en une phrase, avec des accents. Je ferme le body, puis le html. Le rond sur l'onglet : le fichier n'est pas enregistré. Commande S.",
      run: async ({ win, typeCode, point, key, pause }) => {
        await pause(300);
        await typeCode("<body>\n  <h1>Ma première page</h1>\n  <p>Bonjour ! J'apprends à créer des pages web, et c'est ma première.</p>\n</body>\n</html>", { delay: 50 });
        await pause(500);
        await point(win.locator('.tab.active').first(), { hold: 1500 });
        await key('Meta+S');
        await pause(800);
      },
    },
    {
      id: 'navigateur',
      scene: 'browser',
      say: "J'ouvre la page dans le navigateur, comme à l'étape précédente. Deux textes, à deux endroits. L'onglet affiche le title : Mon premier site. La page affiche le h1, en grand : Ma première page.",
      run: async ({ bar, site, home, open, point, pause }) => {
        await open(URL(home));
        await pause(2500);
        await point(bar.locator('#tab'), { hold: 3000 });
        await point(site.locator('h1'), { hold: 3000 });
      },
    },
    {
      id: 'retirer',
      say: "Maintenant, je retire la ligne charset. Le curseur sur la ligne 4, Commande Maj K supprime la ligne. J'enregistre.",
      run: async ({ win, goLine, line, point, key, pause }) => {
        await pause(400);
        await goLine(4);
        await point(line(4), { hold: 1500 });
        await key('Meta+Shift+K');
        await pause(900);
        await key('Meta+S');
        await pause(700);
        await point(win.locator('.tab.active').first(), { hold: 800 });
      },
    },
    {
      id: 'recharger',
      scene: 'browser',
      say: "Je recharge la page. Ici, les accents tiennent : Chrome a deviné le bon encodage, pour un fichier ouvert depuis le disque. Ce n'est pas toujours le cas. Ailleurs, première s'affiche avec deux caractères bizarres à la place du è, et un serveur peut annoncer un autre encodage que celui du fichier. On ne compte pas sur la devinette.",
      run: async ({ site, reload, point, pause }) => {
        await pause(500);
        await reload();
        await pause(1200);
        await point(site.locator('h1'), { hold: 4000 });
        await point(site.locator('p'), { hold: 3000 });
      },
    },
    {
      id: 'remettre',
      say: "Je remets la ligne, au début du head : meta charset égale utf-8. J'enregistre. Le squelette est complet, et le bouton Verify de l'étape le contrôle. À vous de jouer !",
      run: async ({ win, goLine, line, typeCode, point, key, pause }) => {
        await pause(400);
        await goLine(4);
        await typeCode('  <meta charset="utf-8">\n', { delay: 60 });
        await pause(500);
        await point(line(4), { hold: 1500 });
        await key('Meta+S');
        await pause(700);
        await point(win.locator('.tab.active').first(), { hold: 1500 });
      },
    },
  ],
};
