---
title: "Les tableaux HTML"
description: "Un tableau présente des données en lignes et en colonnes, jamais une mise en page : tr, td, caption, thead, tbody, th et scope. Le piège : le tableau de mise en page, invisible à l'écran mais annoncé par le lecteur d'écran."
tags:
  - bit
  - html
difficulty: beginner
duration: 10
requires: "0.9.0"
---

Une page ne fait pas que raconter : elle présente aussi des **données**, qui ont un sens en lignes et en colonnes. Vous saurez construire un tableau de données lisible par un lecteur d'écran, et reconnaître un tableau de mise en page.

**Prérequis** : le bit [Le squelette d'une page HTML](https://byte-layers.com/fr/bits/html-document), pour les balises et leurs attributs, et le bit [Flexbox](https://byte-layers.com/fr/bits/flexbox), pour le dernier exercice.

# Les tableaux HTML

Jusqu'ici, la page montre du texte, des images et des liens. Ce contenu ajoute une structure du HTML : le tableau, pour des données qui ont un sens en lignes et en colonnes.

## Un tableau, c'est pour des données

Un tableau se construit **ligne par ligne** : `<tr>` (*table row*) pour une ligne, `<td>` (*table data*) pour une cellule de données. Les colonnes n'ont pas de balise : elles se forment parce que chaque ligne a le même nombre de cellules.

```scene
lesson: assets/tables.scene.json
step: tableau
```

Une cellule qui **nomme** une colonne ou une ligne est un **en-tête** : elle s'écrit `<th>`. Son attribut **`scope`** dit ce qu'elle nomme, `col` pour la colonne en dessous, `row` pour la ligne à droite. Un lecteur d'écran s'en sert pour annoncer chaque cellule avec ses en-têtes : « Pic du Midi, Date : 12 avril ».

## Les parties d'un tableau : caption, thead, tbody

Un tableau de données se range en trois parties, chacune avec sa balise, toutes dans `<table>`.

```scene
lesson: assets/tables.scene.json
step: structure
```

**`<caption>`** donne le titre, juste après `<table>` ; **`<thead>`** (*table head*) regroupe la ligne d'en-tête, avec ses `<th scope="col">` ; **`<tbody>`** (*table body*) regroupe les lignes de données, où le nom de chaque ligne est un `<th scope="row">`.

## À toi : le tableau des sorties

Le tableau des sorties du club n'a que des `<td>`. Donne-lui le titre « Programme des sorties 2026 », une section `thead` avec ses trois en-têtes de colonne, et dans `tbody`, le nom de chaque sortie en en-tête de ligne.

```playground
runtime: web
title: Le tableau des sorties
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Sorties du club</title>
      <link rel="stylesheet" href="style.css">
    </head>
    <body>
      <table>
        <tr>
          <td>Sortie</td>
          <td>Distance</td>
          <td>Difficulté</td>
        </tr>
        <tr>
          <td>Pic du Midi</td>
          <td>14 km</td>
          <td>Difficile</td>
        </tr>
        <tr>
          <td>Boucle des trois lacs</td>
          <td>12 km</td>
          <td>Facile</td>
        </tr>
        <tr>
          <td>Crêtes de Bassiès</td>
          <td>18 km</td>
          <td>Difficile</td>
        </tr>
        <tr>
          <td>Cascade d'Ars</td>
          <td>9 km</td>
          <td>Moyenne</td>
        </tr>
      </table>
    </body>
    </html>
  style.css: |
    body {
      font-family: system-ui, sans-serif;
    }

    th,
    td {
      border: 1px solid rgb(203, 213, 225);
      padding: 6px 10px;
    }
open: [index.html, style.css]
lock: [style.css]
verify:
  - label: le titre « Programme des sorties 2026 » dans un `caption`
    selector: table caption
    text: Programme des sorties 2026
    hint: "`<caption>` se place juste après `<table>`, avant la première ligne."
  - label: trois en-têtes de colonne `th scope="col"` dans `thead`
    selector: thead th[scope=col]
    count: 3
    hint: "Entoure la première ligne de `<thead>…</thead>`, et change ses `td` en `<th scope=\"col\">`."
  - label: le nom des quatre sorties en `th scope="row"` dans `tbody`
    selector: tbody th[scope=row]
    count: 4
    hint: "Entoure les quatre lignes de données de `<tbody>…</tbody>` ; dans chacune, la première cellule devient `<th scope=\"row\">`."
  - label: les distances et les difficultés restent des `td`
    selector: tbody td
    count: 8
solution: assets/sorties.solution
```

Les en-têtes passent en gras et se centrent : c'est le style par défaut d'un `<th>`. `scope`, lui, ne change rien à l'écran ; il sert à ceux qui écoutent la page.

## Le piège : un tableau pour la mise en page

On trouve encore des pages qui placent leurs blocs dans un tableau invisible : une cellule pour le logo, une autre pour le menu. À l'écran, rien ne le trahit.

```scene
lesson: assets/tables.scene.json
step: miseenpage
```

Le lecteur d'écran annonce un tableau qui n'en est pas un, et la page ne peut pas se réorganiser sur un téléphone : les cellules restent côte à côte. Le test est simple : **si le contenu n'a pas de sens en lignes et en colonnes, ce n'est pas un tableau**. La disposition, c'est le CSS.

## À toi : un entête sans tableau

L'entête place le logo et le menu dans un tableau. Retire le tableau (`table`, `tr`, `td`) pour garder le logo et `nav` directement dans `header`, puis mets-les côte à côte avec Flexbox, le logo à gauche et le menu à droite.

```playground
runtime: web
title: Un entête sans tableau
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
        <table width="100%">
          <tr>
            <td><p class="logo">CM</p></td>
            <td align="right">
              <nav>
                <a href="#projets">Projets</a>
                <a href="#contact">Contact</a>
              </nav>
            </td>
          </tr>
        </table>
      </header>
    </body>
    </html>
  style.css: |
    body {
      font-family: system-ui, sans-serif;
    }

    .logo {
      font-weight: bold;
      margin: 0;
    }

    /* Écris la règle .entete ici */
open: [index.html, style.css]
verify:
  - label: la page ne contient plus de tableau
    selector: table
    exists: false
    hint: "Supprime les balises `table`, `tr` et `td`, et garde ce qu'elles contenaient : le paragraphe `.logo` et `nav`."
  - label: le logo et le menu sont les enfants directs de l'entête
    selector: ".entete > .logo, .entete > nav"
    count: 2
  - label: l'entête range ses enfants avec Flexbox, l'espace entre eux
    selector: .entete
    style: { display: flex, justify-content: space-between }
    hint: "`.entete { display: flex; justify-content: space-between; }`"
solution: assets/entete.solution
```

> 📖 [Les bases des tableaux HTML (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Structuring_content/HTML_table_basics) · [L'élément table (MDN)](https://developer.mozilla.org/fr/docs/Web/HTML/Element/table)

## Trois questions pour vérifier

Trois situations tirées des tableaux de ce contenu : choisis la réponse, l'explication suit.

```quiz
title: "Les tableaux HTML"
tracksProgress: false
showNotice: false
place: stage
questions:
  - prompt: "Un tableau a trois colonnes. Quelle balise crée chaque colonne ?"
    answers:
      - "`<col>`, une par colonne"
      - "Aucune : les colonnes se forment parce que chaque ligne `tr` a le même nombre de cellules"
      - "`<th>`, en haut de chaque colonne"
    correct: 2
    explanation: "Un tableau HTML s'écrit ligne par ligne ; les colonnes naissent de l'alignement des cellules. Le th nomme une colonne, il ne la crée pas."
  - prompt: "À quoi sert `scope=\"row\"` sur un `th` ?"
    answers:
      - "À mettre la ligne en gras"
      - "À dire que cet en-tête nomme la ligne, pour qu'un lecteur d'écran annonce chaque cellule avec lui"
      - "À fusionner les cellules de la ligne"
    correct: 2
    explanation: "scope ne change rien à l'écran : il relie les cellules à leurs en-têtes pour les technologies d'assistance."
  - prompt: "Une page place son logo à gauche et son menu à droite. Faut-il un tableau d'une ligne et deux cellules ?"
    answers:
      - "Oui, c'est la façon la plus simple d'aligner deux blocs"
      - "Non : ce contenu n'a pas de sens en lignes et en colonnes, la disposition revient au CSS"
      - "Oui, à condition de ne pas afficher les bordures"
    correct: 2
    explanation: "Un tableau invisible reste un tableau pour le lecteur d'écran, et ses cellules ne se réorganisent pas sur un téléphone. Flexbox ou Grid placent les blocs."
```

## Récap

- Un **tableau** se construit ligne par ligne : `tr` pour une ligne, `td` pour une cellule de données ; les colonnes naissent du même nombre de cellules.
- Un tableau de données se range en `caption` (le titre), `thead` (les en-têtes) et `tbody` (les données).
- Une cellule qui nomme une colonne ou une ligne est un **`th`** ; son **`scope`** (`col` ou `row`) sert au lecteur d'écran.
- Un tableau sert à des **données**, jamais à placer des blocs : la disposition, c'est le CSS.

Une page ne fait pas que présenter des données : elle peut aussi en recueillir auprès du visiteur. C'est l'objet du contenu [Les formulaires HTML](https://byte-layers.com/fr/bits/html-forms).

```ack
J'ai compris
```
