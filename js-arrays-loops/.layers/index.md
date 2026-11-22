---
title: "Répéter : tableaux et boucles en JavaScript"
description: "Ranger plusieurs valeurs dans un tableau, numéroté à partir de 0, puis les parcourir avec for, for…of et while ; les pièges de l'index 0, du <= qui fait un tour de trop et de la boucle sans fin."
tags:
  - bit
  - javascript
  - web
difficulty: beginner
duration: 15
requires: "0.9.0"
---

Un programme refait souvent la même chose : sur chaque élément d'une liste, ou jusqu'à obtenir la bonne réponse. Vous saurez ranger plusieurs valeurs dans un **tableau**, lire une case par son numéro (qui commence à 0), parcourir un tableau avec `for` et `for…of`, répéter avec `while`, et reconnaître les trois pièges des boucles : l'index 0, le `<=` qui fait un tour de trop, et la boucle qui ne s'arrête jamais.

**Prérequis** : [Décider : les conditions en JavaScript](https://byte-layers.com/fr/bits/js-conditions), pour les comparaisons et `if`.

# Répéter : tableaux et boucles

Afficher cinq projets, c'est cinq fois le même geste. Les écrire cinq fois marche jusqu'au jour où il y en a six. Un tableau range les valeurs ensemble, une boucle répète le geste pour chacune.

## Un tableau : des cases numérotées à partir de 0

Un **tableau** (*array*) est une liste de valeurs, écrite entre crochets et séparées par des virgules. Chaque valeur occupe une **case**, désignée par son numéro, l'**index**, qui commence à **0** :

```javascript
const fruits = ["Pomme", "Banane", "Cerise", "Mangue", "Poire"];
console.log(fruits[0]);      // Pomme : la première case
console.log(fruits[2]);      // Cerise : la troisième case
console.log(fruits.length);  // 5 : le nombre de cases
```

| Écriture | Valeur | Pourquoi |
|---|---|---|
| `fruits[0]` | `"Pomme"` | la première case porte l'index 0 |
| `fruits.length` | `5` | `length` donne le nombre de cases |
| `fruits[fruits.length - 1]` | `"Poire"` | la dernière case porte l'index `length - 1`, ici 4 |
| `fruits[5]` | `undefined` | la case n'existe pas : pas d'erreur, juste « pas de valeur » |
| `fruits.push("Kiwi")` | ajoute `"Kiwi"` à la fin | `length` passe à 6, même avec `const` |

Avec `const`, on ne peut pas remplacer le tableau par un autre, mais on peut changer ce qu'il contient : `push` est permis. Une case qui n'existe pas rend `undefined` sans prévenir, ce qui prépare le piège de la section suivante.

```fill
text: "Avec `const fruits = [\"Pomme\", \"Banane\", \"Cerise\", \"Mangue\", \"Poire\"];`, le troisième fruit s'écrit `fruits[_____]`, et le dernier `fruits[fruits.length - _____]`."
blanks:
  - answers: [2]
    hint: "L'index commence à 0 : la première case est fruits[0]."
  - answers: [1]
    hint: Cinq cases, numérotées de 0 à 4.
```

## La boucle `for` : répéter avec un compteur

Une **boucle** répète un bloc de code. La boucle **`for`** tient un compteur, qu'on appelle souvent `i`, et l'utilise comme index :

```javascript
for (let i = 0; i < fruits.length; i++) {
  console.log("case " + i + " : " + fruits[i]);
}
```

Les parenthèses contiennent trois morceaux, séparés par des points-virgules :

| Morceau | Rôle |
|---|---|
| `let i = 0` | avant le premier tour : le compteur part de 0, la première case |
| `i < fruits.length` | avant chaque tour : on continue tant que c'est vrai ; ici, jusqu'à la case 4 |
| `i++` | après chaque tour : ajoute 1 au compteur (`i = i + 1`) |

La boucle ci-dessous doit afficher les cinq fruits en majuscules, avec leur numéro de case. Elle en oublie un, puis s'arrête sur une erreur. Corrigez ses bornes : lisez d'abord la console.

```playground
runtime: web
title: La boucle qui saute une case et en invente une
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Fruits</title>
      <script src="script.js" defer></script>
    </head>
    <body>
      <h1>Le panier</h1>
    </body>
    </html>
  script.js: |
    const fruits = ["Pomme", "Banane", "Cerise", "Mangue", "Poire"];

    for (let i = 1; i <= fruits.length; i++) {
      console.log("case " + i + " : " + fruits[i].toUpperCase());
    }
open: [script.js, index.html]
lock: [index.html]
show: [editor, preview, console]
verify:
  - label: "la première ligne est « case 0 : POMME »"
    console: "/^case 0 : POMME$/"
    hint: "La première case porte l'index 0 : le compteur doit partir de 0."
  - label: "la dernière ligne est « case 4 : POIRE »"
    console: "/^case 4 : POIRE$/"
  - label: aucune erreur JavaScript
    errors: none
    hint: "Avec `<=`, la boucle fait un tour de plus, sur `fruits[5]`, qui vaut `undefined` : `undefined` n'a pas de `toUpperCase`. Écris `i < fruits.length`."
solution: assets/bornes.solution
```

Les deux fautes sont classiques. Partir de 1 saute la première case, sans erreur. Avec `<=`, le dernier tour lit `fruits[5]`, qui n'existe pas : ici, `toUpperCase()` sur `undefined` lève une `TypeError` ; sans elle, la boucle aurait affiché `undefined` en silence. La règle : **de 0 à `length` exclu**, donc `i = 0` et `i < length`.

## `for…of` : parcourir chaque valeur

Quand le numéro de case ne sert à rien, **`for…of`** est plus simple : à chaque tour, la variable reçoit directement la valeur suivante du tableau, sans compteur ni borne à écrire.

```javascript
for (const fruit of fruits) {
  console.log(fruit);
}
```

Pour un total, on utilise un **accumulateur** : une variable déclarée avec `let` avant la boucle, à 0, à laquelle chaque tour ajoute une valeur.

```javascript
let total = 0;
for (const prix of [3, 5, 2]) {
  total = total + prix;
}
console.log(total); // 10
```

Calculez la moyenne des notes du tableau `notes`, avec une boucle, sans écrire le total ni le nombre de notes à la main : le calcul doit rester juste si l'on ajoute une note.

```playground
runtime: web
title: La moyenne d'une liste de notes
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Notes</title>
      <script src="script.js" defer></script>
    </head>
    <body>
      <h1>Bulletin</h1>
    </body>
    </html>
  script.js: |
    const notes = [12, 15, 9, 18, 16];

    // À toi : le total avec for…of, puis la moyenne
    // console.log("Moyenne :", moyenne);
open: [script.js, index.html]
lock: [index.html]
show: [editor, preview, console]
check: ask
verify:
  - label: "la console affiche « Moyenne : 14 »"
    console: "/^Moyenne : 14$/"
    hint: "`let total = 0;`, une boucle `for (const note of notes)` qui ajoute chaque note, puis `const moyenne = total / notes.length;`."
  - label: la boucle parcourt `notes` avec `for…of`
    file: script.js
    includes: /for\s*\(\s*(const|let)\s+\w+\s+of\s+notes\s*\)/
  - label: le nombre de notes vient de `notes.length`, pas d'un 5 écrit à la main
    file: script.js
    includes: notes.length
solution: assets/moyenne.solution
```

## `while` : répéter jusqu'à ce que ce soit bon

Parfois, on ne sait pas combien de tours il faudra : redemander un nombre jusqu'à ce que le joueur trouve, par exemple. La boucle **`while`** (« tant que ») répète son bloc tant que sa condition est vraie :

```javascript
let compte = 3;
while (compte > 0) {
  console.log("Décollage dans " + compte);
  compte = compte - 1;
}
console.log("Décollage !");
```

La console affiche `Décollage dans 3`, `2`, `1`, puis `Décollage !`. Tout repose sur la ligne `compte = compte - 1` : c'est elle qui finira par rendre la condition fausse. Sans elle, `compte` vaut toujours 3, et la boucle ne s'arrête **jamais**.

> ⚠️ **Une boucle sans fin fige l'onglet.** La page ne répond plus, parce que le moteur ne fait plus que tourner dans la boucle. Fermez l'onglet (Ctrl+W, Cmd+W sous macOS), corrigez le fichier, rouvrez la page : rien n'est cassé. Avant d'écrire un `while`, posez-vous la question : « qu'est-ce qui, dans le bloc, va rendre la condition fausse ? ». C'est aussi pourquoi aucun exercice de ce bit ne vous fait écrire de `while` : une boucle sans fin figerait l'aperçu. Le lab vous en fait écrire une, sur votre machine, avec le jeu de devinette qui redemande.

L'instruction **`break`** sort d'une boucle tout de suite, quelle que soit sa condition : utile quand le joueur clique sur Annuler.

> 📖 [Les tableaux (MDN)](https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Global_Objects/Array) · [Boucles et itération (MDN)](https://developer.mozilla.org/fr/docs/Web/JavaScript/Guide/Loops_and_iteration)

## Trois questions pour vérifier ce que vous avez retenu

```quiz
title: "Tableaux et boucles"
tracksProgress: false
showNotice: false
place: stage
questions:
  - prompt: "Avec `const fruits = [\"Pomme\", \"Banane\", \"Cerise\"];`, que vaut `fruits[3]` ?"
    answers:
      - "\"Cerise\", la troisième case"
      - "undefined : les cases vont de 0 à 2, et une case absente ne provoque pas d'erreur"
      - "Une erreur rouge, parce que la case n'existe pas"
    correct: 2
    explanation: "L'index commence à 0 : les trois cases sont 0, 1 et 2. Lire une case absente rend undefined, sans message."
  - prompt: "Combien de tours fait `for (let i = 0; i <= fruits.length; i++)` sur un tableau de 3 cases ?"
    answers:
      - "3"
      - "4 : avec <=, le dernier tour lit fruits[3], qui n'existe pas"
      - "2"
    correct: 2
    explanation: "i prend les valeurs 0, 1, 2 et 3. Le tour où i vaut 3 lit une case qui n'existe pas. Il faut i < fruits.length."
  - prompt: "Que se passe-t-il si l'on retire `compte = compte - 1` de la boucle `while (compte > 0)` ?"
    answers:
      - "La boucle s'arrête au bout de trois tours"
      - "La boucle ne s'arrête jamais, et l'onglet se fige"
      - "Une erreur rouge signale la boucle"
    correct: 2
    explanation: "Plus rien ne change compte : la condition reste vraie pour toujours. Le moteur tourne sans fin et la page ne répond plus ; on ferme l'onglet et on corrige."
```

## Récap

- Un **tableau** range des valeurs dans des cases numérotées **à partir de 0** ; la dernière est à l'index **`length - 1`** ; une case absente vaut `undefined`, sans erreur.
- **`for (let i = 0; i < t.length; i++)`** parcourt toutes les cases ; partir de 1 en saute une, **`<=`** en invente une.
- **`for…of`** donne chaque valeur sans compteur ; un **accumulateur** déclaré avant la boucle construit un total.
- **`while`** répète tant que sa condition est vraie : quelque chose dans le bloc doit la rendre fausse, sinon la boucle ne finit jamais et fige l'onglet.

Vous écrivez maintenant les mêmes gestes à plusieurs endroits, et vous décrivez des choses par plusieurs valeurs à la fois. Nommer un geste une fois, ranger une description dans un objet : c'est l'objet du bit [Fonctions et objets](https://byte-layers.com/fr/bits/js-functions-objects).

```ack
J'ai compris
```
