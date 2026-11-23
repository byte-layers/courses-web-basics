---
title: "Le responsive design : une page pour tous les écrans"
description: "La même page HTML s'adapte du téléphone au grand écran : la balise meta viewport, des largeurs en max-width plutôt que fixes, les images qui ne débordent plus, et les media queries écrites en mobile-first. Le test décisif : de 360 à 1600 px sans barre de défilement horizontale."
tags:
  - bit
  - css
  - html
difficulty: beginner
duration: 20
requires: "0.9.0"
---

Le **responsive design** consiste à écrire **une seule page** qui s'adapte à toutes les largeurs d'écran, du téléphone au grand écran. Vous saurez pourquoi la balise `meta viewport` est indispensable, comment des largeurs fixes provoquent une barre de défilement horizontale, et comment écrire des media queries dans le bon sens.

**Prérequis** : les bits [Flexbox](https://byte-layers.com/fr/bits/flexbox) et [CSS Grid](https://byte-layers.com/fr/bits/css-grid).

# Le responsive design : une page pour tous les écrans

Une page écrite sur un écran d'ordinateur sera aussi lue sur un téléphone, et ce sera la même page : même HTML, même adresse. Seul le CSS s'ajuste à la largeur.

## Une seule page, des largeurs très différentes

Un même site est lu sur des écrans dont la largeur varie du simple au quadruple, de `360px` pour un téléphone à `1600px` et plus pour un grand écran.

```scene
lesson: assets/responsive.scene.json
step: largeurs
```

Le CSS ne connaît pas l'appareil : il ne connaît que la **largeur de la fenêtre**, en pixels CSS.

Le **test décisif** d'une page adaptative : de `360px` à `1600px`, elle se lit **sans barre de défilement horizontale**. Les outils de développement du navigateur ont un **mode appareil** (Ctrl+Maj+M, ou Cmd+Maj+M sous macOS) qui affiche la page à la largeur de votre choix.

## La balise meta viewport : sans elle, rien ne marche

Un navigateur de téléphone qui ne sait pas si la page est prévue pour lui fait comme si l'écran mesurait environ **`980px`**, puis réduit le tout : le texte devient minuscule, et aucune de vos règles pour petit écran ne s'applique, puisque la fenêtre « mesure » `980px`.

```scene
lesson: assets/responsive.scene.json
step: viewport
```

La page n'a pas changé : seule la **largeur de mise en page** est passée de `980px` à la vraie largeur de l'écran. C'est cette ligne, dans le `head`, qui le dit au navigateur :

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

| Morceau | Rôle |
|---|---|
| `width=device-width` | la largeur de la page est celle de l'écran |
| `initial-scale=1` | aucun zoom au chargement |

⚠️ L'oubli ne se voit **que sur un vrai téléphone** : un ordinateur, l'aperçu des exercices et même certains réglages du mode appareil affichent la page correctement sans elle. C'est pourquoi l'exercice suivant la vérifie dans le texte du fichier.

## Le piège : des largeurs fixes et le scroll horizontal

Une largeur fixe, `width: 960px`, ne rétrécit jamais.

```scene
lesson: assets/responsive.scene.json
step: debord
```

Sur un écran de `375px`, la boîte dépasse de `585px`, et la page entière gagne une **barre de défilement horizontale**. Les images sont le premier coupable, parce qu'elles s'affichent par défaut à leur taille réelle.

| Au lieu de | Écrire |
|---|---|
| `width: 960px` | `max-width: 960px` : la boîte s'arrête à `960px` sur grand écran, et rétrécit sur petit écran |
| rien sur les images | `img { max-width: 100%; height: auto; }` : l'image ne dépasse jamais de son parent et garde ses proportions |
| `padding: 40px` sur tout | des valeurs modestes, ou en `rem` : sur petit écran, chaque pixel compte |

## À toi : une fiche qui déborde

Cette fiche déborde sur un téléphone. Ajoute la balise `meta viewport`, transforme la largeur fixe du conteneur en largeur maximale, et empêche l'image de dépasser.

```playground
runtime: web
title: Une fiche qui déborde
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Camille Martin</title>
      <link rel="stylesheet" href="style.css">
    </head>
    <body>
      <main class="conteneur">
        <h1>Camille Martin</h1>
        <img src="sommet.svg" alt="Un sommet enneigé sous un ciel bleu">
        <p>Développeuse web à Toulouse, randonneuse le week-end.</p>
      </main>
    </body>
    </html>
  style.css: |
    * {
      box-sizing: border-box;
    }

    body {
      font-family: system-ui, sans-serif;
      margin: 0;
    }

    .conteneur {
      width: 960px;
      margin: 0 auto;
      padding: 16px;
    }

    img {
      width: 600px;
    }
  sommet.svg: |
    <svg xmlns="http://www.w3.org/2000/svg" width="600" height="300" viewBox="0 0 600 300">
      <rect width="600" height="300" fill="#bfdbfe"/>
      <polygon points="0,300 220,80 330,190 420,120 600,300" fill="#475569"/>
      <polygon points="220,80 260,120 180,120" fill="#ffffff"/>
    </svg>
open: [style.css, index.html]
verify:
  - label: la balise `meta viewport` est dans le `head`
    file: index.html
    includes: "/<meta[^>]+name=[\"']viewport[\"'][^>]*width=device-width/i"
    hint: "`<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">`, sous le `meta charset`."
  - label: sur un téléphone (`375px`), le conteneur tient dans l'écran
    selector: .conteneur
    width: 375
    style: { width: "/^(\\d{1,2}|[12]\\d\\d|3[0-6]\\d|37[0-5])(\\.\\d+)?px$/" }
    hint: "`width: 960px` ne rétrécit jamais : remplace-le par `max-width: 960px`."
  - label: sur un téléphone, l'image tient dans l'écran
    selector: img
    width: 375
    style: { width: "/^(\\d{1,2}|[12]\\d\\d|3[0-6]\\d|37[0-5])(\\.\\d+)?px$/" }
    hint: "`img { max-width: 100%; height: auto; }` : l'image ne dépasse plus de son parent."
  - label: sur grand écran (`1200px`), le conteneur garde ses `960px`
    selector: .conteneur
    width: 1200
    style: { width: 960px }
solution: assets/fiche.solution
```

Le dernier contrôle vérifie l'autre moitié du travail : `max-width` laisse la boîte à `960px` quand il y a la place, elle ne fait que rétrécir quand il n'y en a pas.

## Les media queries, en mobile-first

Une **media query** applique des règles **seulement à partir d'une certaine largeur**. La méthode courante, le **mobile-first**, écrit d'abord le style du téléphone, sans condition, puis l'enrichit pour les écrans plus larges, avec **`min-width`** :

```css
.menu {
  display: flex;
  flex-direction: column;     /* téléphone : les liens empilés */
}

@media (min-width: 700px) {   /* à partir de 700px de large */
  .menu {
    flex-direction: row;      /* les liens côte à côte */
  }
}
```

Voici ce que fait cette règle quand la fenêtre s'élargit.

```scene
lesson: assets/responsive.scene.json
step: media
```

**`min-width: 700px`** veut dire « la fenêtre fait **au moins** `700px` », donc les grands écrans. `max-width: 700px` veut dire l'inverse, « au plus `700px` ». Confondre les deux est le contresens le plus fréquent : tout est inversé, et aucun message ne le signale. Les media queries se placent **après** les règles de base : à spécificité égale, la dernière règle écrite gagne.

## À toi : un menu qui s'adapte

Le menu devrait être empilé sur un téléphone et en ligne sur grand écran. C'est l'inverse qui se passe. Trouve le contresens dans la media query et corrige-le.

```playground
runtime: web
title: Un menu qui s'adapte
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Camille Martin</title>
      <link rel="stylesheet" href="style.css">
    </head>
    <body>
      <nav>
        <ul class="menu">
          <li><a href="#projets">Projets</a></li>
          <li><a href="#parcours">Parcours</a></li>
          <li><a href="#competences">Compétences</a></li>
          <li><a href="#contact">Contact</a></li>
        </ul>
      </nav>
    </body>
    </html>
  style.css: |
    body {
      font-family: system-ui, sans-serif;
    }

    .menu {
      display: flex;
      flex-direction: column;
      gap: 12px;
      list-style: none;
      padding: 0;
    }

    @media (max-width: 700px) {
      .menu {
        flex-direction: row;
      }
    }
open: [style.css, index.html]
lock: [index.html]
verify:
  - label: sur un téléphone (`375px`), les liens sont empilés
    selector: .menu
    width: 375
    style: { flex-direction: column }
    hint: "À `375px`, la condition `max-width: 700px` est vraie : la media query met le menu en ligne. Laquelle des deux veut dire « au moins » ?"
  - label: sur grand écran (`1200px`), les liens sont en ligne
    selector: .menu
    width: 1200
    style: { flex-direction: row }
    hint: "`@media (min-width: 700px) { … }` s'applique à partir de `700px`."
solution: assets/menu.solution
```

Une page bien construite compte peu de media queries : les largeurs en `max-width`, `flex-wrap` et `repeat(auto-fit, minmax())` font déjà l'essentiel du travail sans aucune condition.

> 📖 [Le responsive design (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/CSS_layout/Responsive_Design) · [Les media queries (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/CSS_layout/Media_queries) · [La balise meta viewport (MDN)](https://developer.mozilla.org/fr/docs/Web/HTML/Guides/Viewport_meta_element) · [Responsive web design basics (web.dev, en anglais)](https://web.dev/articles/responsive-web-design-basics)

## Trois questions pour vérifier

```quiz
title: "Le responsive design"
tracksProgress: false
showNotice: false
place: stage
questions:
  - prompt: "Une page sans `meta viewport` est ouverte sur un téléphone. Que se passe-t-il ?"
    answers:
      - "Elle s'affiche normalement, la balise ne sert qu'aux tablettes"
      - "Le navigateur fait comme si l'écran mesurait environ 980 px et réduit la page : le texte est minuscule, les media queries pour petit écran ne s'appliquent pas"
      - "La page ne s'affiche pas"
    correct: 2
    explanation: "Sans meta viewport, le navigateur du téléphone simule un écran large puis réduit le tout."
  - prompt: "Pourquoi `max-width: 960px` plutôt que `width: 960px` ?"
    answers:
      - "Parce que la boîte s'arrête à 960 px sur grand écran et rétrécit sur un petit, sans barre de défilement horizontale"
      - "Parce que `width` ne fonctionne pas sur un `main`"
      - "Parce que `max-width` est plus récent"
    correct: 1
    explanation: "width fixe la largeur à 960 px partout ; max-width ne fixe qu'une limite haute."
  - prompt: "En mobile-first, que veut dire `@media (min-width: 700px)` ?"
    answers:
      - "Les règles s'appliquent aux écrans de moins de 700 px"
      - "Les règles s'appliquent aux écrans d'au moins 700 px"
      - "Les règles s'appliquent seulement à 700 px tout pile"
    correct: 2
    explanation: "min-width : la fenêtre fait au moins cette largeur. Le style de base sert au téléphone, la media query enrichit pour les grands écrans."
```

## Récap

- Une page **responsive** est une seule page dont le CSS s'adapte à la **largeur de la fenêtre** ; le test décisif : de `360px` à `1600px`, **aucun défilement horizontal**.
- Sans **`meta viewport`**, un téléphone simule un écran de `980px` : rien de ce qui est prévu pour lui ne s'applique.
- Des largeurs en **`max-width`**, jamais fixes, et **`img { max-width: 100%; height: auto; }`**.
- **Mobile-first** : le style du téléphone d'abord, puis des **`@media (min-width: …)`** par largeur croissante, après les règles de base.

Cette page sera lue sur tous les écrans, mais aussi sans souris, ou sans les yeux, par un lecteur d'écran. Ça se vérifie : c'est l'objet du bit [L'accessibilité web](https://byte-layers.com/fr/bits/web-accessibility).

```ack
J'ai compris
```
