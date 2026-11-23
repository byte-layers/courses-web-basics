---
title: "Le DOM : la page vue par JavaScript"
description: "Le navigateur transforme le HTML en un arbre d'objets, le DOM, que JavaScript lit et modifie : trouver des éléments avec querySelector et querySelectorAll, changer leur texte et leurs classes, créer et insérer de nouveaux éléments ; les pièges du premier élément seulement et de la NodeList, une liste qui n'est pas un élément."
tags:
  - bit
  - javascript
  - dom
  - web
difficulty: beginner
duration: 20
requires: "0.9.0"
---

La page HTML que vous avez écrite, JavaScript la voit comme un arbre d'objets, le **DOM**, qu'il peut lire et changer. Vous saurez trouver des éléments avec `querySelector` et `querySelectorAll`, changer leur texte avec `textContent` et leurs classes avec `classList`, créer un élément et l'insérer dans la page, et éviter deux pièges : `querySelector` ne rend que le premier élément trouvé, et `querySelectorAll` rend une liste, sur laquelle on ne change rien d'un coup.

**Prérequis** : [Fonctions et objets](https://byte-layers.com/fr/bits/js-functions-objects), pour les objets et la notation à point, et [Où vit le JavaScript dans une page](https://byte-layers.com/fr/bits/js-in-page), pour `defer`.

# Le DOM : la page vue par JavaScript

Jusqu'ici, votre code parle à la console. À partir de maintenant, il parle à la page : il lit ce qu'elle contient, le modifie, ajoute des éléments qui n'existaient pas.

## Le DOM : la page sous forme d'objets

En lisant le HTML, le navigateur construit en mémoire un **arbre d'objets** : un objet par élément, rangé dans son parent, comme les balises sont imbriquées. Cet arbre s'appelle le **DOM** (*Document Object Model*, le modèle objet du document). C'est lui que le navigateur dessine, et c'est lui que JavaScript modifie, à partir de l'objet **`document`**, la racine de l'arbre.

La scène montre l'arbre construit pour une petite page, puis ce qui change quand JavaScript ajoute un élément.

```scene
lesson: assets/dom.scene.json
step: arbre
```

Le fichier HTML, lui, ne change jamais. Quand JavaScript ajoute un élément, il l'ajoute au DOM : la page affichée le montre, mais le code source (clic droit, **Afficher le code source**) reste tel que vous l'avez écrit. L'onglet **Éléments** (*Elements*, ou *Inspecteur* dans Firefox) des outils de développement, lui, montre le DOM, modifications comprises.

## Trouver des éléments : `querySelector` et `querySelectorAll`

Pour agir sur un élément, on commence par le trouver, avec un **sélecteur CSS**, exactement ceux de votre feuille de style : `"h1"`, `".projet"`, `"#compteur"`, `"nav a"`.

```scene
lesson: assets/dom.scene.json
step: chercher
```

| Méthode | Rend |
|---|---|
| `document.querySelector(sel)` | le **premier** élément qui correspond, et lui seul ; `null` s'il n'y en a aucun |
| `document.querySelectorAll(sel)` | **tous** les éléments, dans une liste (une `NodeList`) ; une liste vide, de `length` 0, s'il n'y en a aucun |

Une `NodeList` ressemble à un tableau : elle a un `length`, des index, et `for…of` la parcourt. Mais c'est une **liste**, pas un élément : elle n'a pas les propriétés d'un élément. `liste.classList` vaut `undefined` ; ce sont ses éléments, un par un, qui ont une `classList`.

## À toi : compte les projets de la page

La page contient trois projets, et le paragraphe `#compteur` doit dire combien. Le code affiche « undefined projets » : corrige la recherche, sans écrire le nombre à la main.

```playground
runtime: web
title: Compte les projets de la page
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Mes projets</title>
      <script src="script.js" defer></script>
    </head>
    <body>
      <h1>Mes projets</h1>
      <p id="compteur">— projets</p>
      <article class="projet"><h2>Portfolio</h2></article>
      <article class="projet"><h2>Météo</h2></article>
      <article class="projet"><h2>Quiz</h2></article>
    </body>
    </html>
  script.js: |
    const projets = document.querySelector(".projet");
    const compteur = document.querySelector("#compteur");
    compteur.textContent = projets.length + " projets";
open: [script.js, index.html]
lock: [index.html]
show: [editor, preview, console]
verify:
  - label: "`#compteur` affiche « 3 projets »"
    selector: "#compteur"
    text: 3 projets
    hint: "`querySelector` rend un seul élément, qui n'a pas de `length`. Pour tous les projets : `querySelectorAll`."
  - label: le nombre vient de `length`, pas d'un 3 écrit à la main
    file: script.js
    excludes: /["'`]3 projets/
solution: assets/compter.solution
```

`querySelector(".projet")` rendait le premier projet seulement, un élément, pas une liste : il n'a pas de `length`, d'où `undefined`. Aucune erreur rouge, juste un texte faux.

## Changer un élément : `textContent` et `classList`

Un élément trouvé est un objet : on change ce qu'il affiche en modifiant ses propriétés.

```javascript
const titre = document.querySelector("h1");
const carte = document.querySelector(".projet");

titre.textContent = "Bonjour !";     // remplace le texte du titre
carte.classList.add("en-avant");     // pose la classe : le CSS colore la carte
carte.classList.toggle("en-avant");  // la retire, puisqu'elle y est
```

La scène joue ces trois lignes : le code à gauche, la page affichée à droite.

```scene
lesson: assets/dom.scene.json
step: changer
```

| Exemple | Effet |
|---|---|
| `titre.textContent = "Bonjour"` | remplace le texte de l'élément |
| `carte.classList.add("en-avant")` | pose une classe |
| `carte.classList.remove("en-avant")` | retire une classe |
| `carte.classList.toggle("en-avant")` | pose la classe si elle manque, la retire sinon |
| `carte.classList.contains("en-avant")` | `true` ou `false` |
| `carte.style.background = "yellow"` | écrit un style directement sur l'élément |

On préfère **`classList`** à `style` : la couleur reste dans le CSS, où elle se change en un seul endroit, et retirer la classe suffit à revenir en arrière. Un style écrit par `style` l'emporte sur les classes, et il faut penser à le vider.

## À toi : mets en avant chaque projet

Le CSS de la page contient une classe `en-avant`, qui donne un fond jaune clair. Le code veut la poser sur les trois projets, mais s'arrête sur une erreur : lis-la, puis corrige.

```playground
runtime: web
title: Mets en avant chaque projet
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Mes projets</title>
      <link rel="stylesheet" href="style.css">
      <script src="script.js" defer></script>
    </head>
    <body>
      <h1>Mes projets</h1>
      <article class="projet"><h2>Portfolio</h2></article>
      <article class="projet"><h2>Météo</h2></article>
      <article class="projet"><h2>Quiz</h2></article>
    </body>
    </html>
  style.css: |
    .projet { padding: 8px; border: 1px solid rgb(203, 213, 225); margin: 8px 0; }
    .en-avant { background-color: rgb(254, 243, 199); }
  script.js: |
    const projets = document.querySelectorAll(".projet");
    projets.classList.add("en-avant");
open: [script.js, index.html, style.css]
lock: [index.html, style.css]
show: [editor, preview, console]
verify:
  - label: les trois projets portent la classe `en-avant`
    selector: ".projet.en-avant"
    count: 3
    hint: "Une liste n'a pas de `classList` : chaque élément en a une. Parcours la liste avec `for (const projet of projets)`."
  - label: leur fond est jaune clair, grâce à la classe
    selector: ".projet"
    style: { background-color: "rgb(254, 243, 199)" }
  - label: aucun style écrit en JavaScript
    file: script.js
    excludes: /\.style\b/
    hint: "Pose la classe avec `classList.add`, la couleur reste dans le CSS."
  - label: aucune erreur JavaScript
    errors: none
solution: assets/classes.solution
```

L'erreur disait `Cannot read properties of undefined (reading 'add')` : la liste n'a pas de propriété `classList`, donc `projets.classList` vaut `undefined`, et l'on ne peut rien lire dedans. Chaque élément de la liste, lui, a sa `classList` : la boucle les prend un par un.

## Créer et insérer : `createElement` et `append`

Pour ajouter un élément qui n'existe pas dans le HTML, on le fabrique, on le remplit, puis on l'insère dans un parent :

```javascript
const li = document.createElement("li"); // fabrique un <li>, encore hors de la page
li.textContent = "HTML";                  // le remplit
liste.append(li);                         // l'insère à la fin de liste : il apparaît
```

Voici les trois gestes l'un après l'autre : l'élément n'apparaît qu'au dernier.

```scene
lesson: assets/dom.scene.json
step: inserer
```

Un élément fabriqué n'est pas dans la page tant qu'il n'est pas inséré : si le code tourne sans erreur et que rien ne s'affiche, c'est presque toujours un `append` oublié. Pour une liste, les trois gestes vont **dans** la boucle : un `createElement` placé avant la boucle fabrique un seul élément, que chaque `append` déplace, et la page n'affiche que le dernier.

## À toi : construis la liste des compétences

Remplis la liste `#competences` avec une ligne par compétence du tableau.

```playground
runtime: web
title: Construis la liste des compétences
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Compétences</title>
      <script src="script.js" defer></script>
    </head>
    <body>
      <h1>Mes compétences</h1>
      <ul id="competences"></ul>
    </body>
    </html>
  script.js: |
    const competences = ["HTML", "CSS", "JavaScript", "Git"];
    const liste = document.querySelector("#competences");

    // À toi : un <li> par compétence, inséré dans liste
open: [script.js, index.html]
lock: [index.html]
show: [editor, preview, console]
check: ask
verify:
  - label: la liste contient quatre lignes
    selector: "#competences li"
    count: 4
    hint: "Dans une boucle `for (const competence of competences)` : `createElement(\"li\")`, `textContent`, puis `liste.append(li)`."
  - label: la première ligne affiche « HTML »
    selector: "#competences li:first-child"
    text: HTML
  - label: la dernière ligne affiche « Git »
    selector: "#competences li:last-child"
    text: Git
    hint: "Si une seule ligne apparaît, avec « Git », ton `createElement` est hors de la boucle : un seul élément a été déplacé quatre fois."
solution: assets/creer.solution
```

> 📖 [Introduction au DOM (MDN)](https://developer.mozilla.org/fr/docs/Web/API/Document_Object_Model/Introduction) · [querySelectorAll (MDN)](https://developer.mozilla.org/fr/docs/Web/API/Document/querySelectorAll) · [classList (MDN)](https://developer.mozilla.org/fr/docs/Web/API/Element/classList) · [createElement (MDN)](https://developer.mozilla.org/fr/docs/Web/API/Document/createElement)

## Trois questions pour vérifier ce que vous avez retenu

```quiz
title: "Le DOM"
tracksProgress: false
showNotice: false
place: stage
questions:
  - prompt: "La page contient cinq éléments `.livre`. Que rend `document.querySelector(\".livre\")` ?"
    answers:
      - "Une liste des cinq livres"
      - "Le premier livre seulement"
      - "Le dernier livre"
    correct: 2
    explanation: "querySelector s'arrête au premier élément qui correspond. Pour les cinq, il faut querySelectorAll."
  - prompt: "Que rend `document.querySelectorAll(\".perdu\")` quand aucun élément n'a cette classe ?"
    answers:
      - "null"
      - "Une liste vide, de length 0"
      - "Une erreur rouge"
    correct: 2
    explanation: "querySelectorAll rend toujours une liste, vide s'il n'y a rien : une boucle dessus ne fait simplement aucun tour. C'est querySelector qui rend null."
  - prompt: "Pourquoi `document.querySelectorAll(\".projet\").classList.add(\"en-avant\")` lève-t-il une erreur ?"
    answers:
      - "Parce que la page n'a pas de projet"
      - "Parce que la NodeList est une liste : elle n'a pas de classList, ce sont ses éléments qui en ont une"
      - "Parce que classList ne marche qu'avec querySelector"
    correct: 2
    explanation: "Une NodeList a un length, des index, et for…of la parcourt, mais pas les propriétés d'un élément : sa classList vaut undefined. On pose la classe sur chaque élément, dans une boucle."
```

## Récap

- Le **DOM** est l'arbre d'objets que le navigateur construit à partir du HTML ; JavaScript le modifie à partir de `document`, et le fichier HTML, lui, ne change pas.
- **`querySelector`** rend le **premier** élément trouvé (ou `null`) ; **`querySelectorAll`** rend une `NodeList` de tous les éléments, vide s'il n'y a rien : une **liste**, pas un élément, qu'on parcourt pour agir sur chacun.
- **`textContent`** change le texte ; **`classList`** pose, retire, bascule des classes, et la couleur reste dans le CSS.
- **`createElement`** fabrique un élément, **`append`** l'insère ; pour une liste, les deux gestes vont dans la boucle.

Votre code construit la page une fois, au chargement, puis ne fait plus rien. Pour qu'il attende que le visiteur clique ou tape, il faut écouter des événements : c'est l'objet du bit [Les événements : réagir aux actions du visiteur](https://byte-layers.com/fr/bits/dom-events).

```ack
J'ai compris
```
