---
title: "CSS : règles, sélecteurs et cascade"
description: "Une règle CSS (sélecteur, propriété, valeur), la feuille de style reliée par link, les propriétés du texte et la liste de repli des polices, les sélecteurs de balise, de classe et d'id, un CSS qui ne signale aucune erreur, et la cascade : spécificité, ordre et héritage, pour savoir quelle règle gagne."
tags:
  - bit
  - web
  - css
difficulty: beginner
duration: 25
requires: "0.9.0"
---

L'apparence d'une page s'écrit dans un second langage, le **CSS** : des règles qui visent des éléments du HTML et disent à quoi ils ressemblent. Vous saurez écrire une règle, relier une feuille de style à une page, viser une balise, une classe ou un id, repérer une règle qui ne fait rien alors que rien ne vous le signale, et prédire quelle règle gagne quand deux se disputent le même élément : c'est la **cascade**.

**Prérequis** : [Le HTML sémantique : le sens avant la forme](https://byte-layers.com/fr/bits/semantic-html), pour les balises qui nomment les zones d'une page, et [Une page web : HTML, CSS et JavaScript](https://byte-layers.com/fr/bits/web-page-languages), pour la balise `<link>`.

# CSS : règles, sélecteurs et cascade

Le HTML dit ce qu'est chaque bloc de la page. Le CSS dit à quoi il ressemble, dans un fichier à part : une même feuille de style peut habiller cent pages, et changer une couleur à un seul endroit les change toutes.

## Une règle, morceau par morceau

Une feuille de style est une suite de **règles**. Chacune dit : *ces éléments-là* ressemblent à *ceci*. En voici une, lue morceau par morceau.

```scene
lesson: assets/syntaxe.scene.json
step: anatomie
```

| Morceau | Ce que c'est |
|---|---|
| `h2` | le **sélecteur** : les éléments visés, ici tous les `<h2>` |
| `{ … }` | le **bloc de déclarations** |
| `color` | la **propriété** (*color*, couleur du texte) : ce qu'on règle |
| `rgb(11, 107, 203)` | la **valeur** : un bleu, en rouge, vert et bleu de 0 à 255 ; on écrit aussi `#0b6bcb` ou `blue` |
| `;` | la fin d'une déclaration, avant la suivante |

## À toi : écris ta première règle

Complète la règle qui rend les paragraphes bleu foncé et les centre : quatre signes de ponctuation. Ce n'est pas celle du HTML : entre la propriété et sa valeur, ni `=` ni guillemets.

```fill
file: assets/regle.fill.css
solution: assets/regle.css
title: Une règle pour les paragraphes
blanks:
  - answers: ["{"]
    hint: Le bloc de déclarations s'ouvre par une accolade.
  - answers: [":"]
    hint: "Entre la propriété et sa valeur : deux-points, pas `=`."
  - answers: [";"]
    hint: Une déclaration se termine par un point-virgule, avant la suivante.
  - answers: ["}"]
    hint: Le bloc se ferme par l'accolade fermante.
```

Le `;` oublié est le piège classique : la déclaration suivante est lue comme la suite de la valeur, et **les deux** sont ignorées.

## Une règle vise tous les éléments de son sélecteur

Une règle ne vise pas un endroit de la page : elle vise **tous** les éléments que décrit son sélecteur.

```scene
lesson: assets/css.scene.json
step: regle
```

Les deux titres `<h2>` ont changé ensemble ; le `<h1>` et le paragraphe n'ont pas bougé. Pour viser l'un sans l'autre, il faut un sélecteur plus précis : on y vient juste après les feuilles de style et les polices.

## Une feuille de style pour toutes les pages

Des déclarations peuvent s'écrire à trois endroits : dans un attribut `style=""` sur une balise, entre `<style>` et `</style>` dans le `<head>`, ou dans un **fichier à part** relié par `<link rel="stylesheet" href="style.css">` (*stylesheet*, feuille de style). On préfère le fichier à part. Voici pourquoi.

```scene
lesson: assets/css.scene.json
step: ranger
```

Une seule feuille habille toutes les pages qui la relient : on change une couleur à **un seul endroit**, et tout le site suit. Le HTML garde le contenu, le CSS l'apparence.

## Les propriétés du texte, et la liste de repli

Les propriétés du texte sont celles qu'on règle en premier : `font-family` (la police), `font-size` (la taille), `font-weight: bold` (le gras), `color`, `text-align` (l'alignement) et `line-height` (l'interligne). Pour la police, on donne une **liste de repli** : le visiteur n'a pas forcément celle qu'on a choisie.

```scene
lesson: assets/syntaxe.scene.json
step: repli
```

La liste finit toujours par une **famille générique**, `sans-serif` (sans empattements) ou `serif` (avec), que tout appareil sait afficher.

## Viser une balise, une classe ou un id

Le sélecteur choisit les éléments visés. Trois formes suffisent pour commencer :

| Sélecteur | Ce qu'il vise |
|---|---|
| `h2`, une **balise** | tous les `<h2>` |
| `.intro`, une **classe**, avec un point | tous les éléments qui portent `class="intro"` |
| `#presentation`, un **id**, avec un dièse | l'unique élément qui porte `id="presentation"` |

```scene
lesson: assets/css.scene.json
step: selecteurs
```

Un élément peut porter plusieurs classes : `class="intro important"`. On nomme une classe par son **rôle** (`intro`, `prix`), pas par son apparence (`bleu`) : le jour où la couleur change, le nom reste juste. Deux autres formes reviennent souvent : `h1, h2` vise les deux balises (la virgule) ; `nav a` vise les liens **à l'intérieur** d'un `<nav>` (l'espace).

## À toi : habille la page de la médiathèque

La page d'une médiathèque est fournie en lecture seule. Écris dans `style.css` les règles qui l'habillent : la police et l'interligne sur `body`, puis une règle par sélecteur.

```playground
runtime: web
title: Habille la page de la médiathèque
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Médiathèque des Trois Rivières</title>
      <link rel="stylesheet" href="style.css">
    </head>
    <body>
      <header>
        <h1>Médiathèque des Trois Rivières</h1>
      </header>
      <main>
        <section id="presentation">
          <h2>Bienvenue</h2>
          <p class="intro">Plus de 40 000 ouvrages et une salle de lecture ouverte à tous.</p>
          <p>L'inscription est gratuite pour les moins de dix-huit ans.</p>
        </section>
        <section id="nouveautes">
          <h2>Nos nouveautés</h2>
          <p class="intro">Une sélection renouvelée chaque mois par l'équipe.</p>
        </section>
      </main>
    </body>
    </html>
  style.css: |
    /* Écris tes règles ici */
open: [style.css, index.html]
lock: [index.html]
verify:
  - label: le `body` a une police sans empattements, avec une liste de repli
    selector: body
    style: { font-family: "/,\\s*sans-serif$/" }
    hint: "`font-family: \"Segoe UI\", Verdana, sans-serif;` : plusieurs polices séparées par des virgules, une famille générique en dernier"
  - label: le `body` a un interligne d'au moins 1.5
    selector: body
    style: { line-height: "/^(2[4-9]|[3-9][0-9])(\\.[0-9]+)?px$/" }
    hint: "`line-height: 1.6;` : 1,6 fois la taille du texte"
  - label: les deux titres `h2` sont bleus, `rgb(11, 107, 203)`
    selector: h2
    style: { color: "rgb(11, 107, 203)" }
  - label: les deux paragraphes `.intro` sont en gras
    selector: .intro
    style: { font-weight: "700" }
    hint: "Le point vise une classe : `.intro { font-weight: bold; }`"
  - label: seule la section `#presentation` a un fond bleu très clair, `rgb(232, 240, 254)`
    selector: "#presentation"
    style: { background-color: "rgb(232, 240, 254)" }
    hint: "Le dièse vise un id : `#presentation { background-color: rgb(232, 240, 254); }`"
solution: assets/selecteurs.solution
```

Regarde la section des nouveautés : son paragraphe `.intro` est en gras, comme celui de la présentation, parce qu'une classe vise tous les éléments qui la portent. Son fond, lui, n'a pas changé : l'id ne visait qu'un élément.

## Le CSS ne signale rien

Le CSS est indulgent : un fichier introuvable, une propriété mal écrite, une valeur inconnue sont **ignorés en silence**. Pas de message, pas de page cassée : la règle ne fait rien, et c'est tout.

```scene
lesson: assets/syntaxe.scene.json
step: silence
```

C'est voulu : un vieux navigateur saute ce qu'il ne connaît pas sans casser la page. Pour voir la panne : clic droit sur l'élément, **Inspecter**, puis le panneau des styles. Une propriété inconnue y apparaît **barrée**, avec un triangle d'avertissement ; une règle dont le sélecteur ne vise pas l'élément n'y apparaît pas du tout.

## À toi : le CSS qui ne fait rien

Dans la page ci-dessous, le prix devrait être grand et gras, et le titre bleu foncé. Rien ne marche. Trouve les deux fautes : l'une est dans `index.html`, l'autre dans `style.css`.

```playground
runtime: web
title: Le CSS qui ne fait rien
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Nous rejoindre</title>
      <link rel="stylesheet" href="styles.css">
    </head>
    <body>
      <h1>Nous rejoindre</h1>
      <p>L'adhésion annuelle à la médiathèque :</p>
      <p class="prix">12 €</p>
    </body>
    </html>
  style.css: |
    h1 {
      colour: rgb(20, 69, 123);
    }

    .prix {
      font-size: 32px;
      font-weight: bold;
    }
open: [index.html, style.css]
verify:
  - label: le prix est grand, 32 px, la feuille de style est donc reliée
    selector: .prix
    style: { font-size: 32px }
    hint: "Compare le nom écrit dans `href` et le nom de l'onglet du fichier CSS, lettre par lettre"
  - label: le titre est bleu foncé, `rgb(20, 69, 123)`
    selector: h1
    style: { color: "rgb(20, 69, 123)" }
    hint: "Relis le nom de la propriété dans la règle `h1` : le CSS est écrit en anglais américain"
solution: assets/silence.solution
```

## La cascade : quand deux règles se disputent

Quand deux règles donnent deux valeurs à la même propriété d'un élément, le navigateur en choisit une : c'est la **cascade**, le C de CSS (*Cascading Style Sheets*, feuilles de style en cascade).

```scene
lesson: assets/css.scene.json
step: cascade
```

Il compare, dans l'ordre :

| Critère | La règle qui gagne |
|---|---|
| 1. l'origine | les vôtres, contre les styles par défaut du navigateur |
| 2. la **spécificité** | la plus précise : `#contenu p` bat `.alerte` |
| 3. l'**ordre** | à spécificité égale, la dernière écrite |

| Sélecteur | Spécificité : id-classes-balises |
|---|---|
| `p` | 0-0-1 |
| `.alerte` | 0-1-0 |
| `main .alerte` | 0-1-1 |
| `#contenu p` | 1-0-1 |

On compare le premier chiffre, puis le suivant en cas d'égalité. Un attribut `style=""` bat toutes ces règles, et `!important` à la fin d'une déclaration passe devant tout : on les évite, ils compliquent chaque modification.

## À toi : qui gagne ?

Dans la page ci-dessous, l'avertissement devrait être rouge, et il reste gris. Trouve pourquoi, puis rends-le rouge **sans modifier ni supprimer la première règle**, et sans `!important`.

```playground
runtime: web
title: Qui gagne ?
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Infos pratiques</title>
      <link rel="stylesheet" href="style.css">
    </head>
    <body>
      <main id="contenu">
        <h1>Infos pratiques</h1>
        <p class="alerte">Fermeture exceptionnelle le 11 novembre.</p>
        <p>Ouvert du mardi au samedi, de 10 h à 18 h.</p>
      </main>
    </body>
    </html>
  style.css: |
    #contenu p {
      color: rgb(51, 51, 51);
    }

    .alerte {
      color: rgb(220, 38, 38);
      font-weight: bold;
    }
open: [style.css, index.html]
lock: [index.html]
check: ask
verify:
  - label: l'avertissement est rouge, `rgb(220, 38, 38)`
    selector: .alerte
    style: { color: "rgb(220, 38, 38)" }
    hint: "Compte la spécificité des deux sélecteurs : `#contenu p` fait 1-0-1, `.alerte` 0-1-0. Rends le second plus précis que le premier"
  - label: l'autre paragraphe reste gris, `rgb(51, 51, 51)`
    selector: "#contenu p:not(.alerte)"
    style: { color: "rgb(51, 51, 51)" }
  - label: la première règle est restée telle quelle
    file: style.css
    includes: "/#contenu p\\s*\\{\\s*color:\\s*rgb\\(51, 51, 51\\);?\\s*\\}/"
  - label: sans `!important`
    file: style.css
    excludes: "!important"
solution: assets/cascade.solution
```

## L'héritage : ce qui descend du parent

Certaines propriétés passent du parent à ses enfants : c'est l'**héritage**.

```scene
lesson: assets/css.scene.json
step: heritage
```

La police et la couleur du texte posées sur `body` descendent dans tous les titres et les paragraphes, sans qu'on les répète. Les marges, les bordures et les fonds, eux, **ne s'héritent pas**. Et une règle qui vise l'élément lui-même passe toujours avant ce qu'il hérite.

## À toi : une seule règle sur `body`

Dans la feuille ci-dessous, trois règles répètent la même police et la même couleur. Remplace-les par **une seule règle** sur `body` : la page doit rester identique.

```playground
runtime: web
title: Une seule règle sur body
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Le club de lecture</title>
      <link rel="stylesheet" href="style.css">
    </head>
    <body>
      <h1>Le club de lecture</h1>
      <p>Rendez-vous le premier jeudi du mois, à 18 h.</p>
      <ul>
        <li>Septembre : un roman</li>
        <li>Octobre : une bande dessinée</li>
      </ul>
    </body>
    </html>
  style.css: |
    h1 {
      font-family: Georgia, serif;
      color: rgb(20, 69, 123);
    }

    p {
      font-family: Georgia, serif;
      color: rgb(20, 69, 123);
    }

    li {
      font-family: Georgia, serif;
      color: rgb(20, 69, 123);
    }
open: [style.css, index.html]
lock: [index.html]
check: ask
verify:
  - label: le `body` porte la police et la couleur
    selector: body
    style: { font-family: "/^Georgia, serif$/", color: "rgb(20, 69, 123)" }
    hint: "`body { font-family: Georgia, serif; color: rgb(20, 69, 123); }`"
  - label: le titre, le paragraphe et la liste les héritent
    selector: "h1, p, li"
    style: { font-family: "/^Georgia, serif$/", color: "rgb(20, 69, 123)" }
  - label: plus de règle `h1`, `p` ni `li`
    file: style.css
    excludes: "/(^|\\n)\\s*(h1|p|li)\\s*[{,]/"
    hint: "Supprime les trois règles : l'héritage fait le travail"
solution: assets/heritage.solution
```

> 📖 [Les bases du CSS (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Styling_basics/Getting_started) · [Les sélecteurs CSS (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Styling_basics/Basic_selectors) · [Cascade, spécificité et héritage (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Styling_basics/Handling_conflicts) · [Le validateur CSS du W3C](https://jigsaw.w3.org/css-validator/)

## Quatre questions pour vérifier ce que vous avez retenu

```quiz
title: "Règles, sélecteurs et cascade"
tracksProgress: false
showNotice: false
place: stage
questions:
  - prompt: "Deux paragraphes portent `class=\"intro\"`, une section porte `id=\"presentation\"`. Que visent `.intro` et `#presentation` ?"
    answers:
      - "`.intro` vise les deux paragraphes ; `#presentation` vise la seule section"
      - "`.intro` vise le premier paragraphe seulement ; `#presentation` vise toute la page"
      - "Les deux visent tous les éléments de la page"
    correct: 1
    explanation: "Une classe vise tous les éléments qui la portent ; un id est unique dans la page, et vise un seul élément."
  - prompt: "Vous écrivez `p { colr: red; }`. Que se passe-t-il ?"
    answers:
      - "Le navigateur affiche une erreur dans la page"
      - "La déclaration est ignorée en silence : les paragraphes gardent leur couleur"
      - "Le navigateur corrige en `color` et colore les paragraphes en rouge"
    correct: 2
    explanation: "Le CSS ignore ce qu'il ne connaît pas, sans rien signaler. Seul le panneau des styles des outils de développement montre la propriété barrée."
  - prompt: "Un paragraphe `<p class=\"note\">` est dans `<main id=\"contenu\">`. La feuille contient `#contenu p { color: gray; }` puis, plus bas, `.note { color: green; }`. De quelle couleur est-il ?"
    answers:
      - "Vert, parce que la règle `.note` est écrite après"
      - "Vert, parce qu'une classe bat une balise"
      - "Gris, parce que `#contenu p` (1-0-1) est plus spécifique que `.note` (0-1-0)"
    correct: 3
    explanation: "L'ordre ne départage que deux règles de même spécificité. Ici, l'id de `#contenu p` l'emporte sur la classe de `.note`."
  - prompt: "La feuille contient `body { color: navy; }` et `p { color: green; }`. De quelle couleur sont un `<h1>` et un `<p>` de la page ?"
    answers:
      - "Tous les deux bleu marine : `body` contient tout"
      - "Le `<h1>` bleu marine, hérité de `body` ; le `<p>` vert, sa propre règle passe avant l'héritage"
      - "Le `<h1>` garde la couleur par défaut : seul `<body>` est visé"
    correct: 2
    explanation: "La couleur s'hérite : le `<h1>`, sans règle à lui, prend celle de `body`. Le `<p>` a sa propre règle, qui passe avant ce qu'il hérite."
```

## Récap

- Une **règle** CSS : un **sélecteur**, puis des déclarations `propriété: valeur;` entre accolades ; on la range dans un fichier relié par `<link rel="stylesheet" href="…">`, qui sert à toutes les pages.
- Une **liste de repli** de polices finit par une famille générique, `sans-serif` ou `serif`.
- Trois sélecteurs : la **balise** (`h2`, tous), la **classe** (`.intro`, tous ceux qui la portent), l'**id** (`#presentation`, un seul). Une classe se nomme par son rôle.
- Le CSS **ignore en silence** ce qu'il ne comprend pas : un fichier non relié ou une faute de frappe ne font rien, sans message.
- La **cascade** départage deux règles : l'origine, puis la **spécificité** (id, classes, balises), puis l'**ordre**. `style=""` et `!important` passent devant, et on les évite.
- L'**héritage** fait descendre la police et la couleur du parent vers ses enfants ; une règle propre à l'enfant passe avant.

Une règle a donné une couleur, une police, un fond. Reste la place que prend chaque élément, et sa taille réelle, qui n'est pas toujours celle qu'on a écrite : c'est l'objet du contenu [Le modèle de boîte](https://byte-layers.com/fr/bits/box-model).

```ack
J'ai compris
```
