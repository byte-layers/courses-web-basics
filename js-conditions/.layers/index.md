---
title: "Décider : les conditions en JavaScript"
description: "Un programme choisit selon les valeurs : comparer avec ===, if et else, enchaîner les cas avec else if, combiner avec et, ou, non ; les pièges du = qui range au lieu de comparer et du == qui confond \"5\" et 5."
tags:
  - bit
  - javascript
  - web
difficulty: beginner
duration: 20
requires: "0.9.0"
---

Un programme ne fait pas toujours la même chose : il **décide** selon les valeurs qu'il reçoit. Vous saurez comparer deux valeurs, écrire une condition avec `if` et `else`, enchaîner plusieurs cas avec `else if`, combiner des conditions avec « et », « ou », « non », et éviter les deux pièges les plus silencieux du langage : le `=` qui range au lieu de comparer, et le `==` qui confond `"5"` et `5`.

**Prérequis** : [La console JavaScript](https://byte-layers.com/fr/bits/js-console), pour les types, `Number()` et `console.log`, et [Où vit le JavaScript dans une page](https://byte-layers.com/fr/bits/js-in-page), pour le fichier `script.js`.

# Décider : les conditions en JavaScript

Jusqu'ici, votre code s'exécute de haut en bas, toujours pareil. Une page de connexion, un jeu, un formulaire doivent pourtant réagir différemment selon ce qu'on leur donne : c'est le rôle des conditions.

## Comparer deux valeurs : `true` ou `false`

Une **comparaison** pose une question au moteur, qui répond par un **booléen** : `true` (vrai) ou `false` (faux). Tapée dans la console, `20 >= 18` répond `true`.

```scene
lesson: assets/conditions.scene.json
step: comparer
```

| Opérateur | Question |
|---|---|
| `===` (`7 === 7` vaut `true`) | égal, en valeur **et** en type ? |
| `!==` (`7 !== 3` vaut `true`) | différent ? |
| `<`, `>` (`3 < 7` vaut `true`) | plus petit, plus grand ? |
| `<=`, `>=` (`18 >= 18` vaut `true`) | plus petit ou égal, plus grand ou égal ? |

L'égalité s'écrit avec **trois** signes `=`. Un seul `=` ne compare rien : il **range** une valeur dans une variable, comme vous l'avez vu avec `let`.

## À toi : un signe `=` ou trois ?

Range, puis compare : à chaque trou, choisis entre `=` (ranger), `===` (égal ?) et `>=` (au moins ?).

```fill
place: stage
text: "Pour ranger la réponse du joueur : `let reponse _____ \"Paris\";`. Pour demander si c'est la bonne : `reponse _____ \"Paris\"`. Pour demander si un score atteint 10 : `score _____ 10`."
blanks:
  - answers: ["="]
    hint: Ici, on range une valeur dans la variable, on ne pose pas de question.
  - answers: ["==="]
    hint: "Une question d'égalité : trois signes `=`."
  - answers: [">="]
    hint: Au moins 10, c'est « plus grand ou égal ».
```

Les trois s'écrivent sans erreur. Seul le sens change : un `=` de trop ou de moins ne se voit qu'au résultat.

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

Un seul des deux blocs s'exécute, jamais les deux. Suivez le moteur avec `age` à 20, puis à 15 :

```scene
lesson: assets/conditions.scene.json
step: if-else
```

## À toi : le code d'accès qui laisse tout passer

Le code ci-dessous contrôle un code d'accès. Le visiteur a tapé `"0000"`, le code secret est `"1234"`, et pourtant la console annonce « Accès autorisé ». Trouve la faute et corrige-la, sans changer les deux valeurs.

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

## Plusieurs cas : `else if`

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

Suivez le moteur avec `age` à 70, puis à 8 :

```scene
lesson: assets/conditions.scene.json
step: else-if
```

L'ordre compte : le premier cas vrai gagne, les suivants ne sont même pas testés.

## À toi : le tarif du musée

Ce musée est gratuit avant 4 ans, à tarif réduit avant 12 ans, à plein tarif ensuite. Pour un enfant de 3 ans, le code annonce pourtant « Tarif réduit ». Remets les cas dans le bon ordre, sans changer l'âge ni les textes.

```playground
runtime: web
title: Le tarif qui oublie la gratuité
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Musée</title>
      <script src="script.js" defer></script>
    </head>
    <body>
      <h1>Billetterie</h1>
    </body>
    </html>
  script.js: |
    const age = 3;

    if (age < 12) {
      console.log("Tarif réduit");
    } else if (age < 4) {
      console.log("Gratuit");
    } else {
      console.log("Plein tarif");
    }
open: [script.js, index.html]
lock: [index.html]
show: [editor, preview, console]
verify:
  - label: la console affiche « Gratuit » pour un enfant de 3 ans
    console: /^Gratuit$/
    hint: "`3 < 12` est vrai : le premier cas gagne, et `age < 4` n'est jamais testé. Mets le cas le plus restrictif en premier."
  - label: l'âge vaut toujours 3, et `age < 4` est testé avant `age < 12`
    file: script.js
    includes: /const age = 3;[\s\S]*age\s*<\s*4[\s\S]*else if\s*\(\s*age\s*<\s*12\s*\)/
    hint: "Garde `const age = 3;` et écris `if (age < 4)`, puis `else if (age < 12)`, puis `else`."
solution: assets/tarif.solution
```

Du plus restrictif au plus large : un cas plus large placé avant avale les plus petits, sans message.

## Combiner : `&&`, `||`, `!`

En maths, on écrit « 18 ≤ âge < 65 ». En JavaScript, `18 <= age < 65` ne pose pas cette question. Suivez le moteur avec un visiteur de 70 ans :

```scene
lesson: assets/conditions.scene.json
step: intervalle
```

Il faut répéter la variable de chaque côté et relier les deux comparaisons par l'un de ces trois opérateurs :

| Opérateur | Vaut `true` quand… |
|---|---|
| `&&` (et) | les deux conditions sont vraies |
| `\|\|` (ou) | au moins l'une est vraie |
| `!` (non) | la condition est fausse |

## À toi : et, ou

Un intervalle, puis l'un ou l'autre : choisis l'opérateur qui relie les deux comparaisons.

```fill
place: stage
text: "Pour savoir si un enfant a entre 6 et 17 ans : `age >= 6 _____ age <= 17`. Pour savoir s'il a droit à la gratuité, avant 12 ans ou à partir de 65 ans : `age < 12 _____ age >= 65`."
blanks:
  - answers: ["&&"]
    hint: Les deux conditions doivent être vraies en même temps.
  - answers: ["||"]
    hint: Il suffit que l'une des deux soit vraie.
```

## Un texte n'est pas un nombre : `===` contre `==`

Il existe aussi une égalité à **deux** signes, `==`. Comparez-la à `===` sur un texte qui ressemble à un nombre :

```scene
lesson: assets/conditions.scene.json
step: egalite
```

`==` paraît plus arrangeant ; il cache en réalité la confusion entre texte et nombre, qui ressortira ailleurs. On utilise toujours **`===`**, et l'on convertit soi-même avec `Number()`.

## À toi : le jeu de devinette

`prompt()` rend toujours du texte, même quand on tape un nombre. Dans ce jeu de devinette, le nombre secret est `7`, et le joueur a tapé `"7"` : du texte, comme ce que rend `prompt()`. Écris la condition qui affiche le verdict : « Gagné ! », « Trop petit. » ou « Trop grand. ».

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
    const saisie = "7"; // ce que le joueur a tapé : du texte, comme ce que rend prompt()
    const proposition = saisie;

    // À toi : affiche proposition suivi de "Gagné !", "Trop petit." ou "Trop grand."
    // par exemple console.log(proposition, "Gagné !");
open: [script.js, index.html]
lock: [index.html]
show: [editor, preview, console]
check: ask
verify:
  - label: la saisie "7" affiche « 7 Gagné ! »
    console: /^7 Gagné !$/
    hint: "Si tu obtiens « 7 Trop grand. », c'est que `\"7\" === 7` vaut `false` : un texte n'est pas un nombre. Convertis : `const proposition = Number(saisie);`"
  - label: le verdict est choisi par `if`, `else if` et `else`
    file: script.js
    includes: /if\s*\([\s\S]*else\s+if\s*\([\s\S]*else\s*\{/
    hint: "Trois cas : `if (proposition === secret) { … } else if (proposition < secret) { … } else { … }`."
  - label: la saisie est convertie avec `Number()`
    file: script.js
    includes: /Number\(\s*saisie\s*\)/
    hint: "La saisie reste du texte tant que tu ne la convertis pas : `Number(saisie)`."
  - label: les comparaisons utilisent `===`, jamais `==`
    file: script.js
    excludes: /[^=!<>]==[^=]/
    hint: "`==` masque la différence entre texte et nombre. Garde `===` et convertis avec `Number()`."
solution: assets/devinette.solution
```

Sans conversion, `"7" === 7` vaut `false`, `"7" < 7` aussi, et le joueur qui trouve le bon nombre lit « Trop grand. », sans aucune erreur. Avec `Number(saisie)`, les comparaisons portent sur des nombres. Change la saisie en `"3"`, puis en `"9"`, pour voir les deux autres verdicts.

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
