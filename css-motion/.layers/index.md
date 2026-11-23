---
title: "Transitions et animations CSS"
description: "Une page qui bouge sans gêner : les effets au survol et au focus, les transitions déclarées sur l'état normal, les animations @keyframes (opacity, transform), et prefers-reduced-motion pour ceux que le mouvement dérange."
tags:
  - bit
  - css
difficulty: beginner
duration: 15
requires: "0.9.0"
---

Une page peut bouger, au survol d'un bouton ou à l'arrivée d'un bloc, avec des **transitions** et des **animations**. Vous saurez écrire une transition qui joue dans les deux sens, décrire une animation avec `@keyframes`, et respecter le réglage de ceux qui demandent moins de mouvement.

**Prérequis** : le bit [CSS : règles, sélecteurs, cascade](https://byte-layers.com/fr/bits/css-rules-cascade), et le bit [L'accessibilité web](https://byte-layers.com/fr/bits/web-accessibility) pour le focus visible.

# Transitions et animations CSS

Un bouton qui change de couleur d'un coup, un bloc qui surgit : le changement est brutal. Ce contenu l'étale dans le temps, puis fait bouger la page sans gêner personne.

## Les transitions : sur l'état normal, pas sur le survol

Les pseudo-classes **`:hover`** (la souris survole l'élément) et **`:focus-visible`** (il a le focus au clavier) changent son style. Écrivez-les ensemble : un effet réservé à la souris n'existe pas pour qui navigue au clavier.

Sans rien d'autre, le changement est brutal. La propriété **`transition`** l'étale dans le temps : `transition: background-color 0.3s` fait passer la couleur de fond d'une valeur à l'autre en trois dixièmes de seconde.

```scene
lesson: assets/motion.scene.json
step: transition
```

Le piège : la transition se déclare sur **l'état normal** de l'élément. Posée seulement dans `:hover`, elle ne joue qu'à l'aller ; au départ de la souris, l'élément retrouve son état normal, qui n'a pas de transition, et le retour est brutal.

## À toi : une transition dans les deux sens

La transition du bouton est écrite dans `.bouton:hover`. Survole le bouton dans l'aperçu : l'aller est doux, le retour sec. Déplace-la dans `.bouton`, et fais jouer le même effet au focus clavier.

```playground
runtime: web
title: Une transition dans les deux sens
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
      <a class="bouton" href="#contact">Me contacter</a>
    </body>
    </html>
  style.css: |
    body {
      font-family: system-ui, sans-serif;
      padding: 24px;
    }

    .bouton {
      display: inline-block;
      background-color: rgb(219, 39, 119);
      color: rgb(255, 255, 255);
      padding: 10px 16px;
      text-decoration: none;
    }

    .bouton:hover {
      background-color: rgb(124, 58, 237);
      transition: background-color 0.3s;
    }
open: [style.css, index.html]
lock: [index.html]
verify:
  - label: la transition est déclarée sur l'état normal du bouton
    selector: .bouton
    style: { transition-duration: 0.3s, transition-property: "/background-color|all/" }
    hint: "Déplace `transition: background-color 0.3s;` de `.bouton:hover` vers `.bouton`."
  - label: le même effet s'applique au focus clavier
    file: style.css
    includes: "/\\.bouton:focus(-visible)?\\s*[,{]|,\\s*\\.bouton:focus/"
    hint: "Une règle pour deux états : `.bouton:hover, .bouton:focus-visible { … }`."
solution: assets/transition.solution
```

## Les animations : @keyframes

Une transition va d'un état à un autre quand quelque chose change. Une **animation** joue toute seule, au chargement par exemple, d'après des étapes nommées dans une règle **`@keyframes`**.

```scene
lesson: assets/motion.scene.json
step: animation
```

La règle `@keyframes` qui décrit ces deux étapes, et la propriété `animation` qui les joue :

```css
@keyframes apparition {
  from { opacity: 0; transform: translateY(20px); }   /* invisible, 20px plus bas */
  to   { opacity: 1; transform: translateY(0); }      /* visible, à sa place */
}

.banniere {
  animation: apparition 0.6s ease-out;   /* nom, durée, courbe */
}
```

| Morceau | Rôle |
|---|---|
| `@keyframes apparition` | nomme une suite d'étapes |
| `from`, `to` (ou `0%`, `50%`, `100%`) | le style à chaque étape |
| `animation: apparition 0.6s ease-out` | joue les étapes `apparition` en 0,6 s, en ralentissant à la fin |

Les propriétés **`opacity`** et **`transform`** sont celles qu'on anime de préférence : le navigateur les anime sans recalculer la disposition de la page, donc sans saccade.

## Le piège : prefers-reduced-motion

Pour certaines personnes, notamment celles qui ont des **troubles vestibulaires** (l'oreille interne, qui gère l'équilibre), un bloc qui glisse ou un fond qui défile provoque des vertiges et des nausées. Les systèmes d'exploitation ont un réglage pour **réduire les animations** (macOS : Accessibilité, Affichage ; Windows : Accessibilité, Effets visuels ; Android et iOS aussi).

```scene
lesson: assets/motion.scene.json
step: reduit
```

La media query **`prefers-reduced-motion: reduce`** permet à la page de respecter ce réglage :

```css
@media (prefers-reduced-motion: reduce) {
  .banniere {
    animation: none;
  }
}
```

## À toi : moins de mouvement sur demande

La bannière glisse à chaque chargement, même pour qui a demandé moins de mouvement. Ajoute à la fin de `style.css` la media query qui coupe son animation dans ce cas.

```playground
runtime: web
title: Moins de mouvement sur demande
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
      <header class="banniere">
        <h1>Camille Martin</h1>
        <p>Développeuse web à Toulouse</p>
      </header>
    </body>
    </html>
  style.css: |
    body {
      font-family: system-ui, sans-serif;
      margin: 0;
    }

    @keyframes glisse {
      from { transform: translateX(-100%); }
      to   { transform: translateX(0); }
    }

    .banniere {
      background-color: rgb(30, 41, 59);
      color: rgb(255, 255, 255);
      padding: 24px;
      animation: glisse 1.2s ease-out;
    }
open: [style.css, index.html]
lock: [index.html]
verify:
  - label: l'animation est coupée quand le système demande moins de mouvement
    file: style.css
    includes: "/prefers-reduced-motion\\s*:\\s*(reduce\\s*\\)\\s*\\{[\\s\\S]*animation(-name)?\\s*:\\s*none|no-preference)/"
    hint: "`@media (prefers-reduced-motion: reduce) { .banniere { animation: none; } }`"
solution: assets/mouvement.solution
```

L'aperçu ne peut pas simuler ce réglage, d'où le contrôle sur le texte du fichier. Dans Chrome, le panneau *Rendering* des outils de développement (menu ⋮, *More tools*, *Rendering*) a une option *Emulate CSS media feature prefers-reduced-motion* : choisissez `reduce` et rechargez, la bannière ne glisse plus.

> 📖 [Les transitions CSS (MDN)](https://developer.mozilla.org/fr/docs/Web/CSS/CSS_transitions/Using_CSS_transitions) · [Les animations CSS (MDN)](https://developer.mozilla.org/fr/docs/Web/CSS/CSS_animations/Using_CSS_animations) · [prefers-reduced-motion (MDN)](https://developer.mozilla.org/fr/docs/Web/CSS/@media/prefers-reduced-motion)

## Trois questions pour vérifier

Trois situations : un bouton, une animation, un réglage du système. Choisis la bonne réponse, l'explication suit.

```quiz
title: "Transitions et animations CSS"
tracksProgress: false
showNotice: false
place: stage
questions:
  - prompt: "La transition d'un bouton est écrite seulement dans `.bouton:hover`. Que voit-on ?"
    answers:
      - "Un effet doux à l'arrivée de la souris, et un retour brutal à son départ"
      - "Un effet doux dans les deux sens"
      - "Aucun effet"
    correct: 1
    explanation: "Au départ de la souris, c'est l'état normal qui s'applique, et il n'a pas de transition. Elle se déclare sur .bouton."
  - prompt: "Une bannière doit apparaître en glissant au chargement. Quelles propriétés animer de préférence ?"
    answers:
      - "`width` et `margin`"
      - "`opacity` et `transform`"
      - "`display` et `position`"
    correct: 2
    explanation: "Le navigateur anime opacity et transform sans recalculer la disposition de la page, donc sans saccade. width et margin la font recalculer à chaque image."
  - prompt: "À quoi sert `@media (prefers-reduced-motion: reduce)` ?"
    answers:
      - "À accélérer les animations sur un téléphone lent"
      - "À appliquer des règles quand la personne a demandé à son système de réduire les animations"
      - "À désactiver toutes les animations du navigateur"
    correct: 2
    explanation: "La media query lit un réglage d'accessibilité du système ; c'est à la page de couper ou d'adoucir ses animations."
```

## Récap

- **`:hover`** et **`:focus-visible`** s'écrivent ensemble, pour la souris et pour le clavier.
- **`transition`** se déclare sur l'**état normal** ; posée sur `:hover` seulement, le retour est brutal.
- **`@keyframes`** décrit une animation ; on anime de préférence `opacity` et `transform`.
- **`prefers-reduced-motion: reduce`** respecte ceux que le mouvement rend malades : coupez ou adoucissez vos animations.

Tout ce que vous écrivez à la main, des bibliothèques le proposent tout fait, en classes prêtes à l'emploi : c'est l'objet du contenu [Bootstrap : des classes toutes faites](https://byte-layers.com/fr/bits/css-frameworks).

```ack
J'ai compris
```
