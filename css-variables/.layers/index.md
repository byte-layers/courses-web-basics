---
title: "Variables CSS : un choix écrit une fois"
description: "Une page cohérente garde ses choix au même endroit : les variables CSS (propriétés personnalisées), déclarées sur :root avec deux tirets, lues avec var(), et qui suivent la cascade. Un thème change en une ligne."
tags:
  - bit
  - css
difficulty: beginner
duration: 8
requires: "0.9.0"
---

Une page cohérente écrit ses choix, ses couleurs par exemple, **à un seul endroit** : ce sont les **variables CSS**. Vous saurez déclarer une variable, la lire partout où elle sert, et changer un thème en ne modifiant qu'une ligne.

**Prérequis** : le bit [CSS : règles, sélecteurs, cascade](https://byte-layers.com/fr/bits/css-rules-cascade).

# Variables CSS : un choix écrit une fois

Dans une feuille de style qui grandit, la même couleur revient dix fois. Changer de thème veut alors dire la chercher partout, et en oublier une. Ce contenu range ces choix dans des variables.

## Les variables CSS : un choix écrit une fois

Une **variable CSS** (le nom officiel est *propriété personnalisée*, *custom property*) est une propriété dont le nom commence par deux tirets. On la déclare dans une règle, puis on lit sa valeur avec **`var()`**. Déclarée sur **`:root`**, qui vise l'élément `html`, elle est disponible dans toute la page.

```scene
lesson: assets/variables.scene.json
step: variables
```

Les trois règles ne contiennent plus la couleur, seulement son **nom**. En CSS :

```css
:root {
  --accent: rgb(219, 39, 119);    /* déclarée une fois */
}

h1 {
  color: var(--accent);            /* lue partout où elle sert */
}
```

Changer la couleur du thème revient alors à changer **une ligne**. Les variables suivent la cascade : une variable redéclarée sur un élément vaut pour lui et ses descendants, ce qui permet par exemple un thème sombre dans une seule section.

## À toi : un thème en une ligne

La couleur d'accent `rgb(219, 39, 119)` est écrite trois fois. Déclare une variable `--accent` sur `:root`, utilise-la aux trois endroits, puis change le thème en violet, `rgb(124, 58, 237)`, en ne modifiant que la variable.

```playground
runtime: web
title: Un thème en une ligne
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Camille Martin</title>
      <link rel="stylesheet" href="style.css">
    </head>
    <body>
      <nav><a href="#projets">Projets</a> <a href="#contact">Contact</a></nav>
      <h1>Camille Martin</h1>
      <a class="bouton" href="#contact">Me contacter</a>
    </body>
    </html>
  style.css: |
    body {
      font-family: system-ui, sans-serif;
    }

    nav a {
      color: rgb(219, 39, 119);
    }

    h1 {
      color: rgb(219, 39, 119);
    }

    .bouton {
      display: inline-block;
      background-color: rgb(219, 39, 119);
      color: rgb(255, 255, 255);
      padding: 10px 16px;
      text-decoration: none;
    }
open: [style.css, index.html]
lock: [index.html]
check: ask
verify:
  - label: "`--accent` est déclarée sur `:root`"
    file: style.css
    includes: "/:root\\s*\\{[^}]*--accent\\s*:/"
    hint: "`:root { --accent: rgb(219, 39, 119); }`, en tête du fichier."
  - label: "`var(--accent)` sert aux trois endroits"
    file: style.css
    includes: "/(var\\(\\s*--accent\\s*\\)[\\s\\S]*){3}/"
    hint: "Remplace chaque `rgb(219, 39, 119)` des règles par `var(--accent)`."
  - label: le titre, les liens du menu et le bouton sont violets
    selector: "h1, nav a"
    style: { color: "rgb(124, 58, 237)" }
    hint: "Une fois les trois `var(--accent)` en place, ne change que la valeur de `--accent`."
  - label: le fond du bouton est violet
    selector: .bouton
    style: { background-color: "rgb(124, 58, 237)" }
solution: assets/theme.solution
```

> 📖 [Les propriétés personnalisées, variables CSS (MDN)](https://developer.mozilla.org/fr/docs/Web/CSS/Using_CSS_custom_properties) · [var() (MDN)](https://developer.mozilla.org/fr/docs/Web/CSS/var)

## Trois questions pour vérifier

Trois situations avec une variable `--accent`. Choisis la bonne réponse, l'explication suit.

```quiz
title: "Variables CSS"
tracksProgress: false
showNotice: false
place: stage
questions:
  - prompt: "Comment lit-on la valeur de la variable `--accent` ?"
    answers:
      - "`color: --accent;`"
      - "`color: var(--accent);`"
      - "`color: $accent;`"
    correct: 2
    explanation: "Une variable CSS se lit avec var(). `$accent` est la syntaxe de Sass, un autre langage qui se compile en CSS."
  - prompt: "Pourquoi déclare-t-on souvent les variables sur `:root` ?"
    answers:
      - "Parce que `:root` vise l'élément `html` : la variable est disponible dans toute la page"
      - "Parce qu'une variable déclarée ailleurs ne fonctionne pas"
      - "Parce que le navigateur les lit plus vite"
    correct: 1
    explanation: "Une variable vaut pour l'élément qui la déclare et ses descendants. Sur :root, c'est-à-dire html, tous les éléments de la page en héritent."
  - prompt: "`--accent` est rose sur `:root`, et redéclarée en bleu dans `.sombre`. De quelle couleur est un `h1` placé dans `.sombre`, avec `color: var(--accent)` ?"
    answers:
      - "Rose, la valeur de `:root`"
      - "Bleu, la valeur de `.sombre`"
      - "Noir, la couleur par défaut"
    correct: 2
    explanation: "Les variables suivent la cascade : redéclarée sur .sombre, la valeur bleue vaut pour cet élément et tous ses descendants, et remplace celle de :root."
```

## Récap

- Une **variable CSS** (*propriété personnalisée*) a un nom qui commence par deux tirets : `--accent`.
- On la déclare souvent sur **`:root`**, qui vise l'élément `html` : elle sert dans toute la page.
- On la lit avec **`var(--accent)`** : un thème change en une ligne.
- Elle suit la **cascade** : redéclarée sur un élément, elle vaut pour lui et ses descendants.

Vos choix sont maintenant rangés à un seul endroit. Reste à faire bouger la page, au survol d'un bouton ou à l'arrivée d'un bloc, sans gêner personne : c'est l'objet du contenu [Transitions et animations CSS](https://byte-layers.com/fr/bits/css-motion).

```ack
J'ai compris
```
