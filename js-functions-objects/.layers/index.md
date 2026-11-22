---
title: "Fonctions et objets en JavaScript"
description: "Nommer un geste une fois avec une fonction, ses paramètres et son return ; décrire une chose par plusieurs valeurs avec un objet, et parcourir un tableau d'objets ; le piège du return oublié, qui rend undefined."
tags:
  - bit
  - javascript
  - web
difficulty: beginner
duration: 15
requires: "0.9.0"
---

Ce que vous répétez, vous le nommez une fois ; ce que vous décrivez, vous le rangez ensemble. Vous saurez écrire une **fonction** avec ses paramètres, lui faire rendre un résultat avec `return`, décrire une chose par un **objet** (`{ titre: "Dune", pages: 900 }`), parcourir un tableau d'objets, et reconnaître le piège du `return` oublié : la fonction calcule, mais rend `undefined`.

**Prérequis** : [Répéter : tableaux et boucles](https://byte-layers.com/fr/bits/js-arrays-loops), pour les tableaux et `for…of`.

# Fonctions et objets

Calculer un prix toutes taxes comprises à trois endroits, c'est trois fois la même formule, et trois endroits à corriger si le taux change. Décrire un projet par un titre, une année et une technologie, c'est trois variables à garder ensemble. Les fonctions et les objets répondent à ces deux gênes.

## Une fonction : un geste nommé une fois

Une **fonction** est un bloc de code qui porte un nom, et qu'on exécute en l'**appelant** par ce nom suivi de parenthèses. On la déclare avec le mot-clé `function` :

```javascript
function addition(a, b) {
  return a + b;
}

console.log(addition(5, 3)); // 8
console.log(addition(2, 2)); // 4
```

| Morceau | Rôle |
|---|---|
| `function addition` | déclare une fonction nommée `addition` |
| `(a, b)` | les **paramètres** : des noms qui recevront les valeurs données à l'appel |
| `return a + b;` | **rend** la valeur calculée à celui qui a appelé, et termine la fonction |
| `addition(5, 3)` | l'**appel** : 5 et 3 sont les **arguments**, rangés dans `a` et `b` |

Vous avez déjà appelé des fonctions toutes faites : `console.log(…)`, `Number(…)`, `Math.max(…)`. Déclarer la vôtre, c'est ajouter un mot au langage.

## `return` : rendre un résultat, pas l'afficher

Afficher un résultat et le rendre sont deux choses différentes. `console.log` l'écrit dans la console, pour vous ; **`return`** le donne au code qui a appelé la fonction, qui peut alors s'en servir : le multiplier, le comparer, l'afficher dans la page. Une fonction sans `return` rend **`undefined`**.

La fonction `prixTTC` ci-dessous calcule bien le prix augmenté de 20 %, mais la dernière ligne affiche `NaN` (*Not a Number*, « pas un nombre »). Lisez la console, puis corrigez la fonction pour que deux abonnements coûtent 60.

```playground
runtime: web
title: La fonction qui calcule mais ne rend rien
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Tarifs</title>
      <script src="script.js" defer></script>
    </head>
    <body>
      <h1>Tarifs</h1>
    </body>
    </html>
  script.js: |
    function prixTTC(prixHT) {
      console.log(prixHT * 1.2);
    }

    const total = prixTTC(25) * 2;
    console.log("Deux abonnements : " + total);
open: [script.js, index.html]
lock: [index.html]
show: [editor, preview, console]
verify:
  - label: "la console affiche « Deux abonnements : 60 »"
    console: "/^Deux abonnements : 60$/"
    hint: "La fonction affiche 30, mais ne le rend pas : `prixTTC(25)` vaut `undefined`, et `undefined * 2` donne `NaN`. Remplace `console.log(…)` par `return …`."
  - label: "`prixTTC` rend son résultat avec `return`"
    file: script.js
    includes: /return\s+prixHT/
solution: assets/return.solution
```

La console affichait bien `30` : la fonction faisait le calcul, mais ne le donnait à personne. `prixTTC(25)` valait `undefined`, et `undefined * 2` donne `NaN`, sans erreur rouge. Une fonction qui ne fait qu'afficher ne se réutilise nulle part.

## Un objet : ranger une description

Un **objet** regroupe plusieurs valeurs qui décrivent une même chose. Il s'écrit entre accolades, avec des paires **clé : valeur** séparées par des virgules :

```javascript
const livre = { titre: "Dune", auteur: "Frank Herbert", pages: 900 };

console.log(livre.titre);      // Dune : la notation à point
console.log(livre["auteur"]);  // Frank Herbert : la notation à crochets
console.log(livre.editeur);    // undefined : la clé n'existe pas
livre.editeur = "Pocket";      // ajoute une clé
```

| Écriture | Ce qu'elle fait |
|---|---|
| `livre.titre` | lit la valeur de la clé `titre` |
| `livre["auteur"]` | même chose, la clé écrite comme un texte : utile quand elle est dans une variable |
| `livre.editeur` | une clé absente rend `undefined`, sans erreur |
| `livre.editeur.nom` | aller chercher **dans** `undefined` lève une erreur : `TypeError: Cannot read properties of undefined` |

Les objets se rangent dans des tableaux : un **tableau d'objets** est la forme la plus courante des données d'une application, une liste de livres, de contacts, de projets. On le parcourt avec `for…of`, et chaque tour reçoit un objet entier.

Votre portfolio liste des projets. Écrivez la fonction `decrire`, qui reçoit un projet et **rend** un texte de la forme `Portfolio (2026, HTML)` ; la boucle du bas l'appelle pour chaque projet.

```playground
runtime: web
title: Décrire chaque projet d'une liste
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
    </body>
    </html>
  script.js: |
    const projets = [
      { titre: "Portfolio", annee: 2026, techno: "HTML" },
      { titre: "Météo", annee: 2025, techno: "JavaScript" },
      { titre: "Quiz", annee: 2024, techno: "CSS" }
    ];

    function decrire(projet) {
      // À toi : rends un texte comme "Portfolio (2026, HTML)"
    }

    for (const projet of projets) {
      console.log(decrire(projet));
    }
open: [script.js, index.html]
lock: [index.html]
show: [editor, preview, console]
check: ask
verify:
  - label: la console affiche « Portfolio (2026, HTML) »
    console: /^Portfolio \(2026, HTML\)$/
    hint: "Assemble avec `+` : `return projet.titre + \" (\" + projet.annee + \", \" + projet.techno + \")\";`"
  - label: la console affiche « Météo (2025, JavaScript) »
    console: /^Météo \(2025, JavaScript\)$/
  - label: la console affiche « Quiz (2024, CSS) »
    console: /^Quiz \(2024, CSS\)$/
solution: assets/objets.solution
```

Au départ, la console affichait trois fois `undefined` : la fonction était appelée, mais ne rendait rien. C'est le même piège qu'avec `prixTTC`.

## Une classe : un moule pour fabriquer des objets

Quand on fabrique beaucoup d'objets de la même forme, une **classe** sert de moule. Son `constructor` range les valeurs reçues dans l'objet avec **`this`** (« cet objet-ci »), et ses **méthodes** sont des fonctions qui travaillent sur ces valeurs. Le mot-clé **`new`** fabrique un objet à partir du moule :

```javascript
class Rectangle {
  constructor(largeur, hauteur) {
    this.largeur = largeur;
    this.hauteur = hauteur;
  }
  calculAire() {
    return this.largeur * this.hauteur;
  }
}

const premier = new Rectangle(10, 5);
console.log(premier.calculAire()); // 50
```

Dans une méthode, `this.` n'est pas facultatif : `largeur` seul déclenche `ReferenceError: largeur is not defined`, parce que le moteur cherche une variable, pas la valeur rangée dans l'objet. Le lab vous fait écrire cette classe pas à pas.

> 📖 [Les fonctions (MDN)](https://developer.mozilla.org/fr/docs/Web/JavaScript/Guide/Functions) · [Utiliser les objets (MDN)](https://developer.mozilla.org/fr/docs/Web/JavaScript/Guide/Working_with_objects) · [Les classes (MDN)](https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Classes)

## Trois questions pour vérifier ce que vous avez retenu

```quiz
title: "Fonctions et objets"
tracksProgress: false
showNotice: false
place: stage
questions:
  - prompt: "Que rend une fonction qui calcule un résultat et l'affiche avec `console.log`, sans `return` ?"
    answers:
      - "Le résultat calculé"
      - "undefined : afficher n'est pas rendre"
      - "Une erreur rouge"
    correct: 2
    explanation: "console.log écrit dans la console, mais la fonction ne donne rien à celui qui l'appelle : elle rend undefined. Pour réutiliser le résultat, il faut return."
  - prompt: "Dans `addition(5, 3)`, que sont 5 et 3 ?"
    answers:
      - "Les arguments : les valeurs données à l'appel, rangées dans les paramètres a et b"
      - "Les paramètres de la fonction"
      - "Les valeurs rendues par la fonction"
    correct: 1
    explanation: "Les paramètres sont les noms écrits dans la déclaration, (a, b). Les arguments sont les valeurs données à l'appel, ici 5 et 3."
  - prompt: "Avec `const livre = { titre: \"Dune\" };`, que donne `livre.auteur` ?"
    answers:
      - "Une erreur : la clé n'existe pas"
      - "undefined, sans erreur"
      - "Une chaîne vide"
    correct: 2
    explanation: "Lire une clé absente rend undefined, sans message. L'erreur n'arrive que si l'on va chercher dans ce undefined, par exemple livre.auteur.nom."
```

## Récap

- Une **fonction** nomme un bloc de code ; on l'appelle avec des **arguments**, rangés dans ses **paramètres**.
- **`return`** rend un résultat au code appelant ; sans `return`, la fonction rend **`undefined`**, et un calcul fait avec donne `NaN`, sans erreur.
- Un **objet** range des paires clé : valeur ; on lit une valeur avec `objet.cle` ou `objet["cle"]` ; une clé absente vaut `undefined`.
- Un **tableau d'objets** se parcourt avec `for…of` : c'est la forme habituelle des données d'une application.
- Une **classe** est un moule à objets : `constructor`, `this`, des méthodes, et `new` pour fabriquer.

Tout ce que vous avez écrit jusqu'ici parle à la console. Pour lire et changer la page elle-même, JavaScript la voit comme des objets : c'est l'objet du bit [Le DOM : la page vue par JavaScript](https://byte-layers.com/fr/bits/dom).

```ack
J'ai compris
```
