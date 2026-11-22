---
title: "L'accessibilité web : une page lisible par tous"
description: "Une page accessible se lit sans souris, sans les yeux, avec un zoom à 200 % : les erreurs les plus fréquentes (alt absent, contraste trop faible, langue absente, titres sautés, focus invisible), les critères RGAA qui les détectent, et les outils pour les trouver, Lighthouse et la grille d'audit."
tags:
  - bit
  - html
  - css
  - accessibility
difficulty: beginner
duration: 15
requires: "0.9.0"
---

Une page **accessible** se lit et s'utilise par tout le monde : au clavier, sans souris ; à l'oreille, avec un **lecteur d'écran** ; avec une vue faible et un zoom à 200 %. Vous saurez reconnaître les cinq erreurs les plus fréquentes, les relier aux critères du **RGAA**, le référentiel français, et les trouver avec des outils.

**Prérequis** : le bit [Tableaux et formulaires HTML](https://byte-layers.com/fr/bits/html-tables-forms), pour les étiquettes reliées, et le bit [Le sens avant la forme](https://byte-layers.com/fr/bits/semantic-html), pour les balises sémantiques.

# L'accessibilité web : une page lisible par tous

Une page peut être belle sur votre écran et inutilisable pour une partie de ses visiteurs. Ce contenu montre ce qui la rend inutilisable, comment le corriger, et comment le vérifier.

## Qui lit votre page autrement

Une personne aveugle écoute la page avec un **lecteur d'écran** (NVDA ou JAWS sous Windows, VoiceOver sous macOS et iOS, TalkBack sous Android) : il lit le texte, annonce les titres, les liens, les champs et leurs étiquettes, et décrit les images par leur texte alternatif. Une personne qui ne peut pas tenir une souris navigue **au clavier** : Tab pour passer d'un lien ou d'un champ au suivant, Entrée pour l'activer. Une personne malvoyante **agrandit** le texte et a besoin de contrastes francs.

Le **WCAG** (*Web Content Accessibility Guidelines*) est la norme internationale du W3C. En France, le **RGAA** (Référentiel général d'amélioration de l'accessibilité) la traduit en 106 critères à vérifier, chacun formulé comme une question. Il est obligatoire pour les services publics, et l'Acte européen sur l'accessibilité étend depuis juin 2025 des obligations à une partie des services privés, comme le commerce en ligne.

## Cinq erreurs fréquentes, et le critère RGAA qui les détecte

La plupart des défauts d'une page débutante tiennent en quelques erreurs, qui se corrigent en une ligne chacune.

| Erreur | Ce que ça donne | Critère RGAA | Correction |
|---|---|---|---|
| Une image sans `alt` | le lecteur d'écran lit le nom du fichier, `IMG_2043.jpg` | 1.1 | `alt="Le sommet du pic du Midi"` ; `alt=""` pour une image décorative |
| Un texte gris clair sur blanc | illisible avec une vue faible, ou au soleil | 3.2 | un contraste d'au moins **4,5:1** pour le texte courant |
| Pas de `lang` sur `html` | le lecteur d'écran lit le français avec un accent anglais | 8.3 | `<html lang="fr">` |
| Un niveau de titre sauté, `h1` puis `h4` | la liste des titres, qu'on parcourt au lecteur d'écran, a des trous | 9.1 | `h1`, puis `h2`, puis `h3`, sans sauter de niveau |
| `outline: none` sur le focus | au clavier, on ne sait plus où l'on est | 10.7 | garder le contour, ou le remplacer par un style visible |

Le **contraste** est le rapport de luminosité entre le texte et son fond : `1:1` pour du blanc sur blanc, `21:1` pour du noir sur blanc. Les outils de développement l'affichent : inspectez un texte, cliquez sur le petit carré de couleur de sa propriété `color`, et le sélecteur de couleur indique le rapport.

Le **focus** est l'élément qui reçoit les touches du clavier. Le navigateur l'entoure d'un contour, l'`outline`. Une règle `outline: none`, souvent ajoutée parce que le contour « fait moche » au clic, le supprime pour tout le monde. Si vous voulez le changer, utilisez **`:focus-visible`**, qui ne s'applique qu'à la navigation au clavier :

```css
a:focus-visible {
  outline: 3px solid rgb(219, 39, 119);
  outline-offset: 2px;
}
```

## Trouve les cinq erreurs

**À toi** : cette page de portfolio contient les cinq erreurs du tableau. Corrige-les dans `index.html` et `style.css`, puis clique sur **Vérifier**. Avant de corriger le focus, essaie : clique dans l'aperçu, puis appuie sur Tab pour passer d'un lien à l'autre.

```playground
runtime: web
title: Trouve les cinq erreurs
files:
  index.html: |
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Camille Martin, développeuse web</title>
      <link rel="stylesheet" href="style.css">
    </head>
    <body>
      <header>
        <h1>Camille Martin</h1>
        <nav>
          <a href="#projets">Projets</a>
          <a href="#contact">Contact</a>
        </nav>
      </header>
      <main>
        <section id="projets">
          <h4>Mes projets</h4>
          <img src="rando.svg">
          <p>Le site du club de randonnée, mon projet de fin de formation.</p>
          <p class="note">Site réalisé en HTML et CSS, sans framework.</p>
        </section>
        <section id="contact">
          <h4>Me contacter</h4>
          <p><a href="mailto:camille@exemple.fr">camille@exemple.fr</a></p>
        </section>
      </main>
    </body>
    </html>
  style.css: |
    body {
      font-family: system-ui, sans-serif;
      background-color: rgb(255, 255, 255);
      color: rgb(30, 41, 59);
    }

    nav a {
      margin-right: 12px;
    }

    a:focus {
      outline: none;
    }

    .note {
      color: rgb(170, 170, 170);
      font-size: 14px;
    }
  rando.svg: |
    <svg xmlns="http://www.w3.org/2000/svg" width="320" height="160" viewBox="0 0 320 160">
      <rect width="320" height="160" fill="#dcfce7"/>
      <polygon points="0,160 120,40 200,120 250,80 320,160" fill="#166534"/>
    </svg>
open: [index.html, style.css]
check: ask
verify:
  - label: la langue de la page est déclarée en français
    selector: html
    attr: { lang: "/^fr/" }
    hint: "Critère 8.3 : `<html lang=\"fr\">`."
  - label: l'image a un texte alternatif qui la décrit
    selector: img
    attr: { alt: "/\\S/" }
    hint: "Critère 1.1 : l'image montre un sommet du site du club ; décris-la dans `alt=\"…\"`."
  - label: le texte `.note` est assez contrasté sur le fond blanc
    selector: .note
    style: { color: "/^rgb\\((\\d{1,2}|10\\d|11[0-8]), (\\d{1,2}|10\\d|11[0-8]), (\\d{1,2}|10\\d|11[0-8])\\)$/" }
    hint: "Critère 3.2 : `rgb(170, 170, 170)` donne 2,3:1. Un gris au moins aussi foncé que `rgb(118, 118, 118)` dépasse 4,5:1."
  - label: les deux sections ont un titre `h2`, sans niveau sauté
    selector: "main > section > h2"
    count: 2
    hint: "Critère 9.1 : après le `h1`, le niveau suivant est `h2`, pas `h4`."
  - label: le focus clavier reste visible, aucun `outline` supprimé
    file: style.css
    excludes: "/outline\\s*:\\s*(none|0)/"
    hint: "Critère 10.7 : supprime la règle `a:focus { outline: none; }`, ou remplace-la par un contour visible avec `:focus-visible`."
solution: assets/erreurs.solution
```

> 💡 **Remarque.** Le contrôle du contraste accepte les couleurs dont chacune des trois composantes vaut au plus `118` : elles dépassent toutes 4,5:1 sur blanc. C'est une règle simple pour l'exercice, pas la seule façon d'y arriver : un bleu foncé comme `rgb(30, 64, 175)` est très bien contrasté, mais le contrôle le refusera. Dans une vraie page, mesurez le rapport avec les outils de développement.

## Vérifier : Lighthouse, puis la grille et le clavier

Un outil automatique trouve une partie des erreurs. **Lighthouse**, intégré à Chrome et à Edge (outils de développement, onglet *Lighthouse*, catégorie *Accessibility*), analyse la page et donne un score sur 100, avec la liste des défauts : `alt` manquants, contrastes, `lang`, champs sans étiquette. Il ne sait pas juger si un `alt` est **pertinent**, si l'ordre des titres a du **sens**, ni si la page se parcourt **au clavier** sans piège.

Le reste se vérifie à la main, avec une grille comme celle du RGAA, et trois gestes simples :

| Geste | Ce qu'il révèle |
|---|---|
| Parcourir toute la page avec Tab, sans souris | le focus visible, l'ordre de passage, les éléments impossibles à atteindre |
| Zoomer à 200 % (Ctrl et +, ou Cmd et +) | le texte qui se coupe ou se superpose |
| Afficher la liste des titres (outils de développement, onglet *Accessibilité*, ou une extension) | les niveaux sautés, les sections sans titre |

Un score de 100 dans Lighthouse ne veut donc pas dire que la page est accessible : il veut dire qu'aucune des erreurs que l'outil sait détecter n'a été trouvée.

> 📖 [L'accessibilité, introduction (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Accessibility/What_is_accessibility) · [Le RGAA 4.1, critères et tests (DINUM)](https://accessibilite.numerique.gouv.fr/methode/criteres-et-tests/) · [Comprendre le contraste des couleurs (MDN)](https://developer.mozilla.org/fr/docs/Web/Accessibility/Guides/Understanding_WCAG/Perceivable/Color_contrast) · [Lighthouse accessibility audits (Chrome, en anglais)](https://developer.chrome.com/docs/lighthouse/accessibility/scoring)

## Trois questions pour vérifier

```quiz
title: "L'accessibilité web"
tracksProgress: false
showNotice: false
place: stage
questions:
  - prompt: "Quel `alt` donner à une image purement décorative, un trait de séparation par exemple ?"
    answers:
      - "Aucun attribut `alt`"
      - "`alt=\"\"` : vide, pour que le lecteur d'écran l'ignore"
      - "`alt=\"image\"`"
    correct: 2
    explanation: "Sans alt, le lecteur d'écran lit le nom du fichier. Un alt vide lui dit d'ignorer l'image (critère 1.2)."
  - prompt: "Pourquoi `outline: none` sur `a:focus` pose-t-il problème ?"
    answers:
      - "Parce que le lien n'est plus cliquable"
      - "Parce qu'au clavier, on ne voit plus quel élément a le focus"
      - "Parce que le lien change de couleur"
    correct: 2
    explanation: "Le contour du focus est le seul repère de qui navigue au clavier. :focus-visible permet de le changer sans le supprimer."
  - prompt: "Lighthouse donne 100 en accessibilité. Qu'en concluez-vous ?"
    answers:
      - "La page est conforme au RGAA"
      - "Aucune des erreurs que l'outil sait détecter n'a été trouvée ; le reste se vérifie à la main"
      - "La page n'a plus besoin d'être testée au clavier"
    correct: 2
    explanation: "Un outil automatique ne juge ni la pertinence d'un alt ni la navigation au clavier : la grille et les tests manuels restent nécessaires."
```

## Récap

- Une page **accessible** s'utilise au **clavier**, avec un **lecteur d'écran** et avec un **zoom** ; le **RGAA** traduit la norme WCAG en critères à vérifier.
- Cinq erreurs fréquentes : image sans **`alt`**, **contraste** sous 4,5:1, pas de **`lang`**, **titres** sautés, **focus** supprimé par `outline: none`.
- **Lighthouse** trouve une partie des erreurs ; la grille, Tab, le zoom à 200 % et la liste des titres trouvent le reste.

Une page cohérente garde aussi ses choix de couleurs au même endroit, et elle bouge sans gêner ceux que le mouvement dérange : c'est l'objet du bit [Variables CSS et mouvement](https://byte-layers.com/fr/bits/css-variables-motion).

```ack
J'ai compris
```
