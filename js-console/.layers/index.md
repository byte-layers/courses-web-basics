---
title: "La console JavaScript : premier contact avec le moteur du navigateur"
description: "Chaque navigateur contient un moteur JavaScript : ouvrir sa console, lui faire calculer et assembler du texte, lire ses trois sortes de réponses, ranger une valeur avec let ou const, et comprendre pourquoi \"5\" + 3 donne \"53\"."
tags:
  - bit
  - javascript
  - web
difficulty: beginner
duration: 20
requires: "0.9.0"
---

Chaque navigateur contient un moteur JavaScript, et sa **console** permet de lui parler tout de suite, sans rien installer ni enregistrer. Vous saurez ouvrir une console, lui faire calculer et assembler du texte, lire ses trois sortes de réponses (une valeur, `undefined`, une erreur), ranger une valeur avec `let` ou `const`, et pourquoi `"5" + 3` donne `"53"`.

**Prérequis** : le bit [sur les trois langages d'une page web](https://byte-layers.com/fr/bits/web-page-languages), pour le rôle de JavaScript à côté de HTML et CSS.

# La console JavaScript : premier contact

Une page écrite en HTML et CSS dit ce qu'elle contient et à quoi elle ressemble. Elle ne fait encore rien : c'est le rôle du troisième langage, **JavaScript**. Avant de l'écrire dans une page, on le découvre là où il répond aussitôt : la console.

## Un moteur JavaScript dans chaque navigateur

Le navigateur ne fait pas que dessiner des pages : il contient un **moteur JavaScript**, un programme qui lit du code JavaScript et l'exécute. Que se passe-t-il quand on lui parle ?

```scene
lesson: assets/console.scene.json
step: moteur
```

La **console** fait partie des outils de développement du navigateur. On y tape une instruction, on appuie sur Entrée, et le moteur répond sur la ligne suivante. C'est un **interpréteur** : il exécute l'instruction tout de suite, sans étape de compilation à lancer soi-même. Rien n'est enregistré : un rechargement de la page efface tout.

| Navigateur | Ouvrir la console |
|---|---|
| Chrome, Edge | F12, puis l'onglet **Console** ; ou Ctrl+Maj+J (Cmd+Option+J sous macOS) |
| Firefox | F12, puis l'onglet **Console** ; ou Ctrl+Maj+K (Cmd+Option+K sous macOS) |
| Safari | d'abord, dans **Réglages**, onglet **Avancés**, cochez « Afficher les fonctionnalités pour les développeurs web » ; puis Cmd+Option+C |

Les exercices de ce bit se font dans la **console de l'aperçu**, sous la page : elle se comporte comme celle du navigateur, et vos réponses y sont vérifiées.

> 📖 [La console des outils de développement (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Howto/Tools_and_setup/What_are_browser_developer_tools) · [L'objet console (MDN)](https://developer.mozilla.org/fr/docs/Web/API/console)

## Calculer et assembler du texte

Le moteur sait d'abord **calculer**, avec les opérateurs de la calculatrice, et manipuler du **texte**, écrit entre guillemets : `"Bonjour"` ou `'Bonjour'`. Voici quelques lignes tapées dans la console, et ses réponses.

```scene
lesson: assets/console-plan.scene.json
step: calcul
```

Le séparateur décimal est le **point** : `2.5`, jamais `2,5`. Entre deux textes, le `+` **assemble**. L'objet **`Math`** range des fonctions toutes faites. Et un programme, qui n'a personne pour lire les réponses, écrit avec **`console.log(…)`** : un message pour le développeur, que le visiteur de la page ne voit pas.

## À toi : calcule dans la console

Dans la console sous l'aperçu, tape d'abord `7 * 8` et Entrée, pour voir la réponse. Puis fais écrire les trois lignes demandées avec `console.log`.

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

Seules les lignes de `console.log`, sans marque, sont vérifiées ici : un programme n'écrit que celles-là.

## Trois sortes de réponses : une valeur, `undefined`, une erreur

Chaque instruction tapée reçoit une réponse, et il n'en existe que trois sortes. Savoir les reconnaître, c'est savoir ce que le moteur a compris.

```scene
lesson: assets/console.scene.json
step: reponses
```

Une **valeur** est le résultat ; **`undefined`** veut dire « pas de valeur » (`console.log` écrit, mais ne rend rien) ; une **erreur**, en rouge, nomme en anglais ce qui manque : `is not defined`, « n'est pas défini ». La lire avant de relire son code fait gagner beaucoup de temps.

Le dernier cas de la scène est le plus dangereux : `3,5 + 1` répond `6`, sans aucun message. Le moteur lit « 3, puis 5 + 1 » et garde le dernier. **Un résultat faux et silencieux** est pire qu'une erreur, parce que rien ne vous alerte.

## À toi : le piège des guillemets

Tu veux que la console écrive le mot Bonjour. Sans guillemets, le moteur cherche une variable `Bonjour` ; avec un seul, le texte n'est jamais refermé. Complète l'instruction.

```fill
place: stage
text: "Pour écrire le mot Bonjour dans la console : `console.log(_____Bonjour_____)`."
blanks:
  - answers: ['"', "'"]
    hint: "Un texte s'ouvre par un guillemet, double ou simple."
  - answers: ['"', "'"]
    hint: Et se referme par le même guillemet.
```

## Le texte et les nombres : `"5" + 3`

Toute valeur a un **type**, que donne `typeof` : `typeof 25` répond `"number"` (un nombre), `typeof "25"` répond `"string"` (une chaîne de caractères, du texte), `typeof true` répond `"boolean"` (vrai ou faux). Les guillemets décident : `25` est un nombre, `"25"` est un texte qui contient deux chiffres.

```scene
lesson: assets/console.scene.json
step: types
```

Ce n'est pas un détail. Quand un `+` voit un texte d'un côté, il **assemble** au lieu d'additionner : `"5" + 3` donne `"53"`, sans erreur. Pour calculer, on convertit d'abord avec **`Number(…)`** : `Number("5")` vaut le nombre `5`, et `Number("5") + 3` donne `8`.

## À toi : le piège du texte qui ressemble à un nombre

Tout ce qu'un visiteur saisit arrive sous forme de texte. La fonction **`prompt("Quel âge avez-vous ?")`** ouvre une boîte de dialogue avec un champ, et rend ce qu'on y a tapé : du texte, toujours, même s'il ne contient que des chiffres (ou `null` si l'on clique sur Annuler).

Les boîtes de dialogue (`alert`, `confirm`, `prompt`) attendent une réponse humaine, que les vérifications ne savent pas donner. Ici, `script.js` contient déjà une variable `ageSaisi`, avec la valeur que `prompt` aurait rendue pour quelqu'un qui tape 25. Tape les trois instructions dans la console, et regarde ce que donne la première.

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

`ageSaisi + 1` donne `251` : le `+` a vu un texte, il a collé le `1` au bout. Pas d'erreur, juste un résultat faux. Après `Number(ageSaisi)`, le `+` voit deux nombres et additionne. Ce piège revient à chaque saisie d'un visiteur.

## Ranger une valeur : `let` et `const`

Une **variable** est un nom qui désigne une valeur, pour la réutiliser plus loin. On la crée avec un mot-clé, puis le signe `=`, qui **range** la valeur de droite dans le nom de gauche : ce n'est pas une égalité au sens des maths.

```scene
lesson: assets/console-plan.scene.json
step: variables
```

| Mot-clé | Ce qu'il crée |
|---|---|
| **`const`** | une constante : changer sa valeur est refusé, `TypeError: Assignment to constant variable.` |
| **`let`** | une variable modifiable : on change sa valeur sans réécrire `let` |

Le bon réflexe : `const` par défaut, `let` seulement quand la valeur doit changer. Le `;` termine une instruction, et `//` commence un commentaire, que le moteur ignore.

## À toi : une variable qui change, une constante qui refuse

Les deux lignes de départ sont dans `script.js` : `const PRIX_ABONNEMENT = 24;` et `let nombreEmprunts = 3;`. Dans la console, ajoute 1 à `nombreEmprunts`, affiche le résultat, puis essaie de changer `PRIX_ABONNEMENT`, pour lire l'erreur.

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

Tape ensuite `PRIX_ABONNEMENT = 30` : la console répond en rouge. C'est `const` qui fait son travail.

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
