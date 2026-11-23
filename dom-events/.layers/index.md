---
title: "Les événements : réagir aux actions du visiteur"
description: "Une page ne change rien toute seule : elle attend qu'on clique, qu'on tape, qu'on envoie. addEventListener, la fonction qu'on confie sans l'appeler, des onglets, la lecture d'un champ avec value et trim, et le formulaire qui ne recharge pas avec preventDefault."
tags:
  - bit
  - javascript
  - dom
  - web
difficulty: beginner
duration: 25
requires: "0.9.0"
---

Une page ne change rien toute seule : elle **attend** que le visiteur fasse quelque chose, cliquer, taper, envoyer un formulaire. Vous saurez écouter un événement avec `addEventListener`, confier une fonction au navigateur sans l'appeler vous-même (le piège de `f()` à la place de `f`), construire des onglets, lire et valider un champ avec `value` et `trim`, et empêcher un formulaire de recharger la page avec `preventDefault`.

**Prérequis** : [Le DOM : la page vue par JavaScript](https://byte-layers.com/fr/bits/dom), pour `querySelector`, `textContent` et `classList`.

# Les événements : réagir aux actions du visiteur

Avec le DOM seul, le code construit la page au chargement, puis plus rien : un monologue. Ici, la page écoute, et c'est ce qui sépare une page d'une application.

## Écouter un événement : `addEventListener`

Chaque action du visiteur produit un **événement** : un clic, une touche, un champ modifié, un formulaire envoyé. On demande au navigateur de prévenir un élément avec **`addEventListener`** (« ajouter un écouteur ») : le nom de l'événement, puis la fonction à exécuter quand il se produit.

```javascript
const bouton = document.querySelector("#bouton");

function direBonjour() {
  console.log("Bonjour !");
}

bouton.addEventListener("click", direBonjour);
```

Qui appelle `direBonjour`, et quand ?

```scene
lesson: assets/events.scene.json
step: ecouter
```

La fonction confiée au navigateur s'appelle un **écouteur** (*listener*) ou un gestionnaire. Ce n'est pas vous qui l'appelez : c'est le navigateur, à chaque événement, autant de fois qu'il se produit. Les événements les plus courants :

| Événement | Se produit quand… |
|---|---|
| `click` | on clique sur un élément, ou on appuie sur Entrée sur un bouton |
| `input` | le contenu d'un champ (`<input>`, `<textarea>`) change, à chaque lettre |
| `submit` | on envoie un formulaire ; il s'écoute sur le `<form>` |
| `keydown` | on enfonce une touche, dans la page ou dans un champ |

## À toi : un bouton qui répond

La fonction `repondre` est écrite, mais personne ne l'appelle : le bouton ne fait rien. Ajoute **une ligne** à la fin de `script.js` pour que le navigateur l'appelle à chaque clic sur le bouton.

```playground
runtime: web
title: Un bouton qui répond
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Bonjour</title>
      <script src="script.js" defer></script>
    </head>
    <body>
      <button id="saluer">Dire bonjour</button>
      <p id="reponse">En attente d'un clic.</p>
    </body>
    </html>
  script.js: |
    const bouton = document.querySelector("#saluer");
    const reponse = document.querySelector("#reponse");

    function repondre() {
      reponse.textContent = "Bonjour, visiteur !";
    }

    // À toi : demande au navigateur d'appeler repondre à chaque clic sur le bouton
open: [script.js, index.html]
lock: [index.html]
show: [editor, preview, console]
verify:
  - label: "avant tout clic, le paragraphe dit encore « En attente d'un clic. »"
    selector: "#reponse"
    text: "/^En attente/"
    hint: "La fonction ne doit pas s'exécuter au chargement : confie `repondre` au navigateur, sans l'appeler toi-même."
  - label: un clic sur le bouton affiche « Bonjour, visiteur ! »
    click: "#saluer"
    selector: "#reponse"
    text: Bonjour, visiteur !
    hint: "Pose un écouteur sur le bouton : `bouton.addEventListener(\"click\", repondre);`"
  - label: aucune erreur JavaScript
    errors: none
solution: assets/bouton.solution
```

## Confier la fonction, ne pas l'appeler : `f` contre `f()`

Le nom d'une fonction seul, `basculer`, **désigne** la fonction. Suivi de parenthèses, `basculer()`, il l'**appelle**, tout de suite, et vaut ce qu'elle rend. Écrire `addEventListener("click", basculer())` exécute donc `basculer` au chargement de la page, une seule fois, et confie au navigateur ce qu'elle a rendu, `undefined` : le clic n'a plus rien à exécuter.

```scene
lesson: assets/events.scene.json
step: f-ou-f
```

Aucune erreur rouge ne signale ce piège : la fonction a bien tourné, une fois, au mauvais moment. Pour s'en apercevoir, il faut regarder **quand** le code s'exécute : un `console.log` dans la fonction qui s'affiche avant tout clic suffit à le trahir.

## À toi : la lampe qui s'allume toute seule

La lampe ci-dessous s'allume toute seule au chargement, et le bouton ne répond plus. Lis le code, puis corrige **une seule** ligne.

```playground
runtime: web
title: La lampe qui s'allume toute seule
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Lampe</title>
      <link rel="stylesheet" href="style.css">
      <script src="script.js" defer></script>
    </head>
    <body>
      <div id="lampe"></div>
      <p id="etat">La lampe est éteinte</p>
      <button id="bouton">Allumer / Éteindre</button>
    </body>
    </html>
  style.css: |
    #lampe { width: 80px; height: 80px; border-radius: 50%; background-color: rgb(203, 213, 225); }
    #lampe.allumee { background-color: rgb(250, 204, 21); }
  script.js: |
    const lampe = document.querySelector("#lampe");
    const etat = document.querySelector("#etat");
    const bouton = document.querySelector("#bouton");

    function basculer() {
      lampe.classList.toggle("allumee");
      if (lampe.classList.contains("allumee")) {
        etat.textContent = "La lampe est allumée";
      } else {
        etat.textContent = "La lampe est éteinte";
      }
    }

    bouton.addEventListener("click", basculer());
open: [script.js, index.html, style.css]
lock: [index.html, style.css]
show: [editor, preview, console]
verify:
  - label: au chargement, sans clic, la lampe est éteinte
    selector: "#lampe.allumee"
    exists: false
    hint: "Les parenthèses de `basculer()` appellent la fonction dès le chargement. Confie-la sans les parenthèses : `addEventListener(\"click\", basculer)`."
  - label: un clic l'allume
    click: "#bouton"
    selector: "#etat"
    text: La lampe est allumée
  - label: un second clic l'éteint
    click: "#bouton"
    selector: "#lampe.allumee"
    exists: false
  - label: aucune erreur JavaScript
    errors: none
solution: assets/lampe.solution
```

## Plusieurs boutons, un seul panneau : les onglets

Des onglets tiennent en une phrase : **tout éteindre, puis rallumer un seul**. Chaque bouton dit quel panneau il ouvre, dans un attribut **`data-`** que l'on invente soi-même (`data-content-id="content2"`), et que `getAttribute` lit :

```javascript
const id = onglet.getAttribute("data-content-id"); // "content2"
const panneau = document.querySelector("#" + id);  // l'élément d'identifiant content2
```

Voici ce que donne cette règle à chaque clic, avec l'attribut `data-` qui relie chaque bouton à son panneau :

```scene
lesson: assets/events-plan.scene.json
step: onglets
```

On pose un écouteur sur **chaque** onglet, dans une boucle. La fonction donnée à `addEventListener` est alors écrite sur place, **sans nom** (voir [Fonctions et objets](https://byte-layers.com/fr/bits/js-functions-objects)) :

```javascript
for (const onglet of onglets) {
  onglet.addEventListener("click", function () {
    ouvrir(onglet);
  });
}
```

Le navigateur appellera cette fonction sans nom au clic, et c'est elle qui appelle `ouvrir(onglet)` : ses parenthèses sont à l'intérieur, elles ne s'exécutent qu'au clic.

## À toi : fais fonctionner les onglets

Le CSS de la page cache tous les panneaux, sauf celui qui porte la classe `active` ; l'onglet ouvert porte la classe `tab-active`. La boucle des écouteurs est écrite : écris la fonction `ouvrir`, qui reçoit l'onglet cliqué.

```playground
runtime: web
title: Fais fonctionner les onglets
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Onglets</title>
      <link rel="stylesheet" href="style.css">
      <script src="script.js" defer></script>
    </head>
    <body>
      <div class="tabs">
        <button class="tab tab-active" data-content-id="content1">Projets</button>
        <button class="tab" data-content-id="content2">Compétences</button>
        <button class="tab" data-content-id="content3">Contact</button>
      </div>
      <div id="content1" class="tab-content active">Trois projets récents.</div>
      <div id="content2" class="tab-content">HTML, CSS, JavaScript.</div>
      <div id="content3" class="tab-content">Écrivez-moi.</div>
    </body>
    </html>
  style.css: |
    .tab { padding: 8px 16px; border: none; background: none; }
    .tab-active { border-bottom: 3px solid rgb(37, 99, 235); font-weight: 700; }
    .tab-content { display: none; padding: 16px; }
    .tab-content.active { display: block; }
  script.js: |
    const onglets = document.querySelectorAll(".tab");
    const panneaux = document.querySelectorAll(".tab-content");

    function ouvrir(onglet) {
      // 1. éteindre : retirer "active" de tous les panneaux et "tab-active" de tous les onglets
      // 2. rallumer : l'onglet cliqué et le panneau de son data-content-id
    }

    for (const onglet of onglets) {
      onglet.addEventListener("click", function () {
        ouvrir(onglet);
      });
    }
open: [script.js, index.html, style.css]
lock: [index.html, style.css]
show: [editor, preview, console]
check: ask
verify:
  - label: un clic sur « Compétences » affiche son panneau
    click: "[data-content-id=content2]"
    selector: "#content2"
    style: { display: block }
  - label: le panneau « Projets » est alors caché
    click: "[data-content-id=content2]"
    selector: "#content1"
    style: { display: none }
    hint: "Commence par tout éteindre : une boucle sur `panneaux` qui retire la classe `active`."
  - label: après « Contact » puis « Projets », un seul panneau est visible
    click: ["[data-content-id=content3]", "[data-content-id=content1]"]
    selector: ".tab-content.active"
    count: 1
  - label: un seul onglet est souligné à la fois
    click: ["[data-content-id=content3]", "[data-content-id=content2]"]
    selector: ".tab-active"
    count: 1
    hint: "Éteins aussi les onglets : une seconde boucle qui retire `tab-active`, puis `onglet.classList.add(\"tab-active\")`."
  - label: aucune erreur JavaScript
    errors: none
solution: assets/onglets.solution
```

## Lire un champ : `value` et `trim`

Ce que le visiteur a tapé dans un champ se lit dans sa propriété **`value`**, toujours sous forme de texte. Avant de le valider, on retire les espaces du début et de la fin avec **`trim()`** (*rogner*). Suivez un champ rempli d'espaces :

```scene
lesson: assets/events-plan.scene.json
step: trim
```

Sans `trim`, un champ rempli d'espaces passe pour rempli : le test `=== ""` le laisse passer. Avec `trim`, il reste un texte vide, que la validation refuse ; et un mot entouré d'espaces garde son mot, sans les bords.

## À toi : refuse un champ plein d'espaces

Ici, le champ contient déjà trois espaces, et le bouton est un simple bouton (`type="button"`), qui n'envoie rien. Écris la validation : un champ vide ou plein d'espaces affiche « Remplissez le champ. » et pose la classe `erreur` sur le message.

```playground
runtime: web
title: Refuse un champ plein d'espaces
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Contact</title>
      <link rel="stylesheet" href="style.css">
      <script src="script.js" defer></script>
    </head>
    <body>
      <label for="prenom">Prénom</label>
      <input id="prenom" value="   ">
      <button type="button" id="valider">Valider</button>
      <p id="message"></p>
    </body>
    </html>
  style.css: |
    #message { color: rgb(22, 101, 52); }
    #message.erreur { color: rgb(185, 28, 28); }
  script.js: |
    const champ = document.querySelector("#prenom");
    const bouton = document.querySelector("#valider");
    const message = document.querySelector("#message");

    bouton.addEventListener("click", function () {
      // À toi : lis le champ, retire les espaces, puis affiche le bon message
    });
open: [script.js, index.html, style.css]
lock: [index.html, style.css]
show: [editor, preview, console]
check: ask
verify:
  - label: un clic sur « Valider » affiche « Remplissez le champ. »
    click: "#valider"
    selector: "#message"
    text: Remplissez le champ.
    hint: "Si le message dit « Bonjour », les espaces comptent encore : `champ.value.trim()`."
  - label: le message porte alors la classe `erreur`, et devient rouge
    click: "#valider"
    selector: "#message"
    style: { color: "rgb(185, 28, 28)" }
    hint: "`message.classList.add(\"erreur\")` dans le cas du champ vide."
  - label: aucune erreur JavaScript
    errors: none
solution: assets/champ.solution
```

## Un formulaire : `submit` et `preventDefault`

Un formulaire envoyé recharge la page : c'est son comportement par défaut, hérité du temps où chaque envoi partait vers un serveur. Pour le traiter en JavaScript, on écoute **`submit` sur le `<form>`** (qui couvre le bouton et la touche Entrée), et l'on coupe ce comportement avec **`preventDefault()`**, appelé sur l'objet événement que le navigateur passe à l'écouteur :

```javascript
formulaire.addEventListener("submit", function (evenement) {
  evenement.preventDefault(); // la page ne se recharge pas
  const prenom = champPrenom.value.trim();
  if (prenom === "") {
    message.textContent = "Remplissez le champ.";
  } else {
    message.textContent = "Bonjour " + prenom + " !";
  }
});
```

Ce qui se passe à l'envoi, sans puis avec `preventDefault` :

```scene
lesson: assets/events.scene.json
step: submit
```

Sans `preventDefault`, votre code s'exécute bien, puis le rechargement efface tout : la page clignote, la console se vide, et rien ne semble s'être passé. L'aperçu des exercices n'envoie pas de formulaire : le rechargement se constate dans un vrai navigateur, sur votre machine.

> 📖 [Introduction aux événements (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Scripting/Events) · [addEventListener (MDN)](https://developer.mozilla.org/fr/docs/Web/API/EventTarget/addEventListener) · [preventDefault (MDN)](https://developer.mozilla.org/fr/docs/Web/API/Event/preventDefault) · [String.prototype.trim (MDN)](https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Global_Objects/String/trim)

## Trois questions pour vérifier ce que vous avez retenu

```quiz
title: "Les événements"
tracksProgress: false
showNotice: false
place: stage
questions:
  - prompt: "Que se passe-t-il avec `bouton.addEventListener(\"click\", basculer())` ?"
    answers:
      - "basculer s'exécute à chaque clic"
      - "basculer s'exécute une fois, au chargement, et le clic n'a plus rien à exécuter"
      - "Une erreur rouge signale les parenthèses"
    correct: 2
    explanation: "Les parenthèses appellent la fonction tout de suite. addEventListener reçoit ce qu'elle rend, undefined. Il faut confier la fonction elle-même : basculer, sans parenthèses."
  - prompt: "Un champ contient trois espaces. Que vaut `champ.value.trim() === \"\"` ?"
    answers:
      - "true : trim retire les espaces, il reste un texte vide"
      - "false : le champ contient trois caractères"
      - "Une erreur, parce que le champ n'est pas vide"
    correct: 1
    explanation: "trim retire les espaces du début et de la fin. Il ne reste rien : le champ compte comme vide, ce que la validation doit refuser."
  - prompt: "Pourquoi appeler `evenement.preventDefault()` dans l'écouteur `submit` d'un formulaire ?"
    answers:
      - "Pour vider les champs"
      - "Pour empêcher le rechargement de la page, qui effacerait ce que le code vient de faire"
      - "Pour envoyer le formulaire au serveur"
    correct: 2
    explanation: "Par défaut, un formulaire envoyé recharge la page. preventDefault coupe ce comportement : le code traite la saisie, et la page reste en place."
```

## Récap

- Une action du visiteur produit un **événement** ; **`addEventListener("click", f)`** confie la fonction `f` au navigateur, qui l'appelle à chaque événement.
- **`f`** désigne la fonction, **`f()`** l'appelle tout de suite : avec les parenthèses, l'écouteur part au chargement, et le clic ne fait plus rien, sans erreur.
- Des **onglets** : un écouteur par bouton, un attribut **`data-`** lu par `getAttribute`, et la règle « tout éteindre, puis rallumer un seul ».
- **`value`** lit un champ, toujours du texte ; **`trim()`** retire les espaces avant de valider.
- Un formulaire s'écoute sur **`submit`**, et **`preventDefault()`** l'empêche de recharger la page.

Les données de vos pages sont encore écrites dans le code. Le plus souvent, elles arrivent d'un serveur, dans un format texte : c'est l'objet du bit [Données JSON et fetch](https://byte-layers.com/fr/bits/json-fetch).

```ack
J'ai compris
```
