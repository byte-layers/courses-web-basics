/**
 * Le dossier ~/byte-layers/web/basics du lab html-css-basics, tel qu'il est
 * au début de chaque étape : les fichiers des étapes précédentes, écrits
 * comme leurs solutions. Les scénarios de VS Code le posent avant de filmer
 * (`files: stepFiles(n)`), pour que l'explorateur montre un vrai parcours.
 */
const DIR = 'byte-layers/web/basics';

const NOTES = 'page=200\nintrouvable=404\nredirection=301\nrequetes=74\n';

const TROIS_HTML = `<!DOCTYPE html>
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
const TROIS_CSS = `#bouton {
  background-color: rgb(219, 39, 119);
  color: white;
  border: none;
  padding: 8px 16px;
}
`;
const TROIS_JS = `document.querySelector('#bouton').addEventListener('click', function () {
  document.querySelector('#titre').textContent = 'Merci !';
});
`;

const PREMIERE = `<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Mon premier site</title>
</head>
<body>
  <h1>Ma première page</h1>
  <p>Bonjour ! J'apprends à créer des pages web, et c'est ma première.</p>
</body>
</html>
`;

const VILLE_SVG = `<svg xmlns="http://www.w3.org/2000/svg" width="320" height="160" viewBox="0 0 320 160">
  <rect width="320" height="160" fill="rgb(224, 242, 254)"/>
  <rect x="30" y="70" width="60" height="90" fill="rgb(236, 72, 153)"/>
  <rect x="110" y="40" width="50" height="120" fill="rgb(37, 99, 235)"/>
  <rect x="180" y="90" width="110" height="70" fill="rgb(250, 204, 21)"/>
  <circle cx="270" cy="35" r="18" fill="rgb(250, 204, 21)"/>
</svg>
`;

const VILLE_HTML = `<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Toulouse</title>
</head>
<body>
  <h1>Toulouse</h1>
  <p>Toulouse est la <strong>ville rose</strong>, traversée par la Garonne et le <em>canal du Midi</em>.</p>
  <img src="images/ville.svg" alt="Un dessin de ville : trois immeubles colorés sous un soleil jaune">

  <h2>À voir</h2>
  <ul>
    <li>Le Capitole</li>
    <li>La basilique Saint-Sernin</li>
    <li>Le couvent des Jacobins</li>
  </ul>

  <h2 id="bonnes-adresses">Bonnes adresses</h2>
  <ol>
    <li>Le Bibent</li>
    <li>Chez Émile</li>
    <li>Le Genty Magre</li>
  </ol>

  <p>
    <a href="https://fr.wikipedia.org/wiki/Toulouse" target="_blank" rel="noopener">Toulouse sur Wikipédia</a> ·
    <a href="#bonnes-adresses">Aller aux bonnes adresses</a> ·
    <a href="mailto:contact@exemple.fr">Nous écrire</a>
  </p>
</body>
</html>
`;

const CLUB_DIV = `<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Les Marcheurs du Dimanche</title>
</head>
<body>
  <div>
    <h1>Les Marcheurs du Dimanche</h1>
    <p>Le blog d'un club de randonnée</p>
    <div>
      <ul>
        <li><a href="#">Accueil</a></li>
        <li><a href="#">Nos sorties</a></li>
        <li><a href="#">Nous rejoindre</a></li>
      </ul>
    </div>
  </div>

  <div>
    <h2>Nos derniers récits</h2>
    <div>
      <div>
        <h3>Le pic du Midi par la face nord</h3>
        <p>Départ à 6 h du parking. La montée est raide, mais le panorama récompense l'effort.</p>
      </div>
      <div>
        <h3>Boucle des trois lacs</h3>
        <p>Une sortie familiale de 12 km, accessible aux enfants à partir de huit ans.</p>
      </div>
    </div>

    <div>
      <h3>Le saviez-vous ?</h3>
      <p>Le club organise une sortie chaque dimanche depuis 1987.</p>
    </div>
  </div>

  <div>
    <p>© 2026 Les Marcheurs du Dimanche</p>
  </div>
</body>
</html>
`;

const CLUB_HTML = `<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Les Marcheurs du Dimanche</title>
</head>
<body>
  <header>
    <h1>Les Marcheurs du Dimanche</h1>
    <p>Le blog d'un club de randonnée</p>
    <nav>
      <ul>
        <li><a href="#">Accueil</a></li>
        <li><a href="#">Nos sorties</a></li>
        <li><a href="#">Nous rejoindre</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <h2>Nos derniers récits</h2>
    <div>
      <article>
        <h3>Le pic du Midi par la face nord</h3>
        <p>Départ à 6 h du parking. La montée est raide, mais le panorama récompense l'effort.</p>
      </article>
      <article>
        <h3>Boucle des trois lacs</h3>
        <p>Une sortie familiale de 12 km, accessible aux enfants à partir de huit ans.</p>
      </article>
    </div>

    <aside>
      <h3>Le saviez-vous ?</h3>
      <p>Le club organise une sortie chaque dimanche depuis 1987.</p>
    </aside>
  </main>

  <footer>
    <p>© 2026 Les Marcheurs du Dimanche</p>
  </footer>
</body>
</html>
`;

const MEDIA_HTML = `<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Médiathèque des Trois Rivières</title>
  <link rel="stylesheet" href="mediatheque.css">
</head>
<body>
  <header>
    <h1>Médiathèque des Trois Rivières</h1>
    <p>Lire, écouter, emprunter, depuis 1994</p>
  </header>
  <nav>
    <ul>
      <li><a href="#presentation">Bienvenue</a></li>
      <li><a href="#nouveautes">Nouveautés</a></li>
    </ul>
  </nav>
  <main>
    <section id="presentation">
      <h2>Bienvenue</h2>
      <p class="intro">Plus de 40 000 ouvrages et une salle de lecture ouverte à tous.</p>
      <p>L'inscription est gratuite pour les moins de dix-huit ans.</p>
    </section>
    <section id="nouveautes">
      <h2>Nos nouveautés</h2>
      <p class="intro">Une sélection renouvelée chaque mois par l'équipe.</p>
      <ul>
        <li>Le Mur invisible, de Marlen Haushofer</li>
        <li>La Horde du Contrevent, d'Alain Damasio</li>
      </ul>
    </section>
  </main>
  <footer>
    <p>12 rue des Peupliers, Toulouse</p>
  </footer>
</body>
</html>
`;

/** mediatheque.css à la fin de 06.2 (avant la bannière). */
const MEDIA_CSS = `body {
  font-family: system-ui, "Segoe UI", sans-serif;
  line-height: 1.6;
  color: #333;
  background-color: #f7f7f5;
}

h1 {
  color: #14457b;
}

h2 {
  color: #0b6bcb;
  text-align: center;
}

.intro {
  font-weight: bold;
}

#presentation {
  background-color: white;
}

a {
  text-decoration: none;
  color: #0b6bcb;
}

footer {
  text-align: center;
  font-size: 14px;
}
`;

/** Les règles de la bannière (06.3). */
const MEDIA_BANNIERE = `
.banniere {
  background-color: #14457b;
  color: white;
  padding: 30px;
  text-align: center;
}

.banniere h1 {
  color: white;
}
`;

const CARTES_HTML = `<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Médiathèque : nos services</title>
  <link rel="stylesheet" href="cartes.css">
</head>
<body>
  <div class="conteneur">
    <header>
      <h1>Nos services</h1>
    </header>
    <main>
      <div class="carte">
        <h2>Emprunter</h2>
        <p>Jusqu'à dix documents pour trois semaines, renouvelables une fois.</p>
      </div>
      <div class="carte">
        <h2>Travailler sur place</h2>
        <p>Quarante places assises, le wifi gratuit et six postes en accès libre.</p>
      </div>
      <div class="carte carte--mise-en-avant">
        <h2>Ateliers du samedi</h2>
        <p>Lecture pour les tout-petits, initiation à l'informatique, club de lecture.</p>
      </div>
    </main>
  </div>
</body>
</html>
`;

/** cartes.css, la solution de 07.2. */
const CARTES_CSS = `* {
  box-sizing: border-box;
}

body {
  font-family: system-ui, "Segoe UI", sans-serif;
  background-color: #eef1f5;
  margin: 0;
}

.conteneur {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.carte {
  background-color: #fff;
  border: 1px solid #d7dee8;
  padding: 20px;
  margin-bottom: 20px;
}

.carte--mise-en-avant {
  background-color: #e8f1fb;
  border-left: 5px solid #0b6bcb;
}
`;

/** Fichiers présents au début de l'étape n (chemins relatifs à HOME). */
function stepFiles(n) {
  const f = {};
  const put = (name, content) => { f[`${DIR}/${name}`] = content; };
  if (n > 1) put('notes.txt', NOTES);
  if (n > 2) { put('trois-langages.html', TROIS_HTML); put('trois-langages.css', TROIS_CSS); put('trois-langages.js', TROIS_JS); }
  if (n > 3) put('premiere-page.html', PREMIERE);
  if (n > 4) { put('ville.html', VILLE_HTML); put('images/ville.svg', VILLE_SVG); }
  if (n > 5) put('club.html', CLUB_HTML);
  if (n > 6) { put('mediatheque.html', MEDIA_HTML.replace('<header>', '<header class="banniere">')); put('mediatheque.css', MEDIA_CSS + MEDIA_BANNIERE); }
  return f;
}

module.exports = { DIR, stepFiles, VILLE_SVG, TROIS_HTML, PREMIERE, CLUB_DIV, CLUB_HTML, MEDIA_HTML, MEDIA_CSS, MEDIA_BANNIERE, CARTES_HTML, CARTES_CSS };
