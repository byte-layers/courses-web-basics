---
title: "Où vit le JavaScript dans une page : script, fichier .js et defer"
description: "Ce qu'on tape dans la console disparaît ; dans la page, le code se rejoue à chaque chargement. La balise script, le fichier .js séparé, le script placé trop tôt qui trouve null, et l'attribut defer."
tags:
  - bit
  - javascript
  - web
difficulty: beginner
duration: 15
requires: "0.9.0"
---

Ce que vous tapez dans la console disparaît au rechargement ; écrit dans la page, le code se rejoue à chaque ouverture. Vous saurez brancher un fichier `.js` sur une page avec la balise `<script>`, pourquoi un script placé dans le `<head>` ne trouve pas les éléments de la page (il obtient `null`), et les deux façons de le corriger : la fin du `<body>` ou l'attribut `defer`.

**Prérequis** : [La console JavaScript](https://byte-layers.com/fr/bits/js-console), pour `console.log`, les variables et la lecture d'une erreur.

# Où vit le JavaScript dans une page

Dans la console, chaque instruction s'exécute une fois et s'oublie. Une page web, elle, se recharge sans cesse : pour que son code se rejoue à chaque fois, il doit faire partie de la page.

## La balise `<script>` et le fichier `.js`

Le navigateur lit le HTML de haut en bas, et une balise `<script>` interrompt sa lecture.

```scene
lesson: assets/in-page.scene.json
step: lecture
```

Quand il rencontre une balise **`<script>`**, il s'arrête, exécute le JavaScript, puis reprend sa lecture. Le code peut s'écrire directement entre les balises :

```html
<script>
  console.log("Bonjour depuis la page");
</script>
```

Ça marche, mais le HTML se remplit de code. On préfère un **fichier séparé**, d'extension `.js`, que la balise désigne par son attribut `src` (*source*), comme un `<link>` désigne une feuille de style :

```html
<script src="script.js"></script>
```

| Écriture | Quand l'utiliser |
|---|---|
| `<script>…</script>`, le code dans le HTML | un essai de deux lignes |
| `<script src="script.js"></script>`, le code dans `script.js`, à côté de la page | tout le reste : un fichier pour le contenu, un pour la forme, un pour le comportement |

La balise s'écrit toujours avec sa fermeture `</script>`, même vide. Le nom dans `src` doit être **exactement** celui du fichier : `Script.js` ne trouve pas `script.js`. Un nom faux ne produit aucune erreur JavaScript, puisqu'aucun code n'est chargé : il ne se passe rien, simplement.

## À toi : branche script.js

Le fichier `script.js` contient déjà une ligne, mais la page ne le charge pas. Ajoute la balise qui le branche, juste avant `</body>`.

```playground
runtime: web
title: Branche le fichier script.js
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Mon portfolio</title>
    </head>
    <body>
      <h1>Ada Lovelace</h1>
      <p>Développeuse web</p>
      <!-- Branche script.js ici -->
    </body>
    </html>
  script.js: |
    console.log("script.js est chargé");
open: [index.html, script.js]
show: [editor, preview, console]
verify:
  - label: la console affiche « script.js est chargé »
    console: /^script\.js est chargé$/
    hint: "Avant `</body>` : `<script src=\"script.js\"></script>`, avec la balise de fermeture."
solution: assets/brancher.solution
```

Recharge l'aperçu ou modifie la page : la ligne revient à chaque fois. C'est la différence avec la console, où rien ne se rejoue.

## Un script trop tôt : l'élément vaut `null`

Un script sert le plus souvent à agir sur la page : changer un texte, réagir à un clic. Pour cela, il doit d'abord **trouver** l'élément. Prenez cette ligne comme une recette, que le bit sur le DOM détaillera : `document.querySelector("#compteur")` cherche dans la page l'élément d'identifiant `compteur`, avec le même sélecteur qu'en CSS, et le rend. S'il ne le trouve pas, il rend **`null`**, la valeur qui veut dire « aucun objet ».

```scene
lesson: assets/in-page.scene.json
step: trop-tot
```

Or le navigateur exécute un script **au moment où il le lit**. Placé dans le `<head>`, le script tourne avant que le `<body>` existe : la recherche rend `null`. Chercher ne provoque pas d'erreur ; c'est en voulant écrire dans `null` que tout s'arrête, avec ce message :

```text
TypeError: Cannot set properties of null (setting 'textContent')
```

Le message dit qu'on ne peut pas modifier une propriété (*set properties*) de `null`. L'erreur pointe la ligne qui écrit, pas celle qui a cherché trop tôt : c'est ce qui rend ce piège difficile à trouver seul.

## À toi : répare le script placé trop tôt

La page ci-dessous est livrée cassée : son script est dans le `<head>`. Lis d'abord l'erreur dans la console, puis répare la page **sans toucher à `script.js`** : la balise peut aller ailleurs.

```playground
runtime: web
title: Répare le script placé trop tôt
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Médiathèque</title>
      <script src="script.js"></script>
    </head>
    <body>
      <h1>Médiathèque</h1>
      <p id="compteur">En attente du script…</p>
    </body>
    </html>
  script.js: |
    console.log("script.js est chargé");
    const compteur = document.querySelector("#compteur");
    compteur.textContent = "47 emprunts aujourd'hui";
open: [index.html, script.js]
lock: [script.js]
show: [editor, preview, console]
verify:
  - label: le paragraphe `#compteur` affiche « 47 emprunts aujourd'hui »
    selector: "#compteur"
    text: 47 emprunts aujourd'hui
    hint: "Le script cherche `#compteur` avant que le `<body>` soit lu. Déplace la balise `<script>` juste avant `</body>`."
  - label: aucune erreur JavaScript
    errors: none
solution: assets/trop-tot.solution
```

La console affichait `script.js est chargé` même dans la page cassée : le fichier était bien chargé, et sa première ligne s'exécutait. Seul le moment posait problème.

## `defer` : charger dans le `<head>`, exécuter après

Placer le script en bas du `<body>` marche partout. L'autre solution garde la balise dans le `<head>`, avec l'attribut **`defer`** (« différer ») : le navigateur télécharge le fichier tout de suite, mais ne l'exécute qu'une fois toute la page lue.

```html
<head>
  <script src="script.js" defer></script>
</head>
```

La même page que dans la scène du script trop tôt, avec `defer` :

```scene
lesson: assets/in-page.scene.json
step: defer
```

| Placement | Le script s'exécute… |
|---|---|
| `<script src>` dans le `<head>` | avant la lecture du `<body>` : `null` |
| `<script src>` juste avant `</body>` | après la lecture du `<body>` : trouvé |
| `<script src defer>` dans le `<head>` | après la lecture de toute la page : trouvé |

Les deux solutions qui marchent se valent pour une page simple. `defer` a l'avantage de regrouper dans le `<head>` tout ce que la page charge, et de commencer le téléchargement plus tôt. `defer` ne fonctionne qu'avec un fichier externe (`src`), pas avec un script écrit entre les balises.

## À toi : garde le script dans le head, avec defer

Même page cassée, autre réparation : garde la balise dans le `<head>`, et fais-la attendre.

```playground
runtime: web
title: Garde le script dans le head, avec defer
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Médiathèque</title>
      <script src="script.js"></script>
    </head>
    <body>
      <h1>Médiathèque</h1>
      <p id="message">En attente du script…</p>
    </body>
    </html>
  script.js: |
    const message = document.querySelector("#message");
    message.textContent = "Ouverte aujourd'hui de 10 h à 18 h";
open: [index.html, script.js]
lock: [script.js]
show: [editor, preview, console]
check: ask
verify:
  - label: le paragraphe `#message` affiche les horaires
    selector: "#message"
    text: Ouverte aujourd'hui de 10 h à 18 h
  - label: la balise `<script>` est restée dans le `<head>`, avec `defer`
    file: index.html
    includes: /<head>[\s\S]*<script[^>]*\sdefer[\s\S]*<\/head>/
    hint: "Un seul mot à ajouter dans la balise : `<script src=\"script.js\" defer></script>`."
  - label: aucune erreur JavaScript
    errors: none
solution: assets/defer.solution
```

> 📖 [L'élément script et l'attribut defer (MDN)](https://developer.mozilla.org/fr/docs/Web/HTML/Reference/Elements/script) · [Ajouter du JavaScript à une page (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Scripting/What_is_JavaScript)

## Trois questions pour vérifier ce que vous avez retenu

```quiz
title: "Le JavaScript dans une page"
tracksProgress: false
showNotice: false
place: stage
questions:
  - prompt: "Une page contient `<script src=\"Script.js\"></script>`, et le fichier s'appelle `script.js`. Que se passe-t-il ?"
    answers:
      - "Le navigateur corrige la majuscule et charge le fichier"
      - "Le fichier n'est pas trouvé : aucun code ne s'exécute, et aucune erreur JavaScript ne le signale"
      - "La page ne s'affiche pas"
    correct: 2
    explanation: "Le nom dans src doit être exactement celui du fichier. Sans fichier, il n'y a aucun code à exécuter, donc aucune erreur JavaScript : il ne se passe rien."
  - prompt: "Un script placé dans le `<head>`, sans `defer`, cherche `#compteur` avec `querySelector`. Qu'obtient-il ?"
    answers:
      - "L'élément, comme partout ailleurs"
      - "null, parce que le body n'a pas encore été lu quand le script s'exécute"
      - "Une erreur à la ligne du querySelector"
    correct: 2
    explanation: "Le navigateur exécute un script au moment où il le lit. Dans le head, le body n'existe pas encore : la recherche rend null, et l'erreur n'arrive qu'à la ligne qui écrit dans cet élément."
  - prompt: "Que fait l'attribut `defer` sur `<script src=\"script.js\" defer>` ?"
    answers:
      - "Il exécute le script une fois toute la page lue, même si la balise est dans le head"
      - "Il empêche le script de s'exécuter"
      - "Il exécute le script avant tout le reste de la page"
    correct: 1
    explanation: "Le fichier est téléchargé tout de suite, mais exécuté après la lecture de toute la page : les éléments du body sont alors trouvés."
```

## Récap

- La balise **`<script src="script.js"></script>`** branche un fichier JavaScript sur la page ; le code se rejoue à chaque chargement, contrairement à la console.
- Le nom dans `src` doit être exact, majuscules comprises ; un nom faux ne charge rien, sans erreur.
- Le navigateur exécute un script **au moment où il le lit** : dans le `<head>`, les éléments du `<body>` n'existent pas encore, `querySelector` rend **`null`**, et l'erreur arrive à la ligne qui écrit dans `null`.
- Deux corrections : la balise **juste avant `</body>`**, ou **`defer`** dans le `<head>`.

Votre code s'exécute maintenant à chaque chargement, mais toujours de la même façon, de haut en bas. Pour qu'il choisisse selon les réponses, il faut des conditions : c'est l'objet du bit [Décider : les conditions en JavaScript](https://byte-layers.com/fr/bits/js-conditions).

```ack
J'ai compris
```
