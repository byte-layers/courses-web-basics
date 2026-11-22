---
title: "Le HTML sémantique : le sens avant la forme"
description: "Pourquoi une page faite de div ne dit rien au navigateur, à un lecteur d'écran ou à un moteur de recherche ; les balises qui nomment les zones (header, nav, main, article, section, aside, footer) ; quand div reste le bon choix ; des titres qui forment un plan, pas une taille."
tags:
  - bit
  - web
  - html
  - accessibility
difficulty: beginner
duration: 12
requires: "0.9.0"
---

Une balise HTML ne dit pas seulement où placer un contenu : elle dit **ce qu'il est**. Vous saurez pourquoi une page faite de `<div>` ne dit rien à ceux qui la lisent sans la voir, ranger les blocs d'une page dans les balises qui les nomment (`header`, `nav`, `main`, `article`, `section`, `aside`, `footer`), reconnaître le cas où `<div>` reste le bon choix, et écrire des titres qui forment le plan de la page plutôt qu'une taille de texte.

**Prérequis** : [Le squelette d'une page HTML, son texte, ses liens et ses images](https://byte-layers.com/fr/bits/html-document), pour les balises, les titres et les listes.

# Le HTML sémantique : le sens avant la forme

Dans le contenu précédent, chaque balise disait déjà ce qu'était son texte : un titre, un paragraphe, une liste. Ce contenu monte d'un étage : il nomme les grandes zones de la page, et il range les titres en un plan.

## Une page faite de `div` : ce que le navigateur ne sait pas

L'élément `<div>` est une boîte sans signification : il groupe des éléments, et c'est tout. Son cousin `<span>` fait de même à l'intérieur d'une ligne de texte. On peut construire une page entière avec des `<div>`, et elle s'affiche très bien. Mais tous les lecteurs d'une page ne la regardent pas :

| Lecteur | Ce qu'il fait de la page | Avec des `<div>` partout |
|---|---|---|
| un **lecteur d'écran**, qui lit la page à voix haute à une personne aveugle | annonce les zones et permet de sauter directement au menu ou au contenu principal | aucune zone à annoncer : il faut tout écouter, du début |
| un **moteur de recherche** | cherche le contenu principal et le distingue du menu et du pied de page | tout a le même poids |
| le **mode lecture** d'un navigateur | ne garde que l'article, sans le menu ni les publicités | il ne trouve pas l'article |

Le **HTML sémantique**, c'est choisir la balise qui dit ce qu'est un bloc. Le navigateur en tire un plan de la page, l'**arbre d'accessibilité**, que lisent les lecteurs d'écran.

## Les balises qui nomment les zones

Ces balises ne changent rien à l'apparence : un `<header>` s'affiche exactement comme un `<div>`. Elles ajoutent du sens.

| Balise | Ce qu'elle contient | Zone annoncée par un lecteur d'écran |
|---|---|---|
| `<header>` | l'en-tête : le nom du site, souvent le menu | *banner* (bannière), pour l'en-tête de la page |
| `<nav>` | un groupe de liens de navigation, le menu | *navigation* |
| `<main>` | le contenu principal ; **un seul** par page | *main* |
| `<article>` | un contenu qui garde son sens publié seul ailleurs : un billet, une fiche produit, un commentaire | *article* |
| `<section>` | une partie thématique, avec son titre | *region*, quand elle a un nom |
| `<aside>` | un contenu à côté du sujet : un encadré, des liens connexes | *complementary* |
| `<footer>` | le pied de page : contact, mentions | *contentinfo*, pour le pied de la page |

Pour choisir entre `<article>` et `<section>`, faites le test de la publication : si ce bloc, copié seul dans un e-mail ou un flux d'actualités, garde tout son sens, c'est un `<article>`. Sinon, c'est une `<section>` d'un ensemble plus grand.

Et `<div>` garde sa place : quand un groupe ne sert qu'à la **mise en page**, sans intention de sens, `<div>` est le bon choix. Le transformer en `<section>` annoncerait une partie qui n'existe pas.

La page ci-dessous est le blog d'un club de randonnée, construit entièrement en `<div>`. Remplace chaque `<div>` par la balise qui dit ce qu'est sa zone, sans oublier la balise fermante. Un seul `<div>` doit rester : celui qui groupe les deux récits pour la mise en page.

```playground
runtime: web
title: Range les blocs de la page
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Les Marcheurs du Dimanche</title>
    </head>
    <body>
      <div>
        <h1>Les Marcheurs du Dimanche</h1>
        <p>Le blog d'un club de randonnée</p>
        <div>
          <ul>
            <li><a href="#">Accueil</a></li>
            <li><a href="#">Nos sorties</a></li>
            <li><a href="#">Nous rejoindre</a></li>
          </ul>
        </div>
      </div>

      <div>
        <h2>Nos derniers récits</h2>
        <div>
          <div>
            <h3>Le pic du Midi par la face nord</h3>
            <p>Départ à 6 h du parking. La montée est raide, mais le panorama récompense l'effort.</p>
          </div>
          <div>
            <h3>Boucle des trois lacs</h3>
            <p>Une sortie familiale de 12 km, accessible aux enfants à partir de huit ans.</p>
          </div>
        </div>

        <div>
          <h3>Le saviez-vous ?</h3>
          <p>Le club organise une sortie chaque dimanche depuis 1987.</p>
        </div>
      </div>

      <div>
        <p>© 2026 Les Marcheurs du Dimanche</p>
      </div>
    </body>
    </html>
verify:
  - label: le nom du club est dans un `<header>`
    selector: header h1
    count: 1
  - label: le menu est dans un `<nav>`
    selector: nav a
    count: 3
  - label: le contenu principal est dans un seul `<main>`
    selector: main
    count: 1
    hint: "`<main>` entoure le titre « Nos derniers récits », les deux récits et l'encadré"
  - label: chaque récit est dans un `<article>`
    selector: article h3
    count: 2
    hint: "Un récit garde son sens publié seul : c'est un `<article>`"
  - label: l'encadré « Le saviez-vous ? » est dans un `<aside>`
    selector: aside
    count: 1
  - label: le pied de page est dans un `<footer>`
    selector: footer
    count: 1
  - label: il reste exactement un `<div>`, celui qui groupe les deux récits
    selector: div
    count: 1
    hint: "Le `<div>` qui entoure les deux récits ne sert qu'à la mise en page : garde-le tel quel"
solution: assets/zones.solution
```

L'aperçu n'a pas bougé d'un pixel pendant l'exercice : c'est tout l'enjeu. Ce que vous avez changé ne se voit pas, il s'entend. Le lab de ce cours vous montre le plan que le navigateur en tire, dans ses outils de développement.

## Les titres : un plan, pas une taille

Les titres `<h1>` à `<h6>` forment le **plan** de la page, comme la table des matières d'un livre : un seul `<h1>`, le sujet de la page ; des `<h2>` pour ses grandes parties ; des `<h3>` pour les sous-parties d'un `<h2>`, et ainsi de suite, sans sauter de niveau. Les lecteurs d'écran proposent de naviguer de titre en titre : c'est souvent la première chose que fait une personne aveugle sur une page.

Le piège : choisir un titre pour sa **taille**. Le navigateur affiche `<h1>` en très grand et `<h4>` en petit, et il est tentant de prendre `<h1>` pour un texte qu'on veut gros, ou `<h4>` pour un sous-titre qu'on veut discret. La taille se règle en CSS, sur n'importe quel élément : c'est l'objet du contenu suivant. La balise, elle, dit le niveau dans le plan.

La recette ci-dessous a été écrite en choisissant les titres à l'œil : « Ingrédients » en `<h1>` parce qu'il paraissait plus visible, « Préparation » en `<h4>` parce qu'il paraissait plus discret. Remets ces deux titres à leur place dans le plan.

```playground
runtime: web
title: Des titres qui forment un plan
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Tarte aux pommes</title>
    </head>
    <body>
      <h1>Tarte aux pommes</h1>
      <p>Une recette pour six personnes, prête en une heure.</p>

      <h1>Ingrédients</h1>
      <ul>
        <li>Une pâte brisée</li>
        <li>Quatre pommes</li>
        <li>Trente grammes de sucre</li>
      </ul>

      <h4>Préparation</h4>
      <ol>
        <li>Étalez la pâte dans le moule.</li>
        <li>Coupez les pommes en fines lamelles et posez-les sur la pâte.</li>
        <li>Saupoudrez de sucre et faites cuire 35 minutes à 180 °C.</li>
      </ol>
    </body>
    </html>
verify:
  - label: un seul `<h1>`, le sujet de la page, « Tarte aux pommes »
    selector: h1
    count: 1
    text: Tarte aux pommes
  - label: les deux grandes parties sont des `<h2>`
    selector: h2
    count: 2
    hint: "« Ingrédients » et « Préparation » sont deux parties de même niveau, juste sous le sujet"
  - label: aucun niveau n'est sauté, il ne reste ni `<h3>` ni `<h4>`
    selector: h3, h4, h5, h6
    exists: false
solution: assets/titres.solution
```

> 📖 [Les balises sémantiques et la structure d'une page (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Structuring_content/Structuring_documents) · [HTML : une bonne base pour l'accessibilité (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Accessibility/HTML) · [L'élément div (MDN)](https://developer.mozilla.org/fr/docs/Web/HTML/Reference/Elements/div)

## Trois questions pour vérifier ce que vous avez retenu

```quiz
title: "Le sens avant la forme"
tracksProgress: false
showNotice: false
place: stage
questions:
  - prompt: "Vous remplacez tous les `<div>` d'une page par `<header>`, `<nav>`, `<main>` et `<footer>`. Que change-t-il à l'écran ?"
    answers:
      - "Rien : ces balises ajoutent du sens, pas de l'apparence"
      - "Le menu passe à l'horizontale"
      - "Le pied de page se colle en bas de la fenêtre"
    correct: 1
    explanation: "Les balises sémantiques s'affichent comme des `<div>`. Elles changent ce que comprennent le navigateur, les lecteurs d'écran et les moteurs de recherche."
  - prompt: "Un blog affiche trois billets, chacun avec son titre et son texte. Quelle balise pour chaque billet ?"
    answers:
      - "`<section>`, parce que c'est une partie de la page"
      - "`<article>`, parce qu'un billet garde son sens publié seul ailleurs"
      - "`<aside>`, parce qu'il est à côté du menu"
    correct: 2
    explanation: "Le test de la publication : copié seul dans un e-mail ou un flux, un billet garde son sens. C'est un `<article>`."
  - prompt: "Vous voulez un sous-titre en très gros caractères. Que faites-vous ?"
    answers:
      - "Un `<h1>`, puisque c'est le plus grand"
      - "Un `<h6>` dans un `<strong>`"
      - "La balise de son niveau dans le plan, `<h2>` par exemple, et la taille en CSS"
    correct: 3
    explanation: "La balise dit le niveau dans le plan de la page ; la taille se règle en CSS. Un deuxième `<h1>` brouille le plan que suivent les lecteurs d'écran."
```

## Récap

- `<div>` et `<span>` groupent sans rien dire ; une page faite de `<div>` n'offre aucun repère aux **lecteurs d'écran**, aux moteurs de recherche et au mode lecture.
- Les balises **sémantiques** nomment les zones : `<header>`, `<nav>`, `<main>` (un seul), `<article>`, `<section>`, `<aside>`, `<footer>`. Elles ne changent pas l'apparence.
- **Article ou section** : un bloc qui garde son sens publié seul est un `<article>`.
- `<div>` reste le bon choix pour un groupe qui ne sert qu'à la mise en page.
- Les **titres** forment un plan : un seul `<h1>`, des `<h2>`, puis des `<h3>`, sans sauter de niveau ; la taille se règle en CSS.

La page a du sens. Reste à lui donner une apparence, avec un deuxième langage qui vise ces balises : c'est l'objet du contenu [CSS : règles, sélecteurs et cascade](https://byte-layers.com/fr/bits/css-rules-cascade).

```ack
J'ai compris
```
