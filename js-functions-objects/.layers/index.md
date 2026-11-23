---
title: "Fonctions et objets en JavaScript"
description: "Nommer un geste une fois avec une fonction, ses paramètres et son return  ; la fonction sans nom et sa forme fléchée ; décrire une chose par plusieurs valeurs avec un objet, et parcourir un tableau d'objets ; le piège du return oublié, qui rend undefined."
tags:
  - bit
  - javascript
  - web
difficulty: beginner
duration: 20
requires: "0.9.0"
---

Ce que vous répétez, vous le nommez une fois ; ce que vous décrivez, vous le rangez ensemble. Vous saurez écrire une **fonction** avec ses paramètres, lui faire rendre un résultat avec `return`, décrire une chose par un **objet** (`{ titre: "Dune", pages: 900 }`), parcourir un tableau d'objets, écrire une fonction sans nom ou en forme fléchée (`(n) => n * 2`), et reconnaître le piège du `return` oublié : la fonction calcule, mais rend `undefined`.

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

Suivez l'appel `addition(5, 3)`, puis `addition(2, 2)` :

```scene
lesson: assets/functions.scene.json
step: appel
```

| Morceau | Rôle |
|---|---|
| `function addition` | déclare une fonction nommée `addition` |
| `(a, b)` | les **paramètres** : des noms qui recevront les valeurs données à l'appel |
| `return a + b;` | **rend** la valeur calculée à celui qui a appelé, et termine la fonction |
| `addition(5, 3)` | l'**appel** : 5 et 3 sont les **arguments**, rangés dans `a` et `b` |

Vous avez déjà appelé des fonctions toutes faites : `console.log(…)`, `Number(…)`, `Math.max(…)`. Déclarer la vôtre, c'est ajouter un mot au langage.

## À toi : écris ta première fonction

Déclare une fonction `carre`, qui reçoit un nombre et **rend** ce nombre multiplié par lui-même. Puis affiche dans la console `carre(4)` et `carre(7)` : la même fonction, appelée deux fois.

```playground
runtime: web
title: Ta première fonction
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Carrés</title>
      <script src="script.js" defer></script>
    </head>
    <body>
      <h1>Carrés</h1>
    </body>
    </html>
  script.js: |
    // À toi : déclare la fonction carre(n), qui rend n * n

    // puis affiche carre(4) et carre(7) dans la console
open: [script.js, index.html]
lock: [index.html]
show: [editor, preview, console]
check: ask
verify:
  - label: la console affiche 16
    console: "/^16$/"
    hint: "Déclare `function carre(n) { … }` avec `return n * n;` dedans, puis écris `console.log(carre(4));`."
  - label: la console affiche 49
    console: "/^49$/"
  - label: "`carre` rend son résultat avec `return`"
    file: script.js
    includes: /return\s/
    hint: "Le résultat doit être **rendu** par la fonction, avec `return`, pas affiché à l'intérieur."
  - label: "les deux nombres viennent de deux appels à `carre`"
    file: script.js
    includes: /carre\(\s*4\s*\)[\s\S]*carre\(\s*7\s*\)/
    hint: "Appelle la fonction : `carre(4)`, puis `carre(7)`, sans écrire 16 ni 49 à la main."
solution: assets/carre.solution
```

Le nom `n` ne vaut rien tant que personne n'appelle la fonction : il reçoit 4 au premier appel, 7 au second.

## `return` : rendre un résultat, pas l'afficher

Afficher un résultat et le rendre sont deux choses différentes. `console.log` l'écrit dans la console, pour vous ; **`return`** le donne au code qui a appelé la fonction, qui peut alors s'en servir : le multiplier, le comparer, l'afficher dans la page. Une fonction sans `return` rend **`undefined`**.

```scene
lesson: assets/functions.scene.json
step: return
```

Une fonction qui ne fait qu'afficher ne se réutilise nulle part : son résultat reste dans la console, et le code qui l'appelle ne reçoit rien.

## À toi : la fonction qui calcule mais ne rend rien

La fonction `prixTTC` ci-dessous calcule bien le prix augmenté de 20 %, mais la dernière ligne affiche `NaN` (*Not a Number*, « pas un nombre »). Lis la console, puis corrige la fonction pour que deux abonnements coûtent 60.

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

La console affichait bien `30` : la fonction faisait le calcul, mais ne le donnait à personne. `prixTTC(25)` valait `undefined`, et `undefined * 2` donne `NaN`, sans erreur rouge.

## Un objet : ranger une description

Un **objet** regroupe plusieurs valeurs qui décrivent une même chose. Il s'écrit entre accolades, avec des paires **clé : valeur** séparées par des virgules :

```javascript
const livre = { titre: "Dune", auteur: "Frank Herbert", pages: 900 };

console.log(livre.titre);      // Dune : la notation à point
console.log(livre["auteur"]);  // Frank Herbert : la notation à crochets
console.log(livre.editeur);    // undefined : la clé n'existe pas
livre.editeur = "Pocket";      // ajoute une clé
```

L'objet range une case par clé : on lit une valeur par son nom, et une clé nouvelle s'ajoute.

```scene
lesson: assets/functions.scene.json
step: objet
```

| Écriture | Ce qu'elle fait |
|---|---|
| `livre.titre` | lit la valeur de la clé `titre` |
| `livre["auteur"]` | même chose, la clé écrite comme un texte : utile quand elle est dans une variable |
| `livre.editeur` | une clé absente rend `undefined`, sans erreur |
| `livre.editeur.nom` | aller chercher **dans** `undefined` lève une erreur : `TypeError: Cannot read properties of undefined` |

## À toi : lis un objet

Le code doit afficher le titre et le réalisateur du film. La console répond deux fois `undefined`, sans erreur : compare les clés lues avec celles de l'objet, puis corrige les deux lectures.

```playground
runtime: web
title: Lis un objet
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Mon film</title>
      <script src="script.js" defer></script>
    </head>
    <body>
      <h1>Mon film</h1>
    </body>
    </html>
  script.js: |
    const film = { titre: "Le Voyage de Chihiro", annee: 2001, realisateur: "Hayao Miyazaki" };

    console.log(film.Titre);
    console.log(film.realisatuer);
open: [script.js, index.html]
lock: [index.html]
show: [editor, preview, console]
verify:
  - label: la console affiche « Le Voyage de Chihiro »
    console: "/^Le Voyage de Chihiro$/"
    hint: "Une clé s'écrit exactement comme dans l'objet, majuscules comprises : `titre`, pas `Titre`."
  - label: la console affiche « Hayao Miyazaki »
    console: "/^Hayao Miyazaki$/"
    hint: "Relis l'orthographe de la clé lue, lettre par lettre, avec celle de l'objet."
  - label: les deux valeurs sont lues dans l'objet, pas recopiées
    file: script.js
    excludes: /console\.log\(\s*["'`]/
    hint: "Garde `console.log(film.…)` : c'est la clé qu'il faut corriger, pas la ligne à remplacer par le texte."
solution: assets/lire.solution
```

Une clé mal écrite ne lève aucune erreur : le moteur cherche une clé qui n'existe pas, et rend `undefined`. Quand une valeur manque, relis d'abord le nom de la clé.

## Un tableau d'objets : une liste de descriptions

Les objets se rangent dans des tableaux : un **tableau d'objets** est la forme la plus courante des données d'une application, une liste de livres, de contacts, de projets. On le parcourt avec `for…of` :

```javascript
const livres = [
  { titre: "Dune", pages: 900 },
  { titre: "Le Hobbit", pages: 320 },
  { titre: "Fondation", pages: 280 }
];

for (const livre of livres) {
  console.log(livre.titre);
}
```

La scène suit les trois tours de la boucle, un par objet du tableau :

```scene
lesson: assets/functions.scene.json
step: liste
```

À chaque tour, `livre` reçoit un **objet entier**, avec toutes ses clés : `livre.titre` lit le titre de l'objet du tour, `livre.pages` lirait son nombre de pages.

## À toi : décris chaque projet

Une liste de projets est décrite par trois objets. Écris la fonction `decrire`, qui reçoit un projet et **rend** un texte de la forme `Portfolio (2026, HTML)` ; la boucle du bas l'appelle pour chaque projet.

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

> 📖 [Les fonctions (MDN)](https://developer.mozilla.org/fr/docs/Web/JavaScript/Guide/Functions) · [Utiliser les objets (MDN)](https://developer.mozilla.org/fr/docs/Web/JavaScript/Guide/Working_with_objects) · [Les fonctions fléchées (MDN)](https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Functions/Arrow_functions)

## Une fonction sans nom, et la forme fléchée

Une fonction n'a pas toujours besoin d'un nom : `function (n) { … }`, sans nom, est une **valeur**, comme un nombre ou un texte. On la range dans une variable, ou on la donne à une autre fonction qui l'appellera plus tard. Elle a aussi une écriture plus courte, la **forme fléchée** (*arrow function*). Suivez la même fonction, écrite quatre fois :

```scene
lesson: assets/fleche.scene.json
step: fleche
```

Les quatre écritures font le même travail. La forme fléchée courte, sans accolades, ne vaut que pour un seul calcul à rendre : dès qu'il y a des accolades, `return` redevient obligatoire.

## À toi : écris-la en flèche

La fonction `saluer` est rangée dans une variable, écrite avec `function`. Réécris-la en **forme fléchée**, sans le mot `function` : la console doit toujours afficher « Bonjour Léa ».

```playground
runtime: web
title: Écris-la en flèche
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Salut</title>
      <script src="script.js" defer></script>
    </head>
    <body>
      <h1>Salut</h1>
    </body>
    </html>
  script.js: |
    const saluer = function (prenom) {
      return "Bonjour " + prenom;
    };

    console.log(saluer("Léa"));
open: [script.js, index.html]
lock: [index.html]
show: [editor, preview, console]
check: ask
verify:
  - label: la console affiche « Bonjour Léa »
    console: /^Bonjour Léa$/
    hint: "Si la console affiche `undefined`, la flèche a gardé ses accolades mais perdu son `return` : garde les deux, ou retire les deux."
  - label: "`saluer` est écrite en forme fléchée, sans le mot `function`"
    file: script.js
    includes: /=>/
    excludes: /\bfunction\b/
    hint: "Retire `function`, et place `=>` juste après les parenthèses des paramètres : `(prenom) => …`."
solution: assets/fleche.solution
```

L'appel `saluer("Léa")` n'a pas changé : seule l'écriture de la fonction change, pas la façon de s'en servir.

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
- Une fonction **sans nom** est une valeur : on la range dans une variable ou on la donne à une autre fonction ; sa **forme fléchée** s'écrit `(n) => n * 2`.

Tout ce que vous avez écrit jusqu'ici parle à la console. Pour lire et changer la page elle-même, JavaScript la voit comme des objets : c'est l'objet du bit [Le DOM : la page vue par JavaScript](https://byte-layers.com/fr/bits/dom).

```ack
J'ai compris
```
