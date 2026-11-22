---
title: "Les bases de JavaScript, sur votre machine"
description: "Lab débutant en huit étapes, dans ~/byte-layers/web/js : la console du navigateur et ses boîtes de dialogue, un script branché sur une page, le jeu de devinette avec ses conditions puis sa boucle, des fonctions, des objets et une classe, une liste construite avec le DOM, un bouton et un formulaire qui réagissent, un tableau rempli depuis un fichier JSON avec fetch."
tags:
  - lab
  - javascript
  - dom
  - web
difficulty: beginner
duration: 150
introTitle: "Présentation"
requires: "0.4.0"
options:
  allowManualProgress: true
  autoCompleteOnNext: unverifiable
---

Les bits du cours vous ont fait rencontrer chaque notion dans un exercice court, en ligne. Ce lab les reprend une à une **sur votre machine** : la vraie console du navigateur, des fichiers que vous créez dans VS Code, des pages que vous ouvrez vous-même. Certains pièges n'existent que là : un fichier pas enregistré, un nom mal écrit dans `src`, une page ouverte sans serveur, une boucle qui fige l'onglet.

## Pour qui ?

**Niveau** : débutant en JavaScript. Le lab suppose :

- le lab [Votre poste de développeur](https://byte-layers.com/fr/labs/dev-setup-lab) : VS Code installé, son terminal intégré, et Node.js ;
- les huit bits du cours, de [La console JavaScript](https://byte-layers.com/fr/bits/js-console) à [Données JSON et fetch](https://byte-layers.com/fr/bits/json-fetch) : chaque étape du lab renvoie au bit qu'elle met en pratique ;
- savoir écrire une page HTML simple et la lier à une feuille de style.

Il ne suppose aucune autre expérience de la programmation.

## Comment ça se passe

Huit étapes, une par bit du cours, environ 2 h 30 en tout. Chaque étape se termine par une vérification. Les premières étapes vous donnent presque tout le code ; les dernières vous donnent un objectif et des critères, et le code est à vous.

| Étape | Ce que vous faites | Fichiers créés |
|---|---|---|
| 01 | parler au navigateur dans sa console, créer le dossier du lab | le dossier `~/byte-layers/web/js` |
| 02 | brancher un script sur une page, et le placer au bon endroit | `index.html`, `script.js` |
| 03 | le jeu de devinette, en un essai | `devinette.html`, `devinette.js` |
| 04 | la devinette qui redemande, et la liste des essais | `devinette.js`, modifié |
| 05 | des fonctions, des objets et une classe, lancés avec Node.js | `formes.js` |
| 06 | une liste de livres construite avec le DOM | `catalogue.html`, `catalogue.js` |
| 07 | une lampe qui s'allume au clic, un formulaire qui ne recharge pas | `lampe.html`, `lampe.js`, `contact.html`, `contact.js` |
| 08 | un tableau rempli depuis un fichier JSON | `registre.html`, `emprunts.json`, `registre.js` |

Tous vos fichiers vivent dans **`~/byte-layers/web/js`**, et le lab ne supprime rien : effacez le dossier quand vous n'en avez plus besoin.

Vous travaillez avec deux fenêtres : **VS Code**, ouvert sur ce dossier, pour écrire ; un **navigateur** (Chrome, Firefox, Edge ou Safari), pour ouvrir les pages et leur console. L'extension **Live Preview** de VS Code, éditée par Microsoft, est conseillée pour l'étape 08 : l'étape dit comment l'installer, et propose une autre solution.

**Sous Windows**, les commandes se tapent dans **Git Bash**, comme au lab « Votre poste de développeur ».

> 💡 **Remarque.** Les boutons de vérification fonctionnent quand ce contenu est ouvert dans VS Code avec l'extension byte_layers, disponible pour macOS et Linux : la page [Comment ça marche](https://byte-layers.com/fr/comment-ca-marche) explique comment l'installer. Ils relisent vos fichiers, et pour les étapes 03 à 05, ils exécutent votre code avec Node.js. Sinon, comparez votre résultat à celui décrit à chaque étape.
