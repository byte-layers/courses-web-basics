---
title: "CSS : règles, sélecteurs et cascade"
description: "Une règle CSS (sélecteur, propriété, valeur), la feuille de style reliée par link, les sélecteurs de balise, de classe et d'id, un CSS qui ne signale aucune erreur, et la cascade : héritage, ordre et spécificité, pour savoir quelle règle gagne."
tags:
  - bit
  - web
  - css
difficulty: beginner
duration: 15
requires: "0.9.0"
---

L'apparence d'une page s'écrit dans un second langage, le **CSS** : des règles qui visent des éléments du HTML et disent à quoi ils ressemblent. Vous saurez écrire une règle, relier une feuille de style à une page, viser une balise, une classe ou un id, repérer une règle qui ne fait rien alors que rien ne vous le signale, et prédire quelle règle gagne quand deux se disputent le même élément : c'est la **cascade**.

**Prérequis** : [Le HTML sémantique : le sens avant la forme](https://byte-layers.com/fr/bits/semantic-html), pour les balises qui nomment les zones d'une page, et [Une page web : HTML, CSS et JavaScript](https://byte-layers.com/fr/bits/web-page-languages), pour la balise `<link>`.

# CSS : règles, sélecteurs et cascade

Le HTML a dit ce qu'est chaque bloc de la page. Le CSS dit à quoi il ressemble, dans un fichier à part : une même feuille de style peut habiller cent pages, et changer une couleur à un seul endroit les change toutes.

## Une règle : un sélecteur, des déclarations

Une feuille de style est une suite de **règles**. En voici une :

```css
h2 {
  color: rgb(11, 107, 203);
  text-align: center;
}
```

| Morceau | Nom | Rôle |
|---|---|---|
| `h2` | le **sélecteur** | les éléments visés : ici, tous les `<h2>` de la page |
| `{ … }` | le bloc de déclarations | ce qu'on applique aux éléments visés |
| `color` | une **propriété** | ce qu'on règle : la couleur du texte |
| `rgb(11, 107, 203)` | la **valeur** | ici un bleu, en rouge, vert et bleu de 0 à 255 ; on écrit aussi `#0b6bcb` ou `blue` |
| `;` | la fin de la déclaration | à ne pas oublier entre deux déclarations |

Les propriétés du texte sont celles qu'on règle en premier : `font-family` pour la police, `font-size` pour la taille, `font-weight: bold` pour le gras, `color`, `text-align`, et `line-height` pour l'interligne. Pour la police, on donne une **liste de repli** : `font-family: system-ui, "Segoe UI", sans-serif` essaie la police du système, puis Segoe UI, puis n'importe quelle police sans empattements. On finit toujours par une famille générique, `sans-serif` ou `serif`, qui existe partout.

Une règle peut s'écrire à trois endroits : dans un attribut `style=""` sur une balise, entre les balises `<style>` dans le `<head>`, ou dans un fichier à part relié par `<link rel="stylesheet" href="style.css">`. On préfère le fichier à part : le HTML garde le contenu, le CSS l'apparence, et une feuille sert à toutes les pages du site.

## Viser une balise, une classe ou un id

Le sélecteur choisit les éléments visés. Trois formes suffisent pour commencer :

| Sélecteur | Écrit | Vise | Dans le HTML |
|---|---|---|---|
| de **balise** | `h2` | tous les éléments de ce type | `<h2>` |
| de **classe** | `.intro`, avec un point | tous les éléments qui portent cette classe, autant qu'on veut | `<p class="intro">` |
| d'**id** | `#presentation`, avec un dièse | l'unique élément qui porte cet id | `<section id="presentation">` |

Un élément peut porter plusieurs classes, séparées par une espace : `class="carte carte--importante"`. On nomme une classe par son **rôle** (`intro`, `prix`, `banniere`), pas par son apparence (`bleu`, `gros`) : le jour où la couleur change, le nom reste juste. Et on préfère les classes aux id pour le style : un id ne sert qu'une fois.

Deux autres formes reviennent souvent : `h1, h2` vise les deux balises d'un coup (la virgule) ; `nav a` vise les liens **à l'intérieur** d'un `<nav>` (l'espace).

La page ci-dessous, celle d'une médiathèque, est fournie en lecture seule. Écris dans `style.css` les règles qui l'habillent.

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
    hint: "`font-family: system-ui, \"Segoe UI\", sans-serif;` : plusieurs polices séparées par des virgules, une famille générique en dernier"
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
  - label: seule la section `#presentation` a un fond blanc
    selector: "#presentation"
    style: { background-color: "rgb(255, 255, 255)" }
    hint: "Le dièse vise un id : `#presentation { background-color: white; }`"
solution: assets/selecteurs.solution
```

Regardez la section des nouveautés : son paragraphe `.intro` est en gras, comme celui de la présentation, parce qu'une classe vise tous les éléments qui la portent. Son fond, lui, n'a pas changé : l'id ne visait qu'un élément.

## Le CSS ne signale rien : un fichier non relié, une faute de frappe

Le CSS est indulgent : une propriété mal écrite, une valeur inconnue, un sélecteur qui ne vise rien sont **ignorés en silence**. Pas de message d'erreur, pas de page cassée : la règle ne fait rien, et c'est tout. C'est voulu, pour qu'un vieux navigateur saute ce qu'il ne connaît pas sans casser la page, mais c'est la panne la plus fréquente du débutant.

Deux causes reviennent sans cesse : la feuille de style n'est pas reliée (balise `<link>` absente, ou nom de fichier différent), et une faute de frappe dans une propriété. Dans la page ci-dessous, le prix devrait être grand et gras, et le titre bleu foncé. Rien ne marche. Trouve les deux fautes : l'une est dans `index.html`, l'autre dans `style.css`.

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

Dans un vrai navigateur, les outils de développement signalent ces deux pannes à qui sait regarder : clic droit sur l'élément, **Inspecter**, puis le panneau des styles. Une propriété inconnue y apparaît barrée, avec un triangle d'avertissement ; une règle dont le sélecteur ne vise pas l'élément n'y apparaît pas du tout. Le lab de ce cours vous y emmène.

## La cascade : quand deux règles se disputent

Un même élément est souvent visé par plusieurs règles. Quand elles règlent des propriétés différentes, elles s'additionnent. Quand elles règlent la même propriété avec deux valeurs, le navigateur en choisit une : c'est la **cascade** (le C de CSS). Il compare, dans l'ordre :

| Critère | La règle qui gagne | Exemple |
|---|---|---|
| 1. l'origine | vos règles battent les styles par défaut du navigateur | votre `a { color: … }` remplace le bleu des liens |
| 2. la **spécificité** | la règle au sélecteur le plus précis | `#contenu p` bat `.alerte` |
| 3. l'**ordre** | à spécificité égale, la dernière écrite | deux règles `p`, la seconde gagne |

La spécificité se compte en trois chiffres : le nombre d'id, puis de classes, puis de balises du sélecteur. On compare le premier chiffre, puis le deuxième en cas d'égalité, puis le troisième.

| Sélecteur | id | classes | balises | Spécificité |
|---|---|---|---|---|
| `p` | 0 | 0 | 1 | 0-0-1 |
| `.alerte` | 0 | 1 | 0 | 0-1-0 |
| `main .alerte` | 0 | 1 | 1 | 0-1-1 |
| `#contenu p` | 1 | 0 | 1 | 1-0-1 |
| `#contenu .alerte` | 1 | 1 | 0 | 1-1-0 |

Un attribut `style=""` écrit sur la balise bat toutes ces règles, et le mot `!important` à la fin d'une déclaration passe devant tout le reste. On les évite : ils gagnent aujourd'hui, et compliquent chaque modification de demain.

Enfin, certaines propriétés passent du parent à ses enfants : c'est l'**héritage**. La police et la couleur du texte posées sur `body` descendent dans tous les paragraphes, sans qu'on les répète. Les marges, les bordures et les fonds, eux, ne s'héritent pas.

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

> 📖 [Les bases du CSS (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Styling_basics/Getting_started) · [Les sélecteurs CSS (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Styling_basics/Basic_selectors) · [Cascade, spécificité et héritage (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Styling_basics/Handling_conflicts) · [Le validateur CSS du W3C](https://jigsaw.w3.org/css-validator/)

## Trois questions pour vérifier ce que vous avez retenu

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
```

## Récap

- Une **règle** CSS : un **sélecteur**, puis des déclarations `propriété: valeur;` entre accolades ; on la range dans un fichier relié par `<link rel="stylesheet" href="…">`.
- Trois sélecteurs : la **balise** (`h2`, tous), la **classe** (`.intro`, tous ceux qui la portent), l'**id** (`#presentation`, un seul). Une classe se nomme par son rôle.
- Le CSS **ignore en silence** ce qu'il ne comprend pas : un fichier non relié ou une faute de frappe ne font rien, sans message.
- La **cascade** départage deux règles : l'origine, puis la **spécificité** (id, classes, balises), puis l'**ordre**. `style=""` et `!important` passent devant, et on les évite.
- L'**héritage** fait descendre la police et la couleur du parent vers ses enfants.

Une règle a donné une couleur, une police, un fond. Reste la place que prend chaque élément, et sa taille réelle, qui n'est pas toujours celle qu'on a écrite : c'est l'objet du contenu [Le modèle de boîte](https://byte-layers.com/fr/bits/box-model).

```ack
J'ai compris
```
