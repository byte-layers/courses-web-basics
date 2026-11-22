---
title: "Décider : les conditions en JavaScript"
description: "Un programme choisit selon les valeurs : comparer avec ===, if et else, enchaîner les cas avec else if, combiner avec et, ou, non ; les pièges du = qui range au lieu de comparer et du == qui confond \"5\" et 5."
tags:
  - bit
  - javascript
  - web
difficulty: beginner
duration: 15
requires: "0.9.0"
---

Un programme ne fait pas toujours la même chose : il **décide** selon les valeurs qu'il reçoit. Vous saurez comparer deux valeurs, écrire une condition avec `if` et `else`, enchaîner plusieurs cas avec `else if`, combiner des conditions avec « et », « ou », « non », et éviter les deux pièges les plus silencieux du langage : le `=` qui range au lieu de comparer, et le `==` qui confond `"5"` et `5`.

**Prérequis** : [La console JavaScript](https://byte-layers.com/fr/bits/js-console), pour les types, `Number()` et `console.log`, et [Où vit le JavaScript dans une page](https://byte-layers.com/fr/bits/js-in-page), pour le fichier `script.js`.

# Décider : les conditions en JavaScript

Jusqu'ici, votre code s'exécute de haut en bas, toujours pareil. Une page de connexion, un jeu, un formulaire doivent pourtant réagir différemment selon ce qu'on leur donne : c'est le rôle des conditions.

## Comparer deux valeurs : `true` ou `false`

Une **comparaison** pose une question au moteur, qui répond par un **booléen** : `true` (vrai) ou `false` (faux). Tapée dans la console, `20 >= 18` répond `true`.

| Opérateur | Question | Exemple | Réponse |
|---|---|---|---|
| `===` | égal, en valeur **et** en type ? | `7 === 7` | `true` |
| `!==` | différent ? | `7 !== 3` | `true` |
| `<`, `>` | plus petit, plus grand ? | `3 < 7` | `true` |
| `<=`, `>=` | plus petit ou égal, plus grand ou égal ? | `18 >= 18` | `true` |

L'égalité s'écrit avec **trois** signes `=`. Un seul `=` ne compare rien : il **range** une valeur dans une variable, comme vous l'avez vu avec `let`. Cette confusion est le premier piège de la section suivante.

## Si… sinon : `if` et `else`

Une **condition** exécute un bloc de code seulement si une comparaison vaut `true`. Le mot-clé **`if`** (« si ») est suivi de la comparaison entre parenthèses, puis du bloc entre accolades ; **`else`** (« sinon ») donne le bloc à exécuter dans le cas contraire :

```javascript
const age = 20;
if (age >= 18) {
  console.log("Majeur");
} else {
  console.log("Mineur");
}
```

Un seul des deux blocs s'exécute, jamais les deux. Ici, la console affiche `Majeur` ; avec `const age = 15;`, elle afficherait `Mineur`.

Le code ci-dessous contrôle un code d'accès. Le visiteur a tapé `"0000"`, le code secret est `"1234"`, et pourtant la console annonce « Accès autorisé ». Trouvez la faute et corrigez-la, sans changer les deux valeurs.

```playground
runtime: web
title: Le code d'accès qui laisse tout passer
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Accès</title>
      <script src="script.js" defer></script>
    </head>
    <body>
      <h1>Espace réservé</h1>
    </body>
    </html>
  script.js: |
    const codeSecret = "1234";
    let saisie = "0000"; // ce que le visiteur a tapé

    if (saisie = codeSecret) {
      console.log("Accès autorisé");
    } else {
      console.log("Accès refusé");
    }
open: [script.js, index.html]
lock: [index.html]
show: [editor, preview, console]
verify:
  - label: la console affiche « Accès refusé » pour la saisie "0000"
    console: /^Accès refusé$/
    hint: "Dans la condition, un seul `=` range `codeSecret` dans `saisie`, puis le texte rangé est pris pour vrai. Pour comparer : `===`."
  - label: la saisie et le code secret n'ont pas changé
    file: script.js
    includes: /let saisie = "0000"[\s\S]*(saisie\s*===\s*codeSecret|codeSecret\s*===\s*saisie)/
    hint: "Garde `let saisie = \"0000\";` et compare `saisie === codeSecret`."
solution: assets/acces.solution
```

Avec un seul `=`, la condition ne pose aucune question : elle range `"1234"` dans `saisie`, et un texte non vide compte comme vrai. Aucune erreur rouge ne le signale. Avec `===`, la question est posée, et la réponse est `false`.

## Plusieurs cas : `else if`, et, ou, non

Quand il y a plus de deux cas, on les enchaîne avec **`else if`** (« sinon si »). Le moteur teste les conditions dans l'ordre et exécute le **premier** bloc dont la condition vaut `true`, puis s'arrête :

```javascript
const age = 70;
if (age < 12) {
  console.log("enfant");
} else if (age < 18) {
  console.log("jeune");
} else if (age < 65) {
  console.log("adulte");
} else {
  console.log("senior");
}
```

L'ordre compte : du plus restrictif au plus large. Si `age < 18` venait avant `age < 12`, un enfant de 8 ans serait classé « jeune », et le cas « enfant » ne serait jamais atteint, sans message.

Pour combiner des conditions, trois opérateurs :

| Opérateur | Se lit | Vaut `true` quand… |
|---|---|---|
| `&&` | et | les deux conditions sont vraies |
| `\|\|` | ou | au moins l'une est vraie |
| `!` | non | la condition est fausse |

En maths, on écrit « 18 ≤ âge < 65 ». En JavaScript, `18 <= age < 65` ne pose pas cette question : le moteur compare d'abord `18 <= age`, obtient `true`, puis compare `true < 65`, et `true` vaut 1 dans un calcul. Pour un visiteur de 70 ans, la réponse est `true`, en silence. Il faut répéter la variable de chaque côté et relier les deux comparaisons.

```fill
text: "Pour savoir si un visiteur a entre 18 et 64 ans : `age >= 18 _____ age < 65`. Pour savoir s'il a droit à la gratuité, avant 12 ans ou à partir de 65 ans : `age < 12 _____ age >= 65`."
blanks:
  - answers: ["&&"]
    hint: Les deux conditions doivent être vraies en même temps.
  - answers: ["||"]
    hint: Il suffit que l'une des deux soit vraie.
```

## Un texte n'est pas un nombre : `===` contre `==`

Il existe aussi une égalité à **deux** signes, `==`. Elle convertit les valeurs avant de comparer : `"5" == 5` répond `true`, alors que `"5" === 5` répond `false`, parce que l'une est un texte et l'autre un nombre. `==` paraît plus arrangeant ; il cache en réalité la confusion entre texte et nombre, qui ressortira ailleurs. On utilise toujours **`===`**, et l'on convertit soi-même avec `Number()`.

C'est exactement ce qui arrive avec `prompt()`, qui rend toujours du texte. Dans ce jeu de devinette, le nombre secret est `7`. Les trois lignes du bas appellent `verdict` avec trois saisies, comme si un joueur les avait tapées : les lignes entre les accolades de `verdict` se rejouent pour chacune (le bit sur les fonctions détaillera cette écriture). Écrivez la condition qui affiche le verdict.

```playground
runtime: web
title: Le jeu de devinette
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Devinette</title>
      <script src="script.js" defer></script>
    </head>
    <body>
      <h1>Devinez un nombre entre 1 et 10</h1>
    </body>
    </html>
  script.js: |
    const secret = 7;

    function verdict(saisie) {
      const proposition = saisie;
      // À toi : affiche proposition suivi de "Gagné !", "Trop petit." ou "Trop grand."
      // par exemple console.log(proposition, "Gagné !");
    }

    // Trois saisies, du texte comme ce que rend prompt()
    verdict("7");
    verdict("3");
    verdict("9");
open: [script.js, index.html]
lock: [index.html]
show: [editor, preview, console]
check: ask
verify:
  - label: la saisie "7" affiche « 7 Gagné ! »
    console: /^7 Gagné !$/
    hint: "Si tu obtiens « 7 Trop grand. », c'est que `\"7\" === 7` vaut `false` : un texte n'est pas un nombre. Convertis : `const proposition = Number(saisie);`"
  - label: la saisie "3" affiche « 3 Trop petit. »
    console: /^3 Trop petit\.$/
  - label: la saisie "9" affiche « 9 Trop grand. »
    console: /^9 Trop grand\.$/
  - label: les comparaisons utilisent `===`, jamais `==`
    file: script.js
    excludes: /[^=!<>]==[^=]/
    hint: "`==` masque la différence entre texte et nombre. Garde `===` et convertis avec `Number()`."
solution: assets/devinette.solution
```

Sans conversion, `"7" === 7` vaut `false`, `"7" < 7` aussi, et le joueur qui trouve le bon nombre lit « Trop grand. », sans aucune erreur. Avec `Number(saisie)`, les trois comparaisons portent sur des nombres.

> 📖 [Les instructions if...else (MDN)](https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Statements/if...else) · [L'égalité stricte === (MDN)](https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Operators/Strict_equality) · [Les opérateurs logiques (MDN)](https://developer.mozilla.org/fr/docs/Web/JavaScript/Guide/Expressions_and_operators#opérateurs_logiques)

## Trois questions pour vérifier ce que vous avez retenu

```quiz
title: "Les conditions"
tracksProgress: false
showNotice: false
place: stage
questions:
  - prompt: "Avec `let n = 20;`, que fait `if (n = 18) { console.log(\"bloc\"); }` ?"
    answers:
      - "Rien : n ne vaut pas 18"
      - "Le bloc s'exécute et n vaut désormais 18 : un seul = range une valeur, il ne compare pas"
      - "Une erreur rouge signale le signe ="
    correct: 2
    explanation: "Un seul = range 18 dans n, puis la valeur rangée, 18, compte comme vraie : le bloc s'exécute. Aucune erreur ne prévient. Pour comparer, on écrit ===."
  - prompt: "Que répondent `\"5\" == 5` et `\"5\" === 5` ?"
    answers:
      - "true et true"
      - "false et false"
      - "true et false : == convertit avant de comparer, === compare aussi le type"
    correct: 3
    explanation: "== convertit le texte en nombre avant de comparer, ce qui cache la différence. === compare la valeur et le type : un texte n'est jamais égal à un nombre."
  - prompt: "Dans une chaîne `if / else if / else`, dans quel ordre écrire `age < 18` et `age < 12` ?"
    answers:
      - "age < 12 d'abord : du plus restrictif au plus large"
      - "age < 18 d'abord, parce que 18 est plus grand"
      - "L'ordre n'a pas d'importance"
    correct: 1
    explanation: "Le moteur exécute le premier bloc dont la condition est vraie. Avec age < 18 en premier, un enfant de 8 ans y entrerait, et le cas age < 12 ne serait jamais atteint."
```

## Récap

- Une **comparaison** rend un booléen, `true` ou `false` ; l'égalité s'écrit **`===`**, la différence `!==`.
- **`if (…) { … } else { … }`** exécute un seul des deux blocs ; **`else if`** enchaîne d'autres cas, testés dans l'ordre, du plus restrictif au plus large.
- **`&&`** (et), **`||`** (ou), **`!`** (non) combinent des conditions ; un intervalle s'écrit `age >= 18 && age < 65`.
- Un seul **`=`** range une valeur au lieu de comparer : la condition passe, sans erreur.
- **`==`** convertit avant de comparer (`"5" == 5` vaut `true`) : on écrit `===` et l'on convertit avec `Number()`.

Votre programme sait choisir, une fois. Pour refaire la même chose sur toute une liste, ou jusqu'à ce que ce soit bon, il faut des tableaux et des boucles : c'est l'objet du bit [Répéter : tableaux et boucles](https://byte-layers.com/fr/bits/js-arrays-loops).

```ack
J'ai compris
```
