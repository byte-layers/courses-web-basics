---
title: "La console JavaScript : premier contact avec le moteur du navigateur"
description: "Chaque navigateur contient un moteur JavaScript : ouvrir sa console, lui faire calculer et assembler du texte, lire ses trois sortes de réponses, ranger une valeur avec let ou const, et comprendre pourquoi \"5\" + 3 donne \"53\"."
tags:
  - bit
  - javascript
  - web
difficulty: beginner
duration: 15
requires: "0.9.0"
---

Chaque navigateur contient un moteur JavaScript, et sa **console** permet de lui parler tout de suite, sans rien installer ni enregistrer. Vous saurez ouvrir une console, lui faire calculer et assembler du texte, lire ses trois sortes de réponses (une valeur, `undefined`, une erreur), ranger une valeur avec `let` ou `const`, et pourquoi `"5" + 3` donne `"53"`.

**Prérequis** : le bit [sur les trois langages d'une page web](https://byte-layers.com/fr/bits/web-page-languages), pour le rôle de JavaScript à côté de HTML et CSS, et le challenge [portfolio v2](https://byte-layers.com/fr/challenges/portfolio-v2-challenge) : ce cours rend votre portfolio interactif.

# La console JavaScript : premier contact

Votre portfolio dit ce qu'il contient (HTML) et à quoi il ressemble (CSS). Il ne fait encore rien : c'est le rôle du troisième langage, **JavaScript**. Avant de l'écrire dans une page, on le découvre là où il répond aussitôt : la console.

## Un moteur JavaScript dans chaque navigateur

Le navigateur ne fait pas que dessiner des pages : il contient un **moteur JavaScript**, un programme qui lit du code JavaScript et l'exécute. Chrome et Edge utilisent V8, Firefox SpiderMonkey, Safari JavaScriptCore. C'est un interpréteur : il lit une instruction et l'exécute tout de suite, sans étape de compilation à lancer soi-même.

La **console** fait partie des outils de développement du navigateur. On y tape une instruction, on appuie sur Entrée, et le moteur répond sur la ligne suivante. Rien n'est enregistré : un rechargement de la page efface tout.

| Navigateur | Ouvrir la console |
|---|---|
| Chrome, Edge | F12, puis l'onglet **Console** ; ou Ctrl+Maj+J (Cmd+Option+J sous macOS) |
| Firefox | F12, puis l'onglet **Console** ; ou Ctrl+Maj+K (Cmd+Option+K sous macOS) |
| Safari | d'abord, dans **Réglages**, onglet **Avancés**, cochez « Afficher les fonctionnalités pour les développeurs web » ; puis Cmd+Option+C |

Les exercices de ce bit se font dans la **console de l'aperçu**, sous la page : elle se comporte comme celle du navigateur, et vos réponses y sont vérifiées. Le lab du cours vous fera ouvrir la vraie.

> 📖 [La console des outils de développement (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Howto/Tools_and_setup/What_are_browser_developer_tools) · [L'objet console (MDN)](https://developer.mozilla.org/fr/docs/Web/API/console)

## Calculer et assembler du texte

Le moteur sait d'abord **calculer**. Les opérateurs sont ceux de la calculatrice : `+`, `-`, `*` pour multiplier, `/` pour diviser, et `%` pour le reste d'une division (`10 % 3` vaut `1`). Les parenthèses fonctionnent comme en maths. Le séparateur décimal est le **point** : `2.5`, jamais `2,5`.

Il sait aussi manipuler du **texte**, qu'on écrit entre guillemets doubles ou simples : `"Bonjour"` ou `'Bonjour'`. Entre deux textes, le `+` ne calcule pas, il **assemble** : `"Bon" + "jour"` donne `"Bonjour"`. Pour les calculs plus riches, l'objet **`Math`** range des fonctions toutes faites :

| Instruction | Réponse | Ce qu'elle fait |
|---|---|---|
| `Math.round(249.67)` | `250` | arrondit à l'entier le plus proche |
| `Math.max(312, 247, 190)` | `312` | rend le plus grand |
| `Math.random()` | un nombre entre 0 et 1 | tire au hasard, différent à chaque fois |

Taper `7 * 8` dans la console affiche la réponse, `56`. Un programme, lui, n'a personne pour lire ses réponses : il écrit dans la console avec **`console.log(…)`**, qui affiche ce qu'on met entre les parenthèses. C'est un message pour le développeur, que le visiteur de la page ne voit pas.

Dans la console sous l'aperçu, tapez d'abord `7 * 8` et Entrée, pour voir la réponse. Puis faites écrire les trois lignes demandées avec `console.log`.

```playground
runtime: web
title: Calcule et assemble dans la console
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Bac à sable</title>
    </head>
    <body>
      <h1>Bac à sable</h1>
      <p>Tout se passe dans la console, sous cette page.</p>
      <script src="script.js"></script>
    </body>
    </html>
  script.js: |
    // Ce fichier est vide : tape tes instructions dans la console, sous l'aperçu.
open: [script.js, index.html]
lock: [index.html]
show: [editor, preview, console]
verify:
  - label: "`console.log` affiche le résultat de 7 × 8"
    console: /^56$/
    hint: "Tape `console.log(7 * 8)` dans la console, puis Entrée."
  - label: la console affiche « Bonjour Ada », assemblé avec `+`
    console: /^Bonjour Ada$/
    hint: "Deux textes et un `+` : `console.log(\"Bonjour \" + \"Ada\")`. L'espace fait partie du premier texte."
  - label: la console affiche le plus grand de 312, 247 et 190, trouvé par `Math`
    console: /^312$/
    hint: "`console.log(Math.max(312, 247, 190))`"
solution: assets/calcul.solution
```

Les réponses de la console et les lignes de `console.log` ne se ressemblent pas tout à fait : une réponse est précédée d'une marque, une ligne de `console.log` non. Seules les secondes sont vérifiées ici, parce qu'un programme n'écrit que celles-là.

## Trois sortes de réponses : une valeur, `undefined`, une erreur

Chaque instruction tapée reçoit une réponse, et il n'en existe que trois sortes. Savoir les reconnaître, c'est savoir ce que le moteur a compris.

| Vous tapez | La console répond | Ce que ça veut dire |
|---|---|---|
| `2 + 3` | `5` | une **valeur** : le résultat de l'instruction |
| `console.log("Salut")` | `Salut`, puis `undefined` | la ligne écrite, puis la réponse : `console.log` écrit, mais ne rend aucune valeur, d'où **`undefined`** (« pas de valeur ») |
| `Bonjour` | `ReferenceError: Bonjour is not defined` | une **erreur**, en rouge : sans guillemets, le moteur cherche une variable nommée `Bonjour`, et n'en trouve pas |
| `"Bonjour` | une `SyntaxError` | une erreur de syntaxe : le texte n'est jamais refermé |

Une erreur en rouge n'est pas le pire des cas. Tapez `3,5 + 1` : la console répond `6`, sans aucun message. La virgule n'est pas un séparateur décimal en JavaScript ; le moteur lit « 3, puis 5 + 1 » et garde le dernier. **Un résultat faux et silencieux** est plus dangereux qu'une erreur, parce que rien ne vous alerte.

> 💡 **Remarque.** Le message d'erreur est en anglais et nomme ce qui manque : `is not defined` (« n'est pas défini »). Lire ce message avant de relire son code fait gagner beaucoup de temps.

## Le texte et les nombres : `"5" + 3`

Toute valeur a un **type**, que donne `typeof` : `typeof 25` répond `"number"` (un nombre), `typeof "25"` répond `"string"` (une chaîne de caractères, du texte), `typeof true` répond `"boolean"` (vrai ou faux). Les guillemets décident : `25` est un nombre, `"25"` est un texte qui contient deux chiffres.

Ce n'est pas un détail. Quand un `+` voit un texte d'un côté, il **assemble** au lieu d'additionner : `"5" + 3` donne `"53"`. Or tout ce qu'un visiteur saisit arrive sous forme de texte. La fonction **`prompt("Quel âge avez-vous ?")`** ouvre une boîte de dialogue avec un champ, et rend ce qu'on y a tapé : du texte, toujours, même s'il ne contient que des chiffres (ou `null` si l'on clique sur Annuler). Pour calculer, on convertit avec **`Number(…)`** : `Number("25")` vaut le nombre `25`.

Les boîtes de dialogue (`alert` pour un message, `confirm` pour OK ou Annuler, `prompt` pour une saisie) attendent une réponse humaine, que les vérifications ne savent pas donner : vous les utiliserez dans le lab. Ici, `script.js` contient déjà une variable `ageSaisi`, avec la valeur que `prompt` aurait rendue pour quelqu'un qui tape 25. Tapez les trois instructions dans la console, et regardez ce que donne la première.

```playground
runtime: web
title: Le piège du texte qui ressemble à un nombre
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Bac à sable</title>
    </head>
    <body>
      <h1>Quel âge avez-vous ?</h1>
      <script src="script.js"></script>
    </body>
    </html>
  script.js: |
    // La valeur que prompt("Quel âge avez-vous ?") rendrait pour quelqu'un qui tape 25
    const ageSaisi = "25";
open: [script.js, index.html]
lock: [index.html]
show: [editor, preview, console]
verify:
  - label: "`console.log(ageSaisi + 1)` affiche l'âge de l'an prochain… ou pas"
    console: /^251$/
    hint: "Tape `console.log(ageSaisi + 1)` et lis le résultat : ce n'est pas 26."
  - label: "`typeof` dit de quel type est `ageSaisi`"
    console: /^string$/
    hint: "`console.log(typeof ageSaisi)`"
  - label: la console affiche 26, après conversion avec `Number`
    console: /^26$/
    hint: "Convertis d'abord, ajoute ensuite : `console.log(Number(ageSaisi) + 1)`."
solution: assets/texte.solution
```

`ageSaisi + 1` donne `251` : le `+` a vu un texte, il a collé le `1` au bout. Pas d'erreur, juste un résultat faux. Après `Number(ageSaisi)`, le `+` voit deux nombres et additionne. Ce piège revient dans tout le cours, à chaque saisie.

## Ranger une valeur : `let` et `const`

Une **variable** est un nom qui désigne une valeur, pour la réutiliser plus loin. On la crée avec un mot-clé, puis le signe `=`, qui **range** la valeur à droite dans le nom à gauche (ce n'est pas une égalité au sens des maths) :

```javascript
const PRIX_ABONNEMENT = 24; // une constante : sa valeur ne changera pas
let nombreEmprunts = 3;     // une variable : sa valeur pourra changer
nombreEmprunts = nombreEmprunts + 1; // on reprend la valeur actuelle, on ajoute 1, on range : 4
```

| Mot-clé | Ce qu'il crée | Changer la valeur ensuite |
|---|---|---|
| **`const`** | une constante | interdit : `TypeError: Assignment to constant variable.` |
| **`let`** | une variable modifiable | permis, sans réécrire `let` |

Le bon réflexe : `const` par défaut, `let` seulement quand la valeur doit changer. Le moteur vous protège alors d'un changement par erreur. Le `;` termine une instruction, et `//` commence un commentaire, que le moteur ignore.

Les deux lignes de départ sont dans `script.js`. Dans la console, ajoutez 1 à `nombreEmprunts`, affichez le résultat, puis essayez de changer `PRIX_ABONNEMENT`, pour lire l'erreur.

```playground
runtime: web
title: Une variable qui change, une constante qui refuse
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Médiathèque</title>
    </head>
    <body>
      <h1>Médiathèque</h1>
      <script src="script.js"></script>
    </body>
    </html>
  script.js: |
    const PRIX_ABONNEMENT = 24;
    let nombreEmprunts = 3;
open: [script.js, index.html]
lock: [index.html]
show: [editor, preview, console]
verify:
  - label: "la console affiche « Emprunts : 4 », après un ajout de 1 à `nombreEmprunts`"
    console: "/^Emprunts : 4$/"
    hint: "Deux instructions : `nombreEmprunts = nombreEmprunts + 1`, puis `console.log(\"Emprunts :\", nombreEmprunts)`. La virgule entre les deux valeurs de `console.log` ajoute un espace."
solution: assets/variables.solution
```

Tapez ensuite `PRIX_ABONNEMENT = 30` : la console répond en rouge `TypeError: Assignment to constant variable.` C'est `const` qui fait son travail.

> 💡 **Remarque.** Dans la console de l'exercice, une variable créée avec `let` ou `const` sur une ligne n'est plus visible à la ligne suivante ; la console du navigateur, elle, la garde. C'est pourquoi les variables de ces exercices sont créées dans `script.js`.

> 📖 [Les types et les variables (MDN)](https://developer.mozilla.org/fr/docs/Web/JavaScript/Guide/Grammar_and_types) · [Number() (MDN)](https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Global_Objects/Number) · [Math (MDN)](https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Global_Objects/Math)

## Trois questions pour vérifier ce que vous avez retenu

```quiz
title: "La console JavaScript"
tracksProgress: false
showNotice: false
place: stage
questions:
  - prompt: "Dans la console, vous tapez `3,5 + 1`. Que se passe-t-il ?"
    answers:
      - "La console répond 4.5"
      - "La console répond 6, sans erreur : la virgule n'est pas un séparateur décimal"
      - "Une erreur rouge signale la virgule"
    correct: 2
    explanation: "Le séparateur décimal est le point. Avec une virgule, le moteur évalue 3, puis 5 + 1, et garde le dernier : 6. Aucun message ne vous prévient."
  - prompt: "Un visiteur tape 25 dans une boîte `prompt`, et le programme calcule `saisie + 1`. Que vaut le résultat ?"
    answers:
      - "26"
      - "\"251\", parce que prompt rend du texte et que + assemble les textes"
      - "Une erreur, parce qu'on ne peut pas additionner un texte"
    correct: 2
    explanation: "prompt rend toujours du texte. Avec un texte d'un côté, + assemble : \"25\" + 1 donne \"251\". Il faut convertir avec Number(saisie) avant de calculer."
  - prompt: "Que se passe-t-il quand on écrit `PRIX = 30` après `const PRIX = 24` ?"
    answers:
      - "PRIX vaut désormais 30"
      - "Le moteur refuse : TypeError, on ne change pas la valeur d'une constante"
      - "Rien : la ligne est ignorée sans message"
    correct: 2
    explanation: "const crée une constante : toute nouvelle valeur est refusée par une TypeError. Pour une valeur qui doit changer, on utilise let."
```

## Récap

- Chaque navigateur contient un **moteur JavaScript** ; sa **console** exécute une instruction dès qu'on appuie sur Entrée.
- La console répond par une **valeur**, par **`undefined`** (pas de valeur) ou par une **erreur** en rouge, qui nomme ce qui manque. Un résultat faux sans erreur, comme `3,5 + 1`, est le cas le plus dangereux.
- **`console.log(…)`** écrit une ligne dans la console : c'est ainsi qu'un programme parle au développeur.
- `"25"` est un texte, `25` un nombre : `"5" + 3` donne `"53"`. Ce qu'on saisit (`prompt`) est toujours du texte, à convertir avec **`Number(…)`**.
- **`const`** crée une constante, **`let`** une variable modifiable ; `=` range une valeur dans un nom.

Ce que vous tapez dans la console disparaît au rechargement. Pour qu'un programme se rejoue à chaque ouverture de la page, il faut l'écrire dans la page : c'est l'objet du bit [Où vit le JavaScript dans une page](https://byte-layers.com/fr/bits/js-in-page).

```ack
J'ai compris
```
