---
title: "Bloc, inline : le flux normal d'une page"
description: "Sans règle de disposition, le navigateur range les boîtes tout seul : les blocs les uns sous les autres, les éléments inline dans la ligne. Prédire où tombe chaque élément, la marge verticale ignorée sur un inline, inline-block, et ce que le flux ne sait pas faire."
tags:
  - bit
  - css
  - html
difficulty: beginner
duration: 20
requires: "0.9.0"
---

Sans aucune règle de disposition, le navigateur range déjà les éléments d'une page : c'est le **flux normal**. Vous saurez prédire où tombe chaque élément, pourquoi une marge verticale ne fait rien sur un lien ou un `span`, ce que change `display: inline-block`, et ce que le flux ne sait pas faire seul.

**Prérequis** : le bit [Le modèle de boîte](https://byte-layers.com/fr/bits/box-model) (contenu, padding, bordure, marge), et savoir écrire une page HTML et sa feuille de style.

# Bloc, inline : le flux normal d'une page

Dans le bit sur le modèle de boîte, chaque élément est une boîte. Ce contenu regarde où le navigateur pose ces boîtes quand vous ne lui dites rien.

## Le flux normal : deux façons de ranger les boîtes

Le navigateur lit le HTML dans l'ordre et pose les boîtes l'une après l'autre. Chaque élément a une valeur de **`display`** par défaut, qui décide de sa façon de se ranger.

```scene
lesson: assets/flow.scene.json
step: flux
```

Un élément **bloc** (`display: block`) commence sur une nouvelle ligne et prend **toute la largeur** disponible, même si son contenu est court. Les blocs s'empilent donc **les uns sous les autres**.

Un élément **inline** (`display: inline`) se place **dans la ligne de texte**, à la suite de ce qui précède, et ne prend que la largeur de son contenu. Quand la ligne est pleine, il passe à la suivante, comme un mot.

| Bloc par défaut | Inline par défaut |
|---|---|
| `div`, `p`, `h1` à `h6`, `ul`, `li`, `header`, `nav`, `main`, `section`, `footer`, `form` | `span`, `a`, `strong`, `em`, `code`, `img`, `label` |

> 💡 **Remarque.** `img` est inline, mais le navigateur pose une image à sa place, avec une largeur et une hauteur propres : on dit un élément *remplacé*. La règle qui suit sur les marges ne le concerne pas.

## À toi : prédis où tombe chaque élément

Voici le haut d'une page de portfolio, sans aucun CSS. Avant de répondre, essaie de dessiner sur un papier ce que le navigateur affiche, puis réponds aux deux questions du plateau : chaque réponse dit pourquoi.

```html
<header>
  <p class="logo">CM</p>
  <h1>Camille Martin</h1>
  <p>Développeuse web à <strong>Toulouse</strong>, <a href="#projets">voir mes projets</a>.</p>
</header>
```

```quiz
title: "Où tombe chaque élément ?"
tracksProgress: false
showNotice: false
place: stage
questions:
  - prompt: "Sur combien de lignes, au minimum, s'affiche ce `header` dans une fenêtre large ?"
    answers:
      - "Une seule : tout se met à la suite"
      - "Trois : le logo, le titre, puis la phrase avec son lien"
      - "Cinq : une par balise"
    correct: 2
    explanation: "Les deux `p` et le `h1` sont des blocs, donc trois lignes. `strong` et `a` sont inline : ils restent dans la phrase."
  - prompt: "Quelle largeur prend le paragraphe `.logo`, qui ne contient que « CM » ?"
    answers:
      - "La largeur de « CM »"
      - "Toute la largeur de son parent, le `header`"
      - "Aucune, tant qu'on ne lui donne pas de `width`"
    correct: 2
    explanation: "Un bloc prend toute la largeur disponible, quelle que soit la longueur de son contenu. On le voit en lui donnant un fond de couleur."
```

## Ce que le navigateur affiche : trois blocs, trois lignes

Le même `header`, ligne par ligne : à gauche le code, à droite ce que le navigateur en fait, sans aucun CSS.

```scene
lesson: assets/flow.scene.json
step: reponse
```

Chaque **bloc** ouvre une ligne et prend toute la largeur, même `.logo` et ses deux lettres. Les deux **inline**, `strong` et `a`, ne créent pas de ligne : ils restent dans la phrase de leur paragraphe.

## Le piège : une marge verticale ignorée sur un inline

Un élément inline vit dans la ligne de texte. Le piège se voit sur un lien habillé en bouton :

```scene
lesson: assets/flow.scene.json
step: marge
```

Sa **marge à gauche et à droite** s'applique, mais sa **marge en haut et en bas ne déplace rien** : la hauteur de la ligne ne change pas pour lui. Son padding vertical se dessine, mais il déborde sur les lignes voisines au lieu de les repousser. Aucun message ne le signale.

## À toi : un bouton qui refuse sa marge

Le lien `.bouton` a une marge du haut de `24px`, et pourtant il colle au paragraphe du dessus, son fond le chevauche même. Regarde l'aperçu, puis fais-lui accepter sa marge en changeant sa valeur de `display` : le bit sur le modèle de boîte t'a montré celle qui garde un élément dans la ligne avec une vraie boîte.

```playground
runtime: web
title: Un bouton qui refuse sa marge
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
      <p>Je cherche une alternance à partir de septembre.</p>
      <a class="bouton" href="#contact">Me contacter</a>
      <p>Réponse sous 48 heures.</p>
    </body>
    </html>
  style.css: |
    body {
      font-family: system-ui, sans-serif;
    }

    .bouton {
      background-color: rgb(219, 39, 119);
      color: rgb(255, 255, 255);
      text-decoration: none;
      padding: 12px 20px;
      margin-top: 24px;
      /* Le lien est inline : sa marge du haut ne fait rien. */
    }
open: [style.css, index.html]
lock: [index.html]
verify:
  - label: le bouton n'est plus `inline` et accepte sa marge du haut
    selector: .bouton
    style: { display: "/^(inline-block|block)$/" }
    hint: "Ajoute `display: inline-block;` dans la règle `.bouton` : il reste dans la ligne, mais ses marges et son padding comptent."
solution: assets/bouton.solution
```

Avec `display: inline-block`, le bouton s'écarte du paragraphe : sa marge et son padding repoussent enfin les lignes voisines. Un `display: block` marcherait aussi, mais le bouton prendrait alors toute la largeur.

## inline-block : dans la ligne, avec une vraie boîte

**`inline-block`** combine les deux comportements : l'élément se place **dans la ligne** comme un inline, et il garde **une boîte complète** comme un bloc. Compare les trois valeurs sur la même phrase :

```scene
lesson: assets/flow.scene.json
step: display
```

La différence se voit à la **hauteur de la ligne** : un inline ne la change pas, sa marge passe sous la ligne voisine. Une boîte `inline-block` compte avec ses marges, et sa ligne s'agrandit pour lui faire de la place.

Une dernière valeur, `display: none`, retire l'élément de la page : il n'est plus affiché du tout.

## À toi : un menu sur une ligne

Le cas le plus courant est le menu. Les éléments `li` d'une liste sont des blocs : ils s'empilent, avec une puce chacun. Mets les quatre liens du menu côte à côte, sans puce et sans le retrait à gauche de la liste.

```playground
runtime: web
title: Un menu sur une ligne
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
      <header>
        <p class="logo">CM</p>
        <nav>
          <ul class="menu">
            <li><a href="#projets">Projets</a></li>
            <li><a href="#parcours">Parcours</a></li>
            <li><a href="#competences">Compétences</a></li>
            <li><a href="#contact">Contact</a></li>
          </ul>
        </nav>
      </header>
    </body>
    </html>
  style.css: |
    body {
      font-family: system-ui, sans-serif;
    }

    .logo {
      font-weight: bold;
    }

    /* Écris tes règles pour .menu et .menu li ici */
open: [style.css, index.html]
lock: [index.html]
verify:
  - label: les éléments `li` du menu sont côte à côte
    selector: .menu li
    style: { display: "/^inline/" }
    hint: "Les `li` sont des blocs : `.menu li { display: inline-block; }` les met dans la ligne."
  - label: la liste n'a plus de puces
    selector: .menu
    style: { list-style-type: none }
    hint: "`list-style: none;` se pose sur la liste, `.menu`."
  - label: la liste n'a plus de retrait à gauche
    selector: .menu
    style: { padding-left: 0px }
    hint: "Le retrait vient du padding par défaut de `ul` : `padding: 0;`."
solution: assets/menu.solution
```

Les liens sont sur une ligne. Un petit espace apparaît entre eux : c'est le retour à la ligne entre deux `li` dans le HTML, que le navigateur affiche comme un espace entre deux mots.

## Ce que le flux normal ne sait pas faire

Le menu est sur une ligne, mais le logo reste **au-dessus**. Compare avec ce qu'on veut obtenir :

```scene
lesson: assets/limites.scene.json
step: limites
```

`.logo` et `nav` sont deux blocs, donc deux lignes. Mettre le logo à gauche et le menu à droite, centrer en hauteur des éléments de tailles différentes, répartir l'espace entre eux : le flux normal ne le fait pas. Il faut un **mode de disposition**, Flexbox ou Grid.

> 💡 **Remarque.** Vous croiserez encore `float: left` dans du code ancien : il sort l'élément du flux et le colle à gauche, le texte qui suit l'entoure. Aujourd'hui, on le garde pour son usage d'origine, une image dans un article.

> 📖 [Le flux normal (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/CSS_layout/Introduction#le_flux_normal) · [La propriété display (MDN)](https://developer.mozilla.org/fr/docs/Web/CSS/display) · [Le modèle de boîte, bloc et inline (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Styling_basics/Box_model)

## Trois questions pour vérifier

```quiz
title: "Bloc, inline : le flux normal"
tracksProgress: false
showNotice: false
place: stage
questions:
  - prompt: "Vous mettez `margin-top: 30px` sur un `span`. Que se passe-t-il ?"
    answers:
      - "Le `span` descend de 30 px"
      - "Rien ne bouge : la marge verticale d'un inline ne déplace rien"
      - "Le navigateur affiche une erreur dans la console"
    correct: 2
    explanation: "Un inline vit dans la ligne de texte : ses marges du haut et du bas ne changent pas la hauteur de la ligne. Le CSS ne signale jamais ce genre de règle sans effet."
  - prompt: "Que fait `display: inline-block` ?"
    answers:
      - "Il place l'élément dans la ligne, et ses dimensions, marges et padding s'appliquent tous"
      - "Il place l'élément sur sa propre ligne, sur toute la largeur"
      - "Il cache l'élément"
    correct: 1
    explanation: "inline-block garde la place dans la ligne d'un inline et la boîte complète d'un bloc."
  - prompt: "Pourquoi un `li` s'affiche-t-il sous le précédent ?"
    answers:
      - "Parce qu'une liste est toujours verticale, aucune règle ne le change"
      - "Parce que `li` est un bloc par défaut : il commence sur une nouvelle ligne"
      - "Parce que le HTML contient un retour à la ligne entre deux `li`"
    correct: 2
    explanation: "Un `li` est un bloc (plus précisément `display: list-item`, avec sa puce). Changer son `display` le met dans la ligne."
```

## Récap

- Le **flux normal** range les boîtes sans aucune règle : les **blocs** les uns sous les autres, sur toute la largeur ; les **inline** dans la ligne, à la largeur de leur contenu.
- Sur un **inline**, `width`, `height` et les **marges verticales** ne font rien, sans aucun message d'erreur.
- **`inline-block`** met un élément dans la ligne en lui gardant une boîte complète.
- Le flux ne sait pas aligner deux blocs sur une ligne ni répartir l'espace entre eux : il faut un **mode de disposition**.

Pour mettre le logo à gauche et le menu à droite, sur la même ligne, il faut prendre la main sur ce rangement : c'est l'objet du bit [Flexbox](https://byte-layers.com/fr/bits/flexbox).

```ack
J'ai compris
```
