---
title: "Flexbox : aligner des éléments sur une ligne"
description: "Un conteneur flex range ses enfants sur une ligne et répartit l'espace entre eux : display: flex sur le parent, justify-content et align-items, les axes qui s'inversent avec flex-direction: column, flex-wrap et la largeur de base des éléments."
tags:
  - bit
  - css
difficulty: beginner
duration: 15
requires: "0.9.0"
---

**Flexbox** est le mode de disposition de CSS fait pour aligner des éléments **sur une ligne** (ou sur une colonne) et répartir l'espace entre eux. Vous saurez déclarer un conteneur flex, aligner ses enfants dans les deux sens, éviter le piège des axes qui s'inversent, et faire passer les éléments à la ligne quand la place manque.

**Prérequis** : le bit [Bloc, inline : le flux normal d'une page](https://byte-layers.com/fr/bits/normal-flow), pour les blocs qui s'empilent.

# Flexbox : aligner des éléments sur une ligne

Le flux normal empile les blocs. Avec Flexbox, vous prenez la main sur ce rangement pour une partie de la page : un entête, un menu, une rangée de cartes.

## Un conteneur flex et ses enfants

Flexbox fonctionne toujours **par paire** : on écrit `display: flex` sur un élément, le **conteneur**, et ce sont ses **enfants directs** qui se rangent côte à côte. Les petits-enfants ne sont pas concernés : un enfant peut devenir à son tour le conteneur des siens.

```css
.entete {
  display: flex;   /* sur le parent : ses enfants passent côte à côte */
  gap: 16px;       /* un espace entre les enfants, pas sur les bords */
}
```

L'erreur la plus fréquente est d'écrire `display: flex` sur les éléments qu'on veut aligner, au lieu de leur parent : rien ne se met côte à côte, et aucun message ne le signale.

**À toi** : dans l'entête, mets le logo à gauche et le menu à droite, sur la même ligne, centrés en hauteur ; puis les quatre liens côte à côte, avec `16px` entre eux. La feuille de départ contient déjà l'erreur classique : trouve-la.

```playground
runtime: web
title: Le logo à gauche, le menu à droite
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
      <header class="entete">
        <p class="logo">CM</p>
        <nav>
          <ul class="menu">
            <li><a href="#projets">Projets</a></li>
            <li><a href="#parcours">Parcours</a></li>
            <li><a href="#competences">Compétences</a></li>
            <li><a href="#contact">Contact</a></li>
          </ul>
        </nav>
      </header>
    </body>
    </html>
  style.css: |
    body {
      font-family: system-ui, sans-serif;
      margin: 0;
    }

    .entete {
      background-color: rgb(30, 41, 59);
      padding: 12px 24px;
    }

    .logo {
      color: rgb(255, 255, 255);
      font-size: 28px;
      font-weight: bold;
      margin: 0;
    }

    .menu {
      list-style: none;
      margin: 0;
      padding: 0;
    }

    .menu li {
      display: flex; /* les liens devraient être côte à côte... */
    }

    .menu a {
      color: rgb(255, 255, 255);
      text-decoration: none;
    }
open: [style.css, index.html]
lock: [index.html]
verify:
  - label: "`.entete` est un conteneur flex"
    selector: .entete
    style: { display: flex }
    hint: "Le logo et `nav` sont les enfants de `.entete` : c'est lui qui reçoit `display: flex`."
  - label: le logo à gauche, le menu à droite
    selector: .entete
    style: { justify-content: space-between }
    hint: "`justify-content: space-between` colle le premier enfant à gauche et le dernier à droite."
  - label: le logo et le menu sont centrés en hauteur
    selector: .entete
    style: { align-items: center }
  - label: les liens sont côte à côte, à `16px` les uns des autres
    selector: .menu
    style: { display: flex, column-gap: 16px }
    hint: "Les `li` sont les enfants de `.menu` : `display: flex` va sur `.menu`, pas sur `.menu li`. Puis `gap: 16px`."
solution: assets/entete.solution
```

Deux conteneurs flex imbriqués, c'est courant : `.entete` range le logo et le menu, `.menu` range ses liens. La règle `display: flex` sur `.menu li` ne servait à rien : chaque `li` rangeait son seul enfant, le lien.

## Répartir et aligner : justify-content et align-items

Un conteneur flex a deux réglages principaux. **`justify-content`** décide où va l'espace libre **le long de la ligne** ; **`align-items`** décide comment les éléments s'alignent **en travers**, quand ils n'ont pas la même hauteur.

| `justify-content` | Effet sur la ligne |
|---|---|
| `flex-start` | tout au début (par défaut) |
| `center` | groupés au centre |
| `flex-end` | tout à la fin |
| `space-between` | le premier au début, le dernier à la fin, l'espace réparti entre eux |

| `align-items` | Effet en travers |
|---|---|
| `stretch` | tous étirés à la même hauteur (par défaut) |
| `center` | centrés |
| `flex-start` | alignés en haut |

Le centrage parfait, horizontal et vertical, tient en trois lignes. Complète-les.

```fill
text: ".boite { display: flex; _____: center; _____: center; }   /* centré sur la ligne, puis en travers */"
blanks:
  - answers: [justify-content]
    hint: "La propriété qui répartit l'espace le long de la ligne."
  - answers: [align-items]
    hint: "La propriété qui aligne en travers de la ligne."
```

## Le piège : avec flex-direction: column, les axes s'inversent

Un conteneur flex a un **axe principal**, la direction dans laquelle il range ses enfants, et un **axe secondaire**, perpendiculaire. Par défaut, `flex-direction: row` : l'axe principal est horizontal. `justify-content` agit toujours sur l'axe principal, `align-items` sur l'axe secondaire.

Avec **`flex-direction: column`**, les enfants s'empilent et l'axe principal devient **vertical**. Les deux propriétés échangent leur effet visible : `justify-content: center` centre alors **en hauteur**, et c'est `align-items: center` qui centre **en largeur**.

| `flex-direction` | Axe principal (`justify-content`) | Axe secondaire (`align-items`) |
|---|---|---|
| `row` (par défaut) | horizontal | vertical |
| `column` | vertical | horizontal |

**À toi** : les deux boutons de la carte sont empilés avec `flex-direction: column`, et ils s'étirent sur toute la largeur. On voudrait les centrer horizontalement, à la largeur de leur texte. `justify-content: center` est déjà là, et il ne change rien en largeur : trouve la bonne propriété.

```playground
runtime: web
title: Centrer une colonne de boutons
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Contact</title>
      <link rel="stylesheet" href="style.css">
    </head>
    <body>
      <section class="carte">
        <h2>Travaillons ensemble</h2>
        <div class="actions">
          <a href="#contact">M'écrire</a>
          <a href="cv.pdf">Télécharger mon CV</a>
        </div>
      </section>
    </body>
    </html>
  style.css: |
    body {
      font-family: system-ui, sans-serif;
    }

    .carte {
      max-width: 400px;
      padding: 24px;
      border: 1px solid rgb(203, 213, 225);
    }

    .actions {
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 12px;
    }

    .actions a {
      background-color: rgb(219, 39, 119);
      color: rgb(255, 255, 255);
      padding: 10px 16px;
      text-decoration: none;
    }
open: [style.css, index.html]
lock: [index.html]
verify:
  - label: les boutons sont centrés horizontalement, à la largeur de leur texte
    selector: .actions
    style: { align-items: center }
    hint: "En `column`, l'horizontale est l'axe secondaire : c'est le rôle d'`align-items`."
solution: assets/colonne.solution
```

Le réflexe à garder : avant d'écrire `justify-content` ou `align-items`, demandez-vous dans quelle direction le conteneur range ses enfants.

## Passer à la ligne : flex-wrap et la largeur de base

Par défaut, un conteneur flex garde tous ses enfants **sur une seule ligne**, quitte à les comprimer jusqu'à les rendre illisibles. **`flex-wrap: wrap`** l'autorise à passer à la ligne.

Sur les enfants, le raccourci **`flex`** donne trois valeurs : la capacité à grandir, la capacité à rétrécir, et la **largeur de base** (`flex-basis`). Avec `flex: 1 1 200px`, chaque photo part de `200px`, puis le navigateur en met autant qu'il peut par ligne et partage l'espace restant entre elles.

```css
.photo {
  flex: 1 1 200px;  /* peut grandir, peut rétrécir, part de 200px */
}
```

**À toi** : la galerie comprime ses six photos sur une seule ligne. Autorise le passage à la ligne, et donne à chaque photo une largeur de base de `200px`.

```playground
runtime: web
title: Une galerie qui passe à la ligne
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Galerie</title>
      <link rel="stylesheet" href="style.css">
    </head>
    <body>
      <div class="galerie">
        <div class="photo">Pic du Midi</div>
        <div class="photo">Lac d'Oô</div>
        <div class="photo">Gavarnie</div>
        <div class="photo">Néouvielle</div>
        <div class="photo">Cauterets</div>
        <div class="photo">Bassiès</div>
      </div>
    </body>
    </html>
  style.css: |
    body {
      font-family: system-ui, sans-serif;
    }

    .galerie {
      display: flex;
      gap: 12px;
    }

    .photo {
      background-color: rgb(224, 231, 255);
      height: 120px;
      padding: 8px;
    }
open: [style.css, index.html]
lock: [index.html]
verify:
  - label: la galerie passe à la ligne
    selector: .galerie
    style: { flex-wrap: wrap }
    hint: "`flex-wrap: wrap;` sur le conteneur, `.galerie`."
  - label: chaque photo part d'une largeur de `200px`
    selector: .photo
    style: { flex-basis: 200px }
    hint: "Sur les enfants : `flex: 1 1 200px;` (ou `flex-basis: 200px;`)."
solution: assets/galerie.solution
```

Élargissez et rétrécissez la fenêtre : le nombre de photos par ligne change tout seul, sans aucune règle par largeur d'écran. C'est la largeur de base qui le décide.

> 📖 [Les bases de Flexbox (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/CSS_layout/Flexbox) · [Concepts de base de Flexbox, les axes (MDN)](https://developer.mozilla.org/fr/docs/Web/CSS/CSS_flexible_box_layout/Basic_concepts_of_flexbox) · [La propriété flex (MDN)](https://developer.mozilla.org/fr/docs/Web/CSS/flex)

## Trois questions pour vérifier

```quiz
title: "Flexbox"
tracksProgress: false
showNotice: false
place: stage
questions:
  - prompt: "Vous voulez trois cartes côte à côte, dans `<div class=\"rangee\">`. Où écrivez-vous `display: flex` ?"
    answers:
      - "Sur chaque carte"
      - "Sur `.rangee`, le parent des cartes"
      - "Sur `body`"
    correct: 2
    explanation: "display: flex se pose sur le conteneur ; ce sont ses enfants directs qui se rangent."
  - prompt: "Un conteneur a `flex-direction: column`. Quelle propriété centre ses enfants horizontalement ?"
    answers:
      - "`justify-content: center`"
      - "`align-items: center`"
      - "`text-align: center`"
    correct: 2
    explanation: "En column, l'axe principal est vertical : justify-content agit en hauteur, align-items en largeur."
  - prompt: "Sans `flex-wrap: wrap`, que fait un conteneur flex quand ses enfants ne tiennent pas sur la ligne ?"
    answers:
      - "Il les fait passer à la ligne suivante"
      - "Il cache ceux qui dépassent"
      - "Il les comprime pour les garder sur une seule ligne"
    correct: 3
    explanation: "Par défaut, Flexbox garde tout sur une ligne et rétrécit les enfants. flex-wrap: wrap autorise le passage à la ligne."
```

## Récap

- **`display: flex`** se pose sur le **conteneur** ; ses **enfants directs** se rangent sur une ligne, et **`gap`** les espace.
- **`justify-content`** répartit l'espace sur l'**axe principal**, **`align-items`** aligne sur l'**axe secondaire**.
- Avec **`flex-direction: column`**, l'axe principal devient vertical : les deux propriétés échangent leur effet visible.
- **`flex-wrap: wrap`** autorise le passage à la ligne, et la **largeur de base** (`flex: 1 1 200px`) décide du nombre d'éléments par ligne.

Flexbox range dans une direction à la fois. Pour une grille de projets, avec des lignes et des colonnes alignées en même temps, CSS a un autre outil : c'est l'objet du bit [CSS Grid](https://byte-layers.com/fr/bits/css-grid).

```ack
J'ai compris
```
