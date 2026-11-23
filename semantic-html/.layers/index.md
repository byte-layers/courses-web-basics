---
title: "Le HTML sémantique : le sens avant la forme"
description: "Pourquoi une page faite de div ne dit rien au navigateur, à un lecteur d'écran ou à un moteur de recherche ; les balises qui nomment les zones (header, nav, main, article, section, aside, footer) ; quand div reste le bon choix ; des titres qui forment un plan, pas une taille."
tags:
  - bit
  - web
  - html
  - accessibility
difficulty: beginner
duration: 15
requires: "0.9.0"
---

Une balise HTML ne dit pas seulement où placer un contenu : elle dit **ce qu'il est**. Vous saurez pourquoi une page faite de `<div>` ne dit rien à ceux qui la lisent sans la voir, ranger les blocs d'une page dans les balises qui les nomment (`header`, `nav`, `main`, `article`, `section`, `aside`, `footer`), reconnaître le cas où `<div>` reste le bon choix, et écrire des titres qui forment le plan de la page plutôt qu'une taille de texte.

**Prérequis** : [Le squelette d'une page HTML, son texte, ses liens et ses images](https://byte-layers.com/fr/bits/html-document), pour les balises, les titres et les listes.

# Le HTML sémantique : le sens avant la forme

Vous savez déjà dire ce qu'est un texte : un titre, un paragraphe, une liste. Ce contenu monte d'un étage : il nomme les grandes zones d'une page, puis il range ses titres en un plan. Le fil : le site d'un club de randonnée, *Les Marcheurs du Dimanche*.

## Une page faite de `div` : ce que le navigateur ne sait pas

L'élément `<div>` (*division*) est une boîte sans signification : il groupe des éléments, et c'est tout. Son cousin `<span>` fait de même à l'intérieur d'une ligne de texte. On peut construire une page entière avec des `<div>`, et elle s'affiche très bien. Mais tous les lecteurs d'une page ne la regardent pas :

| Lecteur | Ce qu'il cherche, et ce qu'il trouve dans une page de `<div>` |
|---|---|
| un **lecteur d'écran**, qui lit la page à voix haute à une personne aveugle | les zones, pour sauter directement au menu ou au contenu. Avec des `<div>` : aucune zone, il faut tout écouter depuis le début |
| un **moteur de recherche** | le contenu principal, à distinguer du menu et du pied de page. Avec des `<div>` : il doit deviner |
| le **mode lecture** d'un navigateur | l'article seul, sans le menu ni les publicités. Avec des `<div>` : il le devine, parfois mal |

Voici l'accueil du club, fait de `<div>`, puis rangé dans des balises qui disent ce qu'est chaque bloc.

```scene
lesson: assets/semantic.scene.json
step: zones
```

Le **HTML sémantique**, c'est choisir la balise qui dit ce qu'est un bloc. Le navigateur en tire un plan de la page, l'**arbre d'accessibilité**, que lisent les lecteurs d'écran.

## Les balises qui nomment les zones

Sept balises disent ce qu'est un bloc. Elles ne changent rien à l'apparence : un `<header>` s'affiche exactement comme un `<div>`. Regarde la page d'un récit du club se ranger, zone par zone.

```scene
lesson: assets/semantic.scene.json
step: balises
```

Ce qu'annonce un lecteur d'écran porte un nom anglais, traduit entre parenthèses :

| Balise | Ce qu'elle contient, et la zone annoncée |
|---|---|
| `<header>` (*en-tête*) | le nom du site, souvent le menu. Annoncé *banner* (bannière) quand c'est l'en-tête de la page |
| `<nav>` | un groupe de liens pour naviguer, le menu. Annoncé *navigation* |
| `<main>` (*principal*) | le contenu principal, **un seul** par page. Annoncé *main* |
| `<article>` | un contenu complet : un billet, une fiche produit, un commentaire. Annoncé *article* |
| `<section>` | une partie, avec son titre. Annoncé *region* (région) quand on lui donne un nom |
| `<aside>` (*à côté*) | un encadré en marge du sujet, des liens connexes. Annoncé *complementary* (complémentaire) |
| `<footer>` (*pied de page*) | le contact, les mentions. Annoncé *contentinfo* (informations sur le contenu) quand c'est le pied de la page |

## Article ou section, et la place de `div`

`<article>` ou `<section>` ? Un test suffit : celui de la **publication**. Copie le bloc, seul, dans un e-mail.

```scene
lesson: assets/semantic.scene.json
step: article
```

Le bloc garde tout son sens : c'est un `<article>`. Il ne se comprend plus sans le reste : c'est une `<section>` d'un ensemble plus grand. Et `<div>` garde sa place : un groupe qui ne sert qu'à la **mise en page**, sans intention de sens, reste un `<div>`. En faire une `<section>` annoncerait une partie qui n'existe pas.

## À toi : range les blocs de la page

La page ci-dessous est l'accueil du club, construit entièrement en `<div>`. Remplace chaque `<div>` par la balise qui dit ce qu'est sa zone, sans oublier la balise fermante. Un seul `<div>` doit rester : celui qui groupe les deux récits pour la mise en page.

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

L'aperçu n'a pas bougé d'un pixel pendant l'exercice : c'est tout l'enjeu. Ce que vous avez changé ne se voit pas, il s'entend. Les outils de développement du navigateur montrent le plan qu'il en tire.

## Les titres : un plan, pas une taille

Les titres `<h1>` à `<h6>` (*heading*, titre de niveau 1 à 6) forment le **plan** de la page, comme la table des matières d'un livre : un seul `<h1>`, le sujet ; des `<h2>` pour ses parties ; des `<h3>` pour les sous-parties d'un `<h2>`, sans sauter de niveau. Les lecteurs d'écran proposent de naviguer de titre en titre.

Le piège : choisir un titre pour sa **taille**, `<h1>` pour un texte qu'on veut gros, `<h4>` pour un sous-titre qu'on veut discret. La taille se règle en CSS, sur n'importe quel élément ; la balise dit le **niveau**.

Voici le plan de l'accueil du club quand ses titres sont choisis à l'œil, puis remis à leur niveau.

```scene
lesson: assets/semantic.scene.json
step: plan
```

Un lecteur d'écran annonce le niveau de chaque titre : un deuxième `<h1>` y fait croire à un deuxième sujet, un `<h4>` sous un `<h1>` à des parties qui manquent.

## À toi : des titres qui forment un plan

L'accueil du club est maintenant rangé en zones, mais ses titres ont été choisis à l'œil : « Nos derniers récits » en `<h1>` parce qu'il paraissait plus visible, les deux récits en `<h4>` parce qu'ils paraissaient plus discrets. Remets ces titres à leur place dans le plan.

```playground
runtime: web
title: Des titres qui forment un plan
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Les Marcheurs du Dimanche</title>
    </head>
    <body>
      <header>
        <h1>Les Marcheurs du Dimanche</h1>
        <p>Le blog d'un club de randonnée</p>
      </header>

      <main>
        <h1>Nos derniers récits</h1>
        <article>
          <h4>Le pic du Midi par la face nord</h4>
          <p>Départ à 6 h du parking. La montée est raide, mais le panorama récompense l'effort.</p>
        </article>
        <article>
          <h4>Boucle des trois lacs</h4>
          <p>Une sortie familiale de 12 km, accessible aux enfants à partir de huit ans.</p>
        </article>
      </main>
    </body>
    </html>
verify:
  - label: un seul `<h1>`, le sujet de la page, « Les Marcheurs du Dimanche »
    selector: h1
    count: 1
    text: Les Marcheurs du Dimanche
  - label: « Nos derniers récits » est un `<h2>`, une partie de la page
    selector: h2
    count: 1
    text: Nos derniers récits
    hint: "« Nos derniers récits » est une grande partie, juste sous le sujet"
  - label: chaque récit est un `<h3>`, une sous-partie des récits
    selector: article h3
    count: 2
    hint: "Un récit est rangé dans « Nos derniers récits » : un cran plus bas qu'un `<h2>`"
  - label: aucun niveau n'est sauté, il ne reste ni `<h4>`, ni `<h5>`, ni `<h6>`
    selector: h4, h5, h6
    exists: false
solution: assets/titres.solution
```

L'aperçu change cette fois : les titres rapetissent ou grandissent. C'est le style par défaut du navigateur, que le CSS remplacera. Ce qui compte, c'est le plan.

## Le tout : une page avec deux erreurs

Voici la page des prochaines sorties du club. Elle a deux défauts qui ne se voient pas à l'écran : une zone qui ne dit pas ce qu'elle est, et des titres choisis pour leur taille. Corrige `index.html`.

```playground
runtime: web
title: Trouve les deux erreurs
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Nos sorties · Les Marcheurs du Dimanche</title>
    </head>
    <body>
      <header>
        <h1>Les Marcheurs du Dimanche</h1>
        <div>
          <ul>
            <li><a href="#">Accueil</a></li>
            <li><a href="#">Nos sorties</a></li>
            <li><a href="#">Nous rejoindre</a></li>
          </ul>
        </div>
      </header>

      <main>
        <h2>Nos prochaines sorties</h2>
        <article>
          <h4>Le lac d'Oô</h4>
          <p>Dimanche 7 juin, départ à 8 h : 10 km et 600 m de dénivelé.</p>
        </article>
        <article>
          <h4>Le cirque de Gavarnie</h4>
          <p>Dimanche 14 juin, départ à 7 h : 14 km et 800 m de dénivelé.</p>
        </article>
      </main>

      <footer>
        <p>© 2026 Les Marcheurs du Dimanche</p>
      </footer>
    </body>
    </html>
verify:
  - label: le menu est dans un `<nav>`
    selector: nav a
    count: 3
    hint: "Un groupe de liens pour naviguer dans le site, c'est une zone qui a son nom"
  - label: il ne reste aucun `<div>`
    selector: div
    exists: false
  - label: chaque sortie a un titre `<h3>`, un cran sous « Nos prochaines sorties »
    selector: article h3
    count: 2
    hint: "Sous un `<h2>`, le niveau suivant est `<h3>` : pas de saut jusqu'au `<h4>`"
  - label: aucun niveau n'est sauté, il ne reste ni `<h4>`, ni `<h5>`, ni `<h6>`
    selector: h4, h5, h6
    exists: false
solution: assets/tout.solution
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
- **Article ou section** : un bloc qui garde son sens copié seul ailleurs est un `<article>` ; sinon, c'est une `<section>`.
- `<div>` reste le bon choix pour un groupe qui ne sert qu'à la mise en page.
- Les **titres** forment un plan : un seul `<h1>`, des `<h2>`, puis des `<h3>`, sans sauter de niveau ; la taille se règle en CSS.

La page a du sens. Reste à lui donner une apparence, avec un deuxième langage qui vise ces balises : c'est l'objet du contenu [CSS : règles, sélecteurs et cascade](https://byte-layers.com/fr/bits/css-rules-cascade).

```ack
J'ai compris
```
