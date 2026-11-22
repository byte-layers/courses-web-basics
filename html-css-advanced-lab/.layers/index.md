---
title: "HTML et CSS avancé, sur votre machine"
description: "Lab débutant en neuf étapes, dans un seul dossier : l'entête d'un portfolio dans le flux normal, puis en Flexbox avec une galerie, la grille de projets en Grid, un formulaire de contact sans JavaScript, la page rendue adaptative, un audit d'accessibilité avec Lighthouse et une grille RGAA allégée, un thème en variables avec des transitions, un bloc refait avec Bootstrap, et Tailwind installé et lancé pour de vrai."
tags:
  - lab
  - html
  - css
difficulty: beginner
duration: 240
introTitle: "Présentation"
requires: "0.4.0"
options:
  allowManualProgress: true
  autoCompleteOnNext: unverifiable
---

Vous construisez, étape par étape, la page d'accueil d'un portfolio de développeuse : un entête, une galerie, une grille de projets, un formulaire de contact. Chaque étape reprend une notion du cours « HTML et CSS avancé » et la pratique **sur votre machine**, dans VS Code et un vrai navigateur, là où se cachent des pièges que les exercices en ligne ne montrent pas : un fichier pas enregistré, un chemin d'image faux, une page ouverte sur un téléphone. La dernière étape installe **Tailwind** et lance son traitement.

## Pour qui ?

**Niveau** : débutant. Ce lab suppose le cours « Les bases HTML CSS » (le squelette d'une page, les balises sémantiques, les sélecteurs, le modèle de boîte) et les bits du cours « HTML et CSS avancé », qu'il pratique dans cet ordre :

1. [Bloc, inline : le flux normal d'une page](https://byte-layers.com/fr/bits/normal-flow)
2. [Flexbox](https://byte-layers.com/fr/bits/flexbox)
3. [CSS Grid](https://byte-layers.com/fr/bits/css-grid)
4. [Tableaux et formulaires HTML](https://byte-layers.com/fr/bits/html-tables-forms)
5. [Le responsive design](https://byte-layers.com/fr/bits/responsive-design)
6. [L'accessibilité web](https://byte-layers.com/fr/bits/web-accessibility)
7. [Variables CSS et mouvement](https://byte-layers.com/fr/bits/css-variables-motion)
8. [Bootstrap : des classes CSS toutes faites](https://byte-layers.com/fr/bits/css-frameworks)
9. [Tailwind, et pourquoi le CSS se compile](https://byte-layers.com/fr/bits/css-build-tools)

Vous pouvez faire chaque étape juste après son bit, ou tout le lab à la fin du cours.

**Ce qu'il faut** : VS Code et Node.js, installés par le lab [Votre poste de développeur](https://byte-layers.com/fr/labs/dev-setup-lab), et un navigateur récent (Chrome, Edge ou Firefox ; l'étape 6 utilise Lighthouse, intégré à Chrome et à Edge). L'extension **Live Preview** de VS Code recharge la page à chaque enregistrement : elle est pratique, pas obligatoire.

## Comment ça se passe

Neuf étapes, environ quatre heures en tout ; chacune tient en 20 à 30 minutes. Toutes travaillent dans **un seul dossier**, `~/byte-layers/web/advanced`, sur deux fichiers qui grandissent d'étape en étape, `index.html` et `style.css`. L'étape 8 y ajoute `bootstrap.html`, l'étape 9 un sous-dossier `tailwind`. Rien n'est supprimé à la fin : le dossier vous sert de modèle pour le challenge du portfolio.

La façon de travailler ne change pas depuis le cours précédent : **j'écris, j'enregistre, je recharge**. Le navigateur lit le fichier enregistré sur le disque, pas ce qui est affiché dans l'éditeur : un rond plein sur l'onglet de VS Code veut dire que le fichier n'est pas encore enregistré.

**Sous Windows**, les commandes se tapent dans **Git Bash**, ouvert dans le terminal intégré de VS Code.

> 💡 **Remarque.** Les boutons de vérification fonctionnent quand ce contenu est ouvert dans VS Code avec l'extension byte_layers, disponible pour macOS et Linux : la page [Comment ça marche](https://byte-layers.com/fr/comment-ca-marche) explique comment l'installer. Sinon, comparez votre page à ce que décrit chaque étape.
