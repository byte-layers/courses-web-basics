/**
 * Live coding « Créer une page en trois fichiers »
 * (lab html-css-basics, étape 02, partie 02.2).
 *
 * VS Code d'abord (moteur byte-layers-videos) : créer le dossier dans le
 * terminal, l'ouvrir, créer et coller les trois fichiers, enregistrer ; puis
 * le navigateur : la page ouverte depuis le disque, le bouton rose, le clic.
 * Le Finder ne se filme pas : la vidéo passe du menu « Reveal in Finder » à
 * la page ouverte.
 */
const HTML = `<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Trois langages</title>
  <link rel="stylesheet" href="trois-langages.css">
</head>
<body>
  <h1 id="titre">Bonjour !</h1>
  <p>Cette page parle trois langages.</p>
  <button type="button" id="bouton">Clique-moi</button>
  <script src="trois-langages.js"></script>
</body>
</html>
`;
const CSS = `#bouton {
  background-color: rgb(219, 39, 119);
  color: white;
  border: none;
  padding: 8px 16px;
}
`;
const JS = `document.querySelector('#bouton').addEventListener('click', function () {
  document.querySelector('#titre').textContent = 'Merci !';
});
`;

/** Ligne n (1 = première) de l'éditeur actif. */
const line = (win, n) => win.locator('.editor-group-container.active .view-line').nth(n - 1);

/** Nouveau fichier dans l'explorateur, nom tapé, contenu collé, enregistré. */
async function newFile(ctx, name, content) {
  const { win, click, type, key, paste, pause } = ctx;
  const header = win.locator('.pane-header').filter({ hasText: /basics/i }).first();
  await ctx.point(header, { hold: 500 });
  await click(header.locator('.action-label[aria-label^="New File"]').first(), { hold: 500 });
  await type(name, 70);
  await pause(400);
  await key('Enter');
  await pause(900);
  await paste(content);
  await pause(900);
}

module.exports = {
  name: 'html-css-basics-02-trois-fichiers',
  recorder: 'vscode',
  title: 'Les bases HTML et CSS',
  subtitle: '02 · Une page en trois fichiers',
  segments: [
    {
      id: 'intro',
      say: "Bienvenue dans ce live coding Byte Layers. Dans cette partie de l'étape 2, on crée une page en trois fichiers, un par langage : HTML, CSS et JavaScript. On les écrit dans VS Code, puis on ouvre la page dans le navigateur.",
      run: async ({ moveTo, pause }) => { await pause(800); await moveTo(640, 300, 900); },
    },
    {
      id: 'dossier',
      say: "Les fichiers vont dans le dossier du lab, basics. Il doit exister avant qu'on l'ouvre dans VS Code. Vous l'avez créé à l'étape 1 : avec la commande mkdir, ou tout simplement dans l'explorateur de fichiers, le Finder sur Mac. Ici, je le crée dans un terminal : mkdir tiret p, puis son chemin.",
      run: async ({ win, command, type, key, point, pause }) => {
        await pause(1500);
        await command('View: Toggle Terminal');
        await pause(2500);
        const term = win.locator('.terminal-wrapper .xterm').last();
        await point(term, { hold: 3000 });
        await type('mkdir -p ~/byte-layers/web/basics', 75);
        await pause(500);
        await key('Enter');
        await pause(1500);
      },
    },
    {
      id: 'ouvrir',
      say: "Je l'ouvre dans VS Code : menu Fichier, Ouvrir le dossier, File, Open Folder. La fenêtre part de mon dossier personnel : je complète le chemin, byte-layers, web, basics, et OK. Sur votre machine, c'est la fenêtre de votre système qui s'affiche, mais le chemin est le même. L'explorateur affiche maintenant BASICS, vide pour l'instant.",
      run: async (ctx) => {
        const { command, pause, key, type } = ctx;
        await pause(600);
        await command('File: Open Folder');
        await pause(1200);
        const input = ctx.win.locator('.quick-input-widget input').first();
        await ctx.point(input, { hold: 600 });
        await type('byte-layers/web/basics', 80);
        await pause(1200);
        await ctx.point(ctx.win.locator('.quick-input-widget').getByRole('button', { name: 'OK' }), { hold: 300 });
        await ctx.relaunch('byte-layers/web/basics');
        await ctx.point(ctx.win.locator('.pane-header').filter({ hasText: /basics/i }).first(), { hold: 2000 });
      },
    },
    {
      id: 'html',
      say: "Premier fichier : trois-langages point html. Bouton Nouveau fichier, je tape son nom, Entrée. Je colle le contenu donné dans l'étape. C'est la page. Dans le head, la balise link appelle le fichier CSS. En bas du body, la balise script appelle le fichier JavaScript. Le rond sur l'onglet dit que le fichier n'est pas encore enregistré : Commande S.",
      run: async (ctx) => {
        const { win, point, key, pause } = ctx;
        await newFile(ctx, 'trois-langages.html', HTML);
        await point(line(win, 6), { hold: 3500 });
        await point(line(win, 12), { hold: 3000 });
        await point(win.locator('.tab.active').first(), { hold: 1500 });
        await key('Meta+S');
        await pause(1000);
      },
    },
    {
      id: 'css',
      say: "Deuxième fichier, trois-langages point css. Je colle la règle qui donne au bouton sa couleur rose, et j'enregistre.",
      run: async (ctx) => {
        const { win, point, key, pause } = ctx;
        await newFile(ctx, 'trois-langages.css', CSS);
        await point(line(win, 2), { hold: 1500 });
        await key('Meta+S');
        await pause(800);
      },
    },
    {
      id: 'js',
      say: "Troisième fichier, trois-langages point js : au clic sur le bouton, le titre change. Je colle, j'enregistre. Plus aucun rond sur les onglets : les trois fichiers sont enregistrés, côte à côte dans BASICS.",
      run: async (ctx) => {
        const { win, point, key, pause } = ctx;
        await newFile(ctx, 'trois-langages.js', JS);
        await point(line(win, 1), { hold: 1500 });
        await key('Meta+S');
        await pause(800);
        await point(win.locator('.tabs-container').first(), { hold: 1500 });
        await point(win.locator('.explorer-folders-view .monaco-list-row').filter({ hasText: 'trois-langages.html' }).first(), { hold: 1500 });
      },
    },
    {
      id: 'reveler',
      say: "Pour ouvrir la page dans le navigateur : clic droit sur trois-langages point html, Reveal in Finder, Afficher dans le Finder. Sous Windows, Reveal in File Explorer. Dans le Finder, un double-clic sur le fichier ouvre la page.",
      run: async ({ win, click, point, key, pause }) => {
        const row = win.locator('.explorer-folders-view .monaco-list-row').filter({ hasText: 'trois-langages.html' }).first();
        await click(row, { button: 'right', hold: 900 });
        const item = win.locator('.monaco-menu .action-item').filter({ hasText: /Reveal in Finder/ }).first();
        await point(item, { hold: 4500 });
        await key('Escape');
        await pause(500);
      },
    },
    {
      id: 'page',
      scene: 'browser',
      say: "La page s'ouvre. Regardez la barre d'adresse : elle commence par file, suivi du chemin du fichier sur le disque. Le bouton est rose : le CSS est bien chargé. Je clique : le titre devient Merci ! Le JavaScript marche aussi.",
      run: async ({ site, home, open, point, click, pause }) => {
        await open(`file://${home}/byte-layers/web/basics/trois-langages.html`);
        await pause(1500);
        await point(site.locator('#bouton'), { hold: 5500 });
        await click(site.locator('#bouton'), { hold: 600 });
        await point(site.locator('#titre'), { hold: 2500 });
      },
    },
    {
      id: 'outro',
      scene: 'browser',
      say: "Les trois fichiers sont en place, et le bouton Verify de l'étape le contrôle. Ensuite, vous retirerez le CSS, puis le JavaScript, pour voir ce que chacun apporte. À vous de jouer !",
      run: async ({ moveTo, pause }) => { await pause(800); await moveTo(640, 500, 800); await pause(1500); },
    },
  ],
};
