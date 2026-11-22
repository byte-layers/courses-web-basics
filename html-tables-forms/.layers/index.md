---
title: "Tableaux et formulaires HTML"
description: "Un tableau présente des données en lignes et en colonnes, jamais une mise en page : caption, thead, tbody, th et scope. Un formulaire recueille des informations et les envoie au serveur : input et ses types, label relié par for et id, name, required. Les pièges : le tableau de mise en page, le champ sans name, le label non relié."
tags:
  - bit
  - html
difficulty: beginner
duration: 15
requires: "0.9.0"
---

Une page ne fait pas que montrer : elle présente des **données** en tableau, et elle peut **recueillir** des informations avec un formulaire, qu'elle envoie au serveur. Vous saurez construire un tableau de données lisible par un lecteur d'écran, reconnaître un tableau de mise en page, et écrire un formulaire dont chaque champ est relié à son étiquette et bien envoyé.

**Prérequis** : le bit [Le squelette d'une page HTML](https://byte-layers.com/fr/bits/html-document), pour les balises et leurs attributs, et le bit [Flexbox](https://byte-layers.com/fr/bits/flexbox).

# Tableaux et formulaires HTML

Jusqu'ici, la page montre du texte, des images et des liens. Ce contenu ajoute deux structures du HTML : le tableau, pour des données qui ont un sens en lignes et en colonnes, et le formulaire, pour que le visiteur réponde.

## Un tableau, c'est pour des données

Un tableau se construit **ligne par ligne** : `<tr>` (*table row*) pour une ligne, `<td>` (*table data*) pour une cellule de données. Les colonnes n'ont pas de balise : elles se forment parce que chaque ligne a le même nombre de cellules.

Une cellule qui **nomme** une colonne ou une ligne est un **en-tête** : elle s'écrit `<th>`. Son attribut **`scope`** dit ce qu'elle nomme, `col` pour la colonne en dessous, `row` pour la ligne à droite. Un lecteur d'écran s'en sert pour annoncer chaque cellule avec ses en-têtes : « Pic du Midi, Distance : 14 km ».

| Balise | Rôle |
|---|---|
| `<caption>` | le titre du tableau, juste après `<table>` |
| `<thead>` | la ou les lignes d'en-tête |
| `<tbody>` | les lignes de données |
| `<th scope="col">` | un en-tête de colonne |
| `<th scope="row">` | un en-tête de ligne |

**À toi** : le tableau des sorties du club n'a que des `<td>`. Donne-lui le titre « Programme des sorties 2026 », une section `thead` avec ses trois en-têtes de colonne, et dans `tbody`, le nom de chaque sortie en en-tête de ligne.

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

Dans les années 2000, on plaçait les blocs d'une page dans des tableaux invisibles : une cellule pour le logo, une autre pour le menu. Cela marche à l'écran, mais un lecteur d'écran annonce « tableau, une ligne, deux colonnes » et lit le menu comme une donnée, et la page ne peut pas se réorganiser sur un téléphone. Le test est simple : **si le contenu n'a pas de sens en lignes et en colonnes, ce n'est pas un tableau**. La disposition, c'est le CSS.

**À toi** : l'entête place le logo et le menu dans un tableau. Retire le tableau (`table`, `tr`, `td`) pour garder le logo et `nav` directement dans `header`, puis mets-les côte à côte avec Flexbox, le logo à gauche et le menu à droite.

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

## Un formulaire : ce que la page envoie au serveur

Un formulaire, c'est le chemin inverse d'une page : au lieu de recevoir du texte du serveur, le navigateur lui **envoie** ce que le visiteur a saisi. Tous les champs vivent dans un `<form>` ; son attribut `action` donne l'adresse qui reçoit les données, `method` la façon de les envoyer.

Chaque champ a trois attributs qui ne servent pas à la même chose :

| Attribut | Pour qui | Rôle |
|---|---|---|
| `id` | la page | un nom unique, que vise le `for` de l'étiquette |
| `name` | le serveur | le nom sous lequel la valeur est envoyée : `email=camille%40exemple.fr` |
| `type` | le navigateur | le genre de champ : `text`, `email`, `tel`, `date`, `checkbox`, `radio` |

L'**étiquette** s'écrit dans un `<label>`, et son attribut `for` reprend **exactement** l'`id` du champ. Cliquer sur l'étiquette met alors le curseur dans le champ (ou coche la case), et un lecteur d'écran annonce l'étiquette en arrivant sur le champ.

```html
<label for="email">Votre e-mail</label>
<input type="email" id="email" name="email" required>
```

L'attribut **`required`** fait refuser l'envoi par le navigateur tant que le champ est vide, et `type="email"` lui fait vérifier la présence d'un `@`. Ces contrôles rendent service au visiteur, mais ils se contournent : le serveur doit tout revérifier.

## Les pièges : un champ sans name, une étiquette non reliée

Deux fautes ne se voient pas à l'écran. Un champ **sans `name`** s'affiche et se remplit normalement, mais sa valeur **n'est pas envoyée** : le serveur ne la reçoit jamais. Une étiquette dont le **`for` ne correspond à aucun `id`** s'affiche aussi normalement, mais elle n'est plus reliée : le clic ne fait rien, et le lecteur d'écran annonce « zone de texte » sans dire laquelle. Aucun message d'erreur dans les deux cas.

**À toi** : le champ Nom est le modèle, complet. Les trois autres ont chacun un défaut : trouve-les et corrige-les. Clique sur chaque étiquette dans l'aperçu : celle qui ne réagit pas n'est pas reliée. Le formulaire n'envoie rien dans l'aperçu, c'est voulu.

```playground
runtime: web
title: Un formulaire de contact bien relié
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
      <form action="/contact" method="post">
        <p>
          <label for="nom">Votre nom</label>
          <input type="text" id="nom" name="nom" required>
        </p>
        <p>
          <label for="mail">Votre e-mail</label>
          <input type="text" id="email">
        </p>
        <p>
          <label for="message">Votre message</label>
          <textarea id="message" rows="5"></textarea>
        </p>
        <p>
          <input type="checkbox" id="newsletter" name="newsletter">
          <label>Je souhaite recevoir la lettre d'information</label>
        </p>
        <button type="submit">Envoyer</button>
      </form>
    </body>
    </html>
  style.css: |
    body {
      font-family: system-ui, sans-serif;
    }

    label {
      display: block;
    }

    #newsletter + label {
      display: inline;
    }
open: [index.html, style.css]
lock: [style.css]
check: ask
verify:
  - label: chaque champ a un `name`, sinon sa valeur n'est pas envoyée
    selector: "form input, form textarea"
    attr: { name: "/\\S/" }
    hint: "Comme le champ Nom : `name=\"email\"`, `name=\"message\"`."
  - label: l'étiquette de l'e-mail vise l'`id` du champ
    selector: "label[for=email]"
    count: 1
    hint: "Le `for` de l'étiquette dit `mail`, l'`id` du champ dit `email` : un seul des deux doit changer."
  - label: l'e-mail est vérifié par le navigateur et obligatoire
    selector: "#email"
    attr: { type: email, required: true }
    hint: "`type=\"email\"` et l'attribut `required`, écrit seul."
  - label: un clic sur l'étiquette de la lettre coche la case
    click: "#newsletter + label"
    selector: "#newsletter:checked"
    hint: "L'étiquette n'a pas de `for` : `<label for=\"newsletter\">`."
solution: assets/contact.solution
```

Les quatre défauts avaient un point commun : la page s'affichait exactement pareil avant et après. C'est le genre de faute qu'un générateur de code laisse passer, et que seul un test (cliquer sur les étiquettes, regarder ce que reçoit le serveur) fait apparaître.

> 📖 [Les bases des tableaux HTML (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Structuring_content/HTML_table_basics) · [Votre premier formulaire (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Extensions/Forms/Your_first_form) · [L'élément label (MDN)](https://developer.mozilla.org/fr/docs/Web/HTML/Element/label) · [Les types de champ input (MDN)](https://developer.mozilla.org/fr/docs/Web/HTML/Element/input#les_différents_types_de_champs_input)

## Trois questions pour vérifier

```quiz
title: "Tableaux et formulaires"
tracksProgress: false
showNotice: false
place: stage
questions:
  - prompt: "À quoi sert `scope=\"row\"` sur un `th` ?"
    answers:
      - "À mettre la ligne en gras"
      - "À dire que cet en-tête nomme la ligne, pour qu'un lecteur d'écran annonce chaque cellule avec lui"
      - "À fusionner les cellules de la ligne"
    correct: 2
    explanation: "scope ne change rien à l'écran : il relie les cellules à leurs en-têtes pour les technologies d'assistance."
  - prompt: "Un champ a un `id` et une étiquette reliée, mais pas de `name`. Que reçoit le serveur à l'envoi ?"
    answers:
      - "La valeur du champ, sous le nom de son `id`"
      - "Rien pour ce champ : sans `name`, sa valeur n'est pas envoyée"
      - "Un message d'erreur"
    correct: 2
    explanation: "name est le nom d'envoi ; id sert seulement dans la page. Un champ sans name s'affiche, mais n'est pas envoyé."
  - prompt: "Comment vérifier qu'une étiquette est bien reliée à son champ ?"
    answers:
      - "Cliquer sur l'étiquette : le curseur doit aller dans le champ, ou la case se cocher"
      - "Regarder si l'étiquette est bien à côté du champ"
      - "Ouvrir la console : une erreur s'affiche si le lien est cassé"
    correct: 1
    explanation: "Le lien for/id ne se voit pas et ne produit aucune erreur ; le clic est le test le plus simple."
```

## Récap

- Un **tableau** sert à des **données** qui ont un sens en lignes et en colonnes : `caption`, `thead`, `tbody`, `th` avec **`scope`**, `td`. Jamais pour placer des blocs : c'est le rôle du CSS.
- Un **formulaire** envoie des données au serveur : chaque champ a un **`name`** (le nom d'envoi), un **`id`** (le nom dans la page) et un **`type`**.
- Le **`label`** est relié par son **`for`**, qui reprend exactement l'`id` du champ ; le clic sur l'étiquette le vérifie.
- **`required`** et `type="email"` font contrôler la saisie par le navigateur, sans remplacer la vérification par le serveur.

Cette page, avec son tableau et son formulaire, sera lue sur un écran de `1600px` comme sur un téléphone de `360px` : c'est l'objet du bit [Le responsive design](https://byte-layers.com/fr/bits/responsive-design).

```ack
J'ai compris
```
