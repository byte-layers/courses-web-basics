---
title: "Données JSON et fetch : charger des données depuis un serveur"
description: "Les données d'une page arrivent souvent d'un serveur, en JSON : un texte qui décrit des objets et des tableaux. JSON.parse et JSON.stringify, fetch et ses promesses, async et await, et le piège du fetch qui ne bloque pas : la donnée n'est pas encore là à la ligne suivante."
tags:
  - bit
  - javascript
  - json
  - web
difficulty: beginner
duration: 25
requires: "0.9.0"
---

Les données d'une page ne sont pas forcément écrites dans son code : elles arrivent souvent d'un serveur, dans un format texte, le **JSON**. Vous saurez lire et écrire du JSON, passer du texte à l'objet avec `JSON.parse` et `JSON.stringify`, demander un fichier au serveur avec `fetch`, et éviter le piège central : `fetch` ne bloque pas, la donnée n'est pas encore là à la ligne suivante.

**Prérequis** : [Fonctions et objets](https://byte-layers.com/fr/bits/js-functions-objects), pour les tableaux d'objets et la forme fléchée, et [Le DOM : la page vue par JavaScript](https://byte-layers.com/fr/bits/dom), pour construire une liste avec `createElement`.

# Données JSON et fetch

Le navigateur demande une page à un serveur et reçoit du texte : c'est ainsi que tout a commencé, avec le HTML. Une page déjà affichée peut refaire la même chose pour ses données : demander une liste de projets, recevoir du texte, et s'en servir pour se remplir.

## JSON : des données écrites en texte

Le **JSON** (*JavaScript Object Notation*) écrit des objets et des tableaux sous forme de texte, avec presque la même syntaxe que JavaScript. C'est le format qu'utilisent la plupart des serveurs pour envoyer des données à une page. Voici un objet, et le même écrit en JSON :

```scene
lesson: assets/json.scene.json
step: json
```

Une liste de projets, telle qu'un serveur l'enverrait :

```json
[
  { "titre": "Portfolio", "annee": 2026, "techno": "HTML" },
  { "titre": "Météo", "annee": 2025, "techno": "JavaScript" }
]
```

Retenez les quatre règles de la scène : clés et textes entre guillemets doubles, pas de virgule après le dernier élément, seulement des données.

## Du texte à l'objet : `JSON.parse`

Un JSON reçu est un **texte**, pas un objet : on ne peut pas y lire une clé avec un point. Regardez ce que donne `texte.titre`, puis la même lecture après `JSON.parse` :

```scene
lesson: assets/fetch.scene.json
step: parse
```

Deux fonctions font le passage, dans un sens et dans l'autre :

| Fonction | Ce qu'elle fait |
|---|---|
| `JSON.parse(texte)` | reçoit un texte JSON, rend l'objet ou le tableau qu'il décrit |
| `JSON.stringify(valeur)` | reçoit un objet ou un tableau, rend son texte JSON, à envoyer ou à ranger |

## À toi : du texte JSON à l'objet

La variable `texte` contient ce qu'un serveur a envoyé. La console affiche `Titre : undefined` : fais-lui afficher le vrai titre.

```playground
runtime: web
title: Du texte JSON à l'objet
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>JSON</title>
      <script src="script.js" defer></script>
    </head>
    <body>
      <h1>Un livre reçu du serveur</h1>
    </body>
    </html>
  script.js: |
    // Ce que le serveur a envoyé : du texte
    const texte = '{"titre": "Dune", "auteur": "Frank Herbert", "pages": 900}';

    console.log("Titre :", texte.titre);
open: [script.js, index.html]
lock: [index.html]
show: [editor, preview, console]
verify:
  - label: "la console affiche « Titre : Dune »"
    console: "/^Titre : Dune$/"
    hint: "Un texte n'a pas de clé `titre`. Transforme-le d'abord en objet : `const livre = JSON.parse(texte);`, puis lis `livre.titre`."
  - label: le texte est transformé avec `JSON.parse`
    file: script.js
    includes: JSON.parse(texte)
solution: assets/parse.solution
```

`texte.titre` valait `undefined` : le texte contient bien les caractères « titre », mais une chaîne n'a pas de propriété de ce nom. Après `JSON.parse`, on a un objet, et la notation à point fonctionne.

## `fetch` : demander un fichier, sans attendre la réponse

**`fetch(adresse)`** demande au serveur la ressource qui se trouve à cette adresse : un fichier `projets.json` à côté de la page, ou l'adresse d'une API. La réponse met du temps à venir, quelques millisecondes ou plusieurs secondes. Pendant ce temps, le navigateur ne bloque pas la page : `fetch` rend tout de suite une **promesse** (*Promise*), un objet qui dit « la réponse arrivera », et le code continue à la ligne suivante.

On indique ce qu'il faudra faire de la réponse avec **`.then(…)`**, qui reçoit une fonction, écrite ici en **forme fléchée** (voir [Fonctions et objets](https://byte-layers.com/fr/bits/js-functions-objects)). Le navigateur l'appellera **plus tard**, quand la réponse sera là :

```javascript
fetch("projets.json")
  .then((reponse) => reponse.json())
  .then((projets) => {
    console.log(projets.length + " projets reçus");
  });
console.log("Demande envoyée");
```

Dans quel ordre ces lignes s'exécutent-elles ?

```scene
lesson: assets/fetch.scene.json
step: fetch
```

| Morceau | Rôle |
|---|---|
| `fetch("projets.json")` | envoie la demande, rend une promesse de réponse |
| `(reponse) => reponse.json()` | une fonction fléchée : elle reçoit la réponse et rend la lecture de son corps en JSON, une seconde promesse |
| `.then((projets) => { … })` | quand le JSON est lu, reçoit le tableau d'objets : c'est ici, et seulement ici, qu'on s'en sert |

La console affiche d'abord `Demande envoyée`, puis `3 projets reçus` : la dernière ligne du code s'exécute **avant** la fonction du `.then`. C'est tout le piège.

## À toi : la liste qui reste vide

La page doit afficher les projets de `projets.json`. Le code les demande, mais la liste reste vide et la console annonce 0 projet. Déplace ce qu'il faut pour que la page se remplisse.

```playground
runtime: web
title: La liste qui reste vide
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
      <ul id="projets"></ul>
    </body>
    </html>
  projets.json: |
    [
      { "titre": "Portfolio", "annee": 2026 },
      { "titre": "Météo", "annee": 2025 },
      { "titre": "Quiz", "annee": 2024 }
    ]
  script.js: |
    const liste = document.querySelector("#projets");

    function afficher(projets) {
      for (const projet of projets) {
        const li = document.createElement("li");
        li.textContent = projet.titre + " (" + projet.annee + ")";
        liste.append(li);
      }
    }

    let projets = [];
    fetch("projets.json")
      .then((reponse) => reponse.json())
      .then((donnees) => {
        projets = donnees;
      });

    console.log("Projets chargés :", projets.length);
    afficher(projets);
open: [script.js, projets.json, index.html]
lock: [index.html, projets.json]
show: [editor, preview, console]
check: ask
verify:
  - label: la liste affiche les trois projets
    selector: "#projets li"
    count: 3
    hint: "Les deux dernières lignes s'exécutent avant l'arrivée des données. Déplace-les dans la fonction du second `.then`, après `projets = donnees;`."
  - label: "la console affiche « Projets chargés : 3 »"
    console: "/^Projets chargés : 3$/"
  - label: aucune erreur JavaScript
    errors: none
solution: assets/fetch.solution
```

Au départ, `afficher(projets)` s'exécutait pendant que la demande voyageait encore : `projets` était le tableau vide du début. Les données sont bien arrivées ensuite, mais plus personne ne s'en servait. Tout ce qui dépend des données va **dans** le `.then`.

## `async` et `await` : la même chose, plus lisible

Une autre écriture fait la même chose. Dans une fonction déclarée **`async`**, le mot **`await`** devant une promesse met cette fonction en pause jusqu'à la réponse, sans bloquer la page :

```javascript
async function charger() {
  const reponse = await fetch("projets.json");
  if (!reponse.ok) {
    console.error("Erreur HTTP " + reponse.status);
    return;
  }
  const projets = await reponse.json();
  afficher(projets);
}

charger();
console.log("Chargement lancé");
```

Suivez la fonction `charger`, puis la même demande vers un fichier absent :

```scene
lesson: assets/fetch.scene.json
step: await
```

Deux `await` : le premier attend la réponse du serveur (son statut, `200` ou `404`), le second la lecture du JSON. Un fichier introuvable ne fait pas échouer `fetch` : la réponse arrive, avec le statut `404`, d'où le test de **`reponse.ok`**, qui vaut `true` pour un statut de succès.

> ⚠️ **`fetch` a besoin d'un serveur.** Une page ouverte par un double-clic a une adresse en `file://` : le navigateur y refuse `fetch("projets.json")`. Il faut servir le dossier par un petit serveur local, en `http://`.

## À toi : réécris le chargement avec `async` et `await`

Ce code charge une liste de livres avec `.then`, et il fonctionne. Réécris le chargement dans une fonction `async`, avec deux `await` et sans aucun `.then` : la page doit afficher les mêmes trois livres.

```playground
runtime: web
title: Le chargement, avec async et await
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Mes livres</title>
      <script src="script.js" defer></script>
    </head>
    <body>
      <h1>Mes livres</h1>
      <ul id="livres"></ul>
    </body>
    </html>
  livres.json: |
    [
      { "titre": "Dune", "auteur": "Frank Herbert" },
      { "titre": "Fondation", "auteur": "Isaac Asimov" },
      { "titre": "Hypérion", "auteur": "Dan Simmons" }
    ]
  script.js: |
    const liste = document.querySelector("#livres");

    function afficher(livres) {
      for (const livre of livres) {
        const li = document.createElement("li");
        li.textContent = livre.titre + ", " + livre.auteur;
        liste.append(li);
      }
    }

    fetch("livres.json")
      .then((reponse) => reponse.json())
      .then((livres) => {
        console.log("Livres chargés :", livres.length);
        afficher(livres);
      });
open: [script.js, livres.json, index.html]
lock: [index.html, livres.json]
show: [editor, preview, console]
check: ask
verify:
  - label: le chargement n'utilise plus `.then`
    file: script.js
    excludes: .then(
    hint: "Écris une fonction `async function charger() { … }`, puis appelle-la : `charger();`."
  - label: la réponse est attendue avec `await fetch`
    file: script.js
    includes: await fetch(
    hint: "`const reponse = await fetch(\"livres.json\");`, puis `const livres = await reponse.json();`"
  - label: la liste affiche les trois livres
    selector: "#livres li"
    count: 3
    hint: "Sans le second `await`, `livres` est encore une promesse, pas un tableau."
  - label: "la console affiche « Livres chargés : 3 »"
    console: "/^Livres chargés : 3$/"
  - label: aucune erreur JavaScript
    errors: none
solution: assets/await.solution
```

> 📖 [Utiliser fetch (MDN)](https://developer.mozilla.org/fr/docs/Web/API/Fetch_API/Using_Fetch) · [Manipuler du JSON (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Scripting/JSON) · [Les promesses, async et await (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Extensions/Async_JS/Promises)

## Trois questions pour vérifier ce que vous avez retenu

```quiz
title: "JSON et fetch"
tracksProgress: false
showNotice: false
place: stage
questions:
  - prompt: "Que donne `JSON.stringify({ titre: \"Dune\" })` ?"
    answers:
      - "Un objet, identique au premier"
      - "Le texte {\"titre\":\"Dune\"}, à envoyer ou à ranger"
      - "Une erreur, parce que la clé n'a pas de guillemets"
    correct: 2
    explanation: "JSON.stringify transforme un objet en texte JSON, avec les clés entre guillemets doubles. JSON.parse fait le chemin inverse."
  - prompt: "Un code écrit `fetch(\"data.json\").then(…)`, puis `console.log(donnees)` à la ligne suivante. Pourquoi `donnees` est-il encore vide ?"
    answers:
      - "Parce que le fichier n'existe pas"
      - "Parce que fetch ne bloque pas : la ligne suivante s'exécute avant l'arrivée de la réponse"
      - "Parce que console.log ne sait pas afficher un tableau"
    correct: 2
    explanation: "fetch rend tout de suite une promesse et le code continue. La fonction du .then s'exécute plus tard, à l'arrivée des données : c'est là qu'il faut s'en servir."
  - prompt: "Le serveur répond 404 à une demande `fetch`. Que se passe-t-il ?"
    answers:
      - "fetch échoue avec une erreur"
      - "La réponse arrive normalement, avec reponse.ok à false : c'est au code de le tester"
      - "La page se recharge"
    correct: 2
    explanation: "Un statut d'erreur HTTP est une réponse comme une autre pour fetch. Seul un problème réseau le fait échouer ; le 404 se détecte avec reponse.ok."
```

## Récap

- Le **JSON** est un texte qui décrit des objets et des tableaux : clés et textes entre guillemets doubles, pas de virgule finale, pas de fonction.
- **`JSON.parse`** transforme un texte JSON en objet, **`JSON.stringify`** fait l'inverse ; on ne lit pas de clé dans un texte.
- **`fetch(adresse)`** demande une ressource et rend une **promesse** ; **`.then`** donne la fonction à appeler à l'arrivée des données.
- `fetch` **ne bloque pas** : tout ce qui utilise les données va dans le `.then`, ou après un **`await`** dans une fonction `async`.
- Un statut `404` ne fait pas échouer `fetch` : on teste **`reponse.ok`**. Et `fetch` vers un fichier local demande un serveur, pas une page ouverte en `file://`.

Pour tout refaire sur votre machine, avec la vraie console du navigateur, un éditeur et des fichiers que vous créez vous-même : [Les bases de JavaScript, sur votre machine](https://byte-layers.com/fr/labs/js-basics-lab).

```ack
J'ai compris
```
