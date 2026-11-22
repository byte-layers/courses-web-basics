---
title: "Bootstrap : des classes CSS toutes faites"
description: "Un framework CSS est une feuille de style déjà écrite, qu'on utilise par ses classes : charger Bootstrap depuis un CDN, sa grille container, row et col, ses composants, ce qu'il fait à votre place (Flexbox, media queries, un style cohérent) et ce qu'il ne fait pas (le sens, les alt, les étiquettes)."
tags:
  - bit
  - css
difficulty: beginner
duration: 15
requires: "0.9.0"
---

Un **framework CSS** comme **Bootstrap** est une feuille de style déjà écrite, que l'on utilise en ajoutant ses **classes** au HTML. Vous saurez le charger, disposer une page avec sa grille, utiliser ses composants, et surtout reconnaître ce qu'il fait à votre place, parce que vous venez de l'écrire à la main, et ce qu'il ne fait pas.

**Prérequis** : les bits [Flexbox](https://byte-layers.com/fr/bits/flexbox), [Le responsive design](https://byte-layers.com/fr/bits/responsive-design) et [L'accessibilité web](https://byte-layers.com/fr/bits/web-accessibility).

# Bootstrap : des classes CSS toutes faites

Un entête en Flexbox, une grille qui passe de trois colonnes à une, des boutons avec un survol : vous savez maintenant écrire tout cela. Une équipe qui veut aller vite, ou garder le même style sur cinquante pages, prend souvent un framework qui l'a déjà écrit.

## Un framework CSS : une feuille de style qu'on utilise par ses classes

Bootstrap est, pour l'essentiel, **un fichier CSS** de quelques milliers de règles, et un fichier JavaScript pour les composants qui réagissent (menus déroulants, fenêtres modales). Vous ne l'écrivez pas et vous ne le modifiez pas : vous ajoutez à vos balises les classes qu'il définit, `btn`, `card`, `row`, et ses règles s'appliquent.

Pour le charger, le plus simple est un **CDN** (*content delivery network*), un serveur public qui distribue des bibliothèques. Une balise `<link>` dans le `head` suffit, avec une **version précise** dans l'adresse, pour que la page ne change pas toute seule le jour où sort une version suivante :

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css">
```

Ce fichier pèse environ `230 Ko`, `30 Ko` une fois compressé pour le transfert. Le navigateur le télécharge en entier, même si la page n'utilise que trois classes.

## La grille : container, row, col

La grille de Bootstrap tient en trois classes, qu'on imbrique toujours dans cet ordre :

| Classe | Rôle | Ce que c'est en CSS |
|---|---|---|
| `container` | centre le contenu, avec une largeur maximale | `max-width` qui change à chaque point de rupture |
| `row` | une rangée | `display: flex; flex-wrap: wrap;` |
| `col-md-4` | une colonne de 4 douzièmes, à partir de l'écran `md` | `width: 33.33%` dans une media query `min-width: 768px` |

La rangée est découpée en **12 parts** : trois colonnes `col-md-4` la remplissent. Le préfixe `md` est un **point de rupture** : `sm` (576 px), `md` (768 px), `lg` (992 px), `xl` (1200 px). En dessous de `md`, la colonne prend toute la largeur : c'est du mobile-first, avec `min-width`, exactement comme dans le bit sur le responsive design.

**À toi** : charge Bootstrap dans la page avec la balise `<link>` ci-dessus, puis range les trois projets dans un `container`, une `row` et trois colonnes `col-md-4`.

```playground
runtime: web
title: La grille de Bootstrap
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Projets</title>
      <!-- Charge Bootstrap ici -->
    </head>
    <body>
      <main>
        <article>
          <h2>Météo du jour</h2>
          <p>Une page qui affiche la météo de Toulouse.</p>
        </article>
        <article>
          <h2>Quiz Pyrénées</h2>
          <p>Dix questions sur les sommets.</p>
        </article>
        <article>
          <h2>Club de rando</h2>
          <p>Le site du club, avec son formulaire d'inscription.</p>
        </article>
      </main>
    </body>
    </html>
open: [index.html]
verify:
  - label: la page charge la feuille de style de Bootstrap 5.3.8
    file: index.html
    includes: "/<link[^>]+href=[\"']https:\\/\\/cdn\\.jsdelivr\\.net\\/npm\\/bootstrap@5\\.3\\.8\\/dist\\/css\\/bootstrap(\\.min)?\\.css[\"']/"
    hint: "Recopie la balise `<link>` du texte à la place du commentaire, dans le `head`."
  - label: "les trois projets sont dans `container`, `row`, puis `col-md-4`"
    selector: ".container > .row > .col-md-4"
    count: 3
    hint: "`<main class=\"container\">`, puis `<div class=\"row\">` autour des articles, et `class=\"col-md-4\"` sur chaque `article`."
  - label: la rangée est en Flexbox, grâce au CSS de Bootstrap (demande le réseau)
    selector: .row
    style: { display: flex }
    hint: "Si les deux contrôles précédents passent et pas celui-ci, la feuille de Bootstrap ne s'est pas chargée : vérifie l'adresse, ou ta connexion."
solution: assets/grille.solution
```

Rétrécissez l'aperçu sous `768px` : les trois projets s'empilent. Vous n'avez écrit ni Flexbox ni media query, mais elles sont bien là, dans le fichier de Bootstrap.

## Ce que le framework fait à votre place

Bootstrap apporte d'un coup ce qui prend du temps à écrire et à tester :

| Il fournit | Ce que vous écririez sinon |
|---|---|
| une remise à zéro des styles des navigateurs | des marges et des polices qui changent d'un navigateur à l'autre |
| la grille `container`, `row`, `col` | Flexbox, `gap` et une media query par point de rupture |
| des composants : `btn`, `card`, `navbar`, `form-control`, `alert` | des dizaines de règles, leurs états `:hover` et `:focus` |
| des utilitaires : `mt-3`, `text-center`, `d-flex` | une petite règle chaque fois |
| des composants en JavaScript : menu repliable, fenêtre modale | le script et sa gestion du clavier |

Il se personnalise par ses **variables CSS** (`--bs-primary`…) ou en recompilant ses sources Sass, et on ajoute toujours sa propre feuille de style, chargée **après** la sienne, pour ce qui est propre au site.

## Ce qu'il ne fait pas : le sens, les alt, les étiquettes

Une classe Bootstrap change l'**apparence**, jamais le **sens**. Une `div class="h3"` ressemble à un titre, mais ce n'est pas un titre pour un lecteur d'écran ; une image avec `img-fluid` ne déborde plus, mais elle n'a toujours pas de texte alternatif si vous n'en écrivez pas ; un `form-control` est joli, mais son étiquette n'est reliée que si `for` et `id` correspondent. Tout ce que le bit sur l'accessibilité vous a fait vérifier reste à votre charge.

**À toi** : cette carte a l'air parfaite. Pour un lecteur d'écran, elle n'a ni titre ni image décrite. Donne-lui un vrai titre `h3` à la place de la `div class="h5"` (garde la classe pour l'apparence), et décris l'image.

```playground
runtime: web
title: Une carte jolie, et lisible
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Projet</title>
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css">
    </head>
    <body class="p-4">
      <h2>Mes projets</h2>
      <div class="card w-50">
        <img src="club.svg" class="card-img-top img-fluid">
        <div class="card-body">
          <div class="h5 card-title">Club de rando</div>
          <p class="card-text">Le site du club, avec son formulaire d'inscription.</p>
          <a href="#club" class="btn btn-primary">Voir le projet</a>
        </div>
      </div>
    </body>
    </html>
  club.svg: |
    <svg xmlns="http://www.w3.org/2000/svg" width="320" height="140" viewBox="0 0 320 140">
      <rect width="320" height="140" fill="#dbeafe"/>
      <polygon points="0,140 110,40 180,100 230,60 320,140" fill="#1e3a8a"/>
    </svg>
open: [index.html]
verify:
  - label: le titre de la carte est un vrai titre `h3`
    selector: ".card h3"
    text: Club de rando
    hint: "`<h3 class=\"h5 card-title\">Club de rando</h3>` : la balise donne le sens, la classe garde l'apparence."
  - label: l'image de la carte a un texte alternatif
    selector: ".card img"
    attr: { alt: "/\\S/" }
    hint: "`alt=\"…\"` : que montre l'image ?"
solution: assets/carte.solution
```

> 💡 **Remarque.** Avec Bootstrap, toutes les pages finissent par se ressembler un peu, et le navigateur télécharge tout le framework pour quelques classes. Le bit suivant présente une autre approche, qui ne garde que les classes réellement utilisées.

> 📖 [Bootstrap, bien démarrer (en anglais)](https://getbootstrap.com/docs/5.3/getting-started/introduction/) · [La grille de Bootstrap (en anglais)](https://getbootstrap.com/docs/5.3/layout/grid/) · [L'accessibilité selon Bootstrap (en anglais)](https://getbootstrap.com/docs/5.3/getting-started/accessibility/)

## Trois questions pour vérifier

```quiz
title: "Bootstrap"
tracksProgress: false
showNotice: false
place: stage
questions:
  - prompt: "En CSS, que fait la classe `row` de Bootstrap ?"
    answers:
      - "Elle crée un tableau HTML"
      - "Elle met le conteneur en Flexbox, avec passage à la ligne"
      - "Elle ajoute une ligne horizontale"
    correct: 2
    explanation: "`.row` vaut display: flex; flex-wrap: wrap; (plus des marges pour les gouttières) : c'est Flexbox, déjà écrit."
  - prompt: "Que veut dire `col-md-4` ?"
    answers:
      - "4 colonnes de taille moyenne"
      - "4 douzièmes de la largeur, à partir de 768 px ; toute la largeur en dessous"
      - "Une colonne de 4 cm"
    correct: 2
    explanation: "La rangée a 12 parts ; md est le point de rupture de 768 px, en mobile-first."
  - prompt: "Une page faite avec Bootstrap est-elle accessible ?"
    answers:
      - "Oui, Bootstrap s'en charge"
      - "Pas forcément : les alt, les vrais titres et les étiquettes reliées restent à écrire"
      - "Non, Bootstrap empêche l'accessibilité"
    correct: 2
    explanation: "Les classes changent l'apparence, pas le sens. Le HTML reste votre travail."
```

## Récap

- Un **framework CSS** est une feuille de style déjà écrite, utilisée par ses **classes** ; Bootstrap se charge par un `<link>` vers un **CDN**, avec une version précise.
- Sa grille **`container`**, **`row`**, **`col-md-4`** est faite de Flexbox et de media queries **mobile-first**, en 12 parts.
- Il fournit une remise à zéro, des composants et des utilitaires ; votre feuille de style se charge **après** la sienne.
- Il ne donne ni le **sens** (les vrais titres), ni les **`alt`**, ni les **étiquettes reliées** : le HTML reste votre travail.

Avec Bootstrap, vous chargez un CSS tout fait, et entier. Tailwind fait l'inverse : il fabrique votre CSS à partir des classes que vous utilisez, ce qui demande une étape de traitement. C'est l'objet du bit [Tailwind, et pourquoi le CSS se compile](https://byte-layers.com/fr/bits/css-build-tools).

```ack
J'ai compris
```
