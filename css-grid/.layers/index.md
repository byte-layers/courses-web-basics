---
title: "CSS Grid : des lignes et des colonnes"
description: "Une grille CSS range ses enfants en lignes et en colonnes à la fois : display: grid, grid-template-columns et l'unité fr, un élément sur deux colonnes, une grille qui s'adapte seule avec repeat(auto-fit, minmax()), et comment choisir entre Flexbox et Grid."
tags:
  - bit
  - css
difficulty: beginner
duration: 20
requires: "0.9.0"
---

**CSS Grid** est le mode de disposition de CSS fait pour ranger des éléments **en lignes et en colonnes à la fois**. Vous saurez déclarer une grille et ses colonnes, faire occuper deux cases à un élément, écrire une grille qui change de nombre de colonnes toute seule, et choisir entre Flexbox et Grid.

**Prérequis** : le bit [Flexbox](https://byte-layers.com/fr/bits/flexbox), pour le conteneur, ses enfants et `gap`.

# CSS Grid : des lignes et des colonnes

Avec Flexbox, chaque ligne vit sa vie : une carte de la deuxième ligne n'a aucune raison de s'aligner sous une carte de la première. Pour une grille de projets bien alignée, CSS Grid dessine les colonnes d'abord, puis y range les éléments.

## Une grille : les colonnes d'abord

Comme Flexbox, Grid fonctionne par paire : **`display: grid`** sur le conteneur, et ses enfants directs se rangent dans la grille. La différence, c'est que vous décrivez les **colonnes** avec **`grid-template-columns`** : une valeur par colonne. Les lignes se créent toutes seules, autant qu'il en faut.

```scene
lesson: assets/grid.scene.json
step: pistes
```

Aucune règle ne vise les cartes : elles **suivent les colonnes**, ligne après ligne. L'unité **`fr`** (pour *fraction*) partage l'espace restant entre les colonnes. La fin de la scène s'écrit ainsi :

```css
.projets {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;  /* une colonne double, deux simples */
  gap: 16px;                           /* entre les lignes et entre les colonnes */
}
```

L'écriture `repeat(3, 1fr)` est le raccourci de `1fr 1fr 1fr`.

## À toi : la grille de projets

Six projets s'empilent l'un sous l'autre. Range-les dans une grille de **trois colonnes égales**, avec `24px` d'espace entre les cartes, dans les deux sens.

```playground
runtime: web
title: La grille de projets
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Projets</title>
      <link rel="stylesheet" href="style.css">
    </head>
    <body>
      <section class="projets">
        <article class="carte">Météo du jour</article>
        <article class="carte">Quiz Pyrénées</article>
        <article class="carte">Liste de courses</article>
        <article class="carte">Portfolio v1</article>
        <article class="carte">Recettes</article>
        <article class="carte">Club de rando</article>
      </section>
    </body>
    </html>
  style.css: |
    body {
      font-family: system-ui, sans-serif;
    }

    .carte {
      background-color: rgb(224, 231, 255);
      padding: 24px;
    }

    /* Écris la règle .projets ici */
open: [style.css, index.html]
lock: [index.html]
verify:
  - label: "`.projets` est une grille"
    selector: .projets
    style: { display: grid }
    hint: "`display: grid;` sur le conteneur, `.projets`."
  - label: la grille a trois colonnes
    selector: .projets
    style: { grid-template-columns: "/^\\S+ \\S+ \\S+$/" }
    hint: "`grid-template-columns: repeat(3, 1fr);` ou `1fr 1fr 1fr`."
  - label: "`24px` entre les cartes, en ligne comme en colonne"
    selector: .projets
    style: { row-gap: 24px, column-gap: 24px }
    hint: "`gap: 24px;` règle les deux à la fois."
solution: assets/grille.solution
```

Les six cartes forment deux lignes de trois, alignées en colonnes, sans qu'aucune règle ne vise les cartes elles-mêmes.

## Un élément sur plusieurs colonnes

Chaque enfant occupe une case par défaut. **`grid-column: span 2`** (*span* : s'étendre sur) posé sur un enfant lui fait occuper **deux colonnes**.

```scene
lesson: assets/grid.scene.json
step: span
```

La règle vise l'enfant, pas le conteneur : les autres cartes ne changent pas, elles se rangent dans les cases qui restent, quitte à passer à la ligne suivante.

## À toi : un projet en vedette

La grille est en place. Fais occuper deux colonnes au projet `.vedette`, le premier de la liste.

```playground
runtime: web
title: Un projet en vedette
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Projets</title>
      <link rel="stylesheet" href="style.css">
    </head>
    <body>
      <section class="projets">
        <article class="carte vedette">Club de rando, mon projet de fin de formation</article>
        <article class="carte">Météo du jour</article>
        <article class="carte">Quiz Pyrénées</article>
        <article class="carte">Liste de courses</article>
        <article class="carte">Recettes</article>
      </section>
    </body>
    </html>
  style.css: |
    body {
      font-family: system-ui, sans-serif;
    }

    .projets {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 24px;
    }

    .carte {
      background-color: rgb(224, 231, 255);
      padding: 24px;
    }

    .vedette {
      background-color: rgb(252, 231, 243);
    }
open: [style.css, index.html]
lock: [index.html]
verify:
  - label: le projet vedette occupe deux colonnes
    selector: .vedette
    style: { grid-column: span 2 }
    hint: "Dans la règle `.vedette` : `grid-column: span 2;`."
solution: assets/vedette.solution
```

## Une grille qui s'adapte seule : auto-fit et minmax

Trois colonnes fixes, c'est bien sur un écran large, mais sur un téléphone de `375px` chaque carte ne fait plus qu'une centaine de pixels. Grid sait choisir lui-même le nombre de colonnes : **`repeat(auto-fit, minmax(220px, 1fr))`** veut dire « autant de colonnes que possible, chacune d'au moins `220px`, et l'espace restant partagé entre elles ».

```scene
lesson: assets/grid.scene.json
step: autofit
```

Le nombre de colonnes se **recalcule à chaque largeur** : dès que la colonne de plus ne tiendrait plus à `220px`, la grille la retire, et les cartes se rangent sur celles qui restent.

| Morceau | Rôle |
|---|---|
| `repeat(…, …)` | répète une colonne |
| `auto-fit` | autant de fois que la largeur le permet |
| `minmax(220px, 1fr)` | chaque colonne fait au moins `220px`, au plus une part de l'espace |

> 💡 **Remarque.** On croise aussi `auto-fill` à la place d'`auto-fit`. La différence ne se voit que quand il y a peu d'éléments : `auto-fill` garde des colonnes vides au bout de la ligne, `auto-fit` étire les éléments présents.

## À toi : une grille sans largeur fixe

La grille a trois colonnes fixes. Remplace-les pour que **chaque carte fasse au moins `250px`** de large : la grille doit n'avoir **qu'une colonne sur un téléphone** (`375px`) et **au moins trois sur un grand écran** (`1200px`), sans écrire de règle par largeur d'écran.

```playground
runtime: web
title: Une grille sans largeur fixe
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Projets</title>
      <link rel="stylesheet" href="style.css">
    </head>
    <body>
      <section class="projets">
        <article class="carte">Météo du jour</article>
        <article class="carte">Quiz Pyrénées</article>
        <article class="carte">Liste de courses</article>
        <article class="carte">Portfolio v1</article>
        <article class="carte">Recettes</article>
        <article class="carte">Club de rando</article>
      </section>
    </body>
    </html>
  style.css: |
    body {
      font-family: system-ui, sans-serif;
    }

    .projets {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 24px;
    }

    .carte {
      background-color: rgb(224, 231, 255);
      padding: 24px;
    }
open: [style.css, index.html]
lock: [index.html]
verify:
  - label: une seule colonne sur un téléphone (`375px`)
    selector: .projets
    width: 375
    style: { grid-template-columns: "/^[\\d.]+px$/" }
    hint: "Reprends la formule de la scène : `repeat(auto-fit, minmax(…, 1fr))`, avec le minimum demandé."
  - label: au moins trois colonnes sur un grand écran (`1200px`)
    selector: .projets
    width: 1200
    style: { grid-template-columns: "/^\\S+( \\S+){2,}$/" }
    hint: "Avec `minmax(250px, 1fr)`, combien de colonnes de `250px` tiennent dans `1200px` ?"
solution: assets/autofit.solution
```

## Flex ou Grid : une dimension ou deux

Les deux outils se recoupent, et la question qui les départage est simple : **dans combien de directions faut-il aligner ?** Et ce choix se fait pour chaque conteneur, pas pour toute la page.

```scene
lesson: assets/grid.scene.json
step: combine
```

| Besoin | L'outil, et pourquoi |
|---|---|
| Un menu, une barre d'outils, des boutons côte à côte | **Flexbox** : une seule direction, la taille de chaque élément dépend de son contenu |
| Une grille de cartes alignées en lignes et en colonnes | **Grid** : deux directions à la fois, les colonnes sont les mêmes pour toutes les lignes |
| La disposition d'une page : entête, menu latéral, contenu, pied | **Grid** : des zones en deux dimensions |
| Le contenu d'une carte de la grille : un titre, un texte, un bouton en bas | **Flexbox** : une colonne, dans une case de la grille |

## À toi : Flex ou Grid ?

Trois éléments d'un site, trois conteneurs. Pour chacun, compte les directions dans lesquelles il faut aligner, puis choisis l'outil sur le plateau.

```quiz
title: "Flex ou Grid ?"
tracksProgress: false
showNotice: false
place: stage
questions:
  - prompt: "Un fil d'Ariane : « Accueil > Projets > Météo », sur une ligne."
    answers: ["Flexbox", "Grid"]
    correct: 1
    explanation: "Une seule direction, des éléments de longueurs différentes : Flexbox."
  - prompt: "Un calendrier : sept colonnes, une ligne par semaine, chaque jour aligné sous le même jour de la semaine précédente."
    answers: ["Flexbox", "Grid"]
    correct: 2
    explanation: "Les jours doivent s'aligner en colonnes d'une ligne à l'autre : deux dimensions, Grid."
  - prompt: "Une galerie de photos : autant de colonnes que l'écran le permet, et chaque photo alignée sur celles du dessus."
    answers: ["Flexbox", "Grid"]
    correct: 2
    explanation: "Les photos doivent s'aligner en colonnes d'une ligne à l'autre : deux dimensions, donc Grid, avec repeat(auto-fit, minmax(…, 1fr))."
```

> 📖 [Les grilles CSS (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/CSS_layout/Grids) · [grid-template-columns (MDN)](https://developer.mozilla.org/fr/docs/Web/CSS/grid-template-columns) · [Relation entre Grid et les autres méthodes de disposition (MDN)](https://developer.mozilla.org/fr/docs/Web/CSS/CSS_grid_layout/Relationship_of_grid_layout_with_other_layout_methods)

## Trois questions pour vérifier

```quiz
title: "CSS Grid"
tracksProgress: false
showNotice: false
place: stage
questions:
  - prompt: "Que donne `grid-template-columns: 2fr 1fr` ?"
    answers:
      - "Deux colonnes, la première deux fois plus large que la seconde"
      - "Deux lignes, la première deux fois plus haute"
      - "Trois colonnes de même largeur"
    correct: 1
    explanation: "Une valeur par colonne ; fr partage l'espace restant, ici en trois parts : deux pour la première, une pour la seconde."
  - prompt: "Comment un élément de la grille occupe-t-il deux colonnes ?"
    answers:
      - "`width: 200%`"
      - "`grid-column: span 2` sur cet élément"
      - "`grid-template-columns: span 2` sur le conteneur"
    correct: 2
    explanation: "grid-column se pose sur l'enfant ; grid-template-columns décrit les colonnes du conteneur."
  - prompt: "Que fait `repeat(auto-fit, minmax(220px, 1fr))` sur un écran de 375 px ?"
    answers:
      - "Trois colonnes très étroites"
      - "Une seule colonne : deux colonnes d'au moins 220 px ne tiennent pas"
      - "Une erreur, car il manque une media query"
    correct: 2
    explanation: "auto-fit met autant de colonnes de 220 px minimum que la largeur le permet : une seule sur un téléphone."
```

## Récap

- **`display: grid`** sur le conteneur, **`grid-template-columns`** pour décrire les colonnes ; les lignes se créent seules, et **`gap`** espace les deux.
- L'unité **`fr`** partage l'espace restant ; **`repeat(3, 1fr)`** répète une colonne.
- **`grid-column: span 2`** fait occuper deux colonnes à un élément.
- **`repeat(auto-fit, minmax(220px, 1fr))`** choisit le nombre de colonnes selon la largeur, sans règle par écran.
- **Flexbox** pour une direction, **Grid** pour deux ; on choisit pour chaque conteneur, et on les combine.

Votre page sait maintenant montrer. Elle peut aussi présenter des données en tableau, puis recueillir des informations : c'est l'objet des bits [Les tableaux HTML](https://byte-layers.com/fr/bits/html-tables) et [Les formulaires HTML](https://byte-layers.com/fr/bits/html-forms).

```ack
J'ai compris
```
