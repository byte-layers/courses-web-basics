---
title: "Les bases HTML et CSS, sur votre machine"
description: "Lab débutant : lire les requêtes d'une page dans l'onglet Réseau, retirer le CSS puis le JavaScript d'une page, écrire un squelette HTML, une fiche avec liens et image, ranger une page en balises sémantiques, l'habiller en CSS avec ses propres classes, et déjouer le piège de la largeur."
tags:
  - lab
  - web
  - html
  - css
difficulty: beginner
duration: 100
introTitle: "Présentation"
requires: "0.4.0"
options:
  allowManualProgress: true
  autoCompleteOnNext: unverifiable
---

Les bits de ce cours ont fait jouer chaque notion dans un aperçu, dans la page. Ce lab la refait sur votre machine, avec **VS Code** pour écrire et un **navigateur** pour voir : de vrais fichiers, enregistrés sur votre disque, et les outils de développement du navigateur. Certains pièges n'existent que là : un fichier pas enregistré, une page ouverte depuis le disque, des majuscules que votre système ignore et qu'un serveur n'ignorera pas.

## Pour qui ?

**Niveau** : débutant. Vous n'avez jamais écrit de page web à la main.

**Ce qu'il faut savoir** : ce qu'enseignent les sept bits du cours, de [Le web : une adresse, une requête, une page](https://byte-layers.com/fr/bits/web-request-response) à [Le modèle de boîte](https://byte-layers.com/fr/bits/box-model). Chaque étape du lab rappelle le bit qu'elle reprend.

**Ce qu'il faut avoir** :

- VS Code, installé au lab [Votre poste de développeur](https://byte-layers.com/fr/labs/dev-setup-lab), où vous avez appris à ouvrir un dossier, créer un fichier et l'enregistrer ;
- un navigateur de bureau à jour : **Chrome**, **Edge** ou **Firefox**. Les deux premières étapes donnent le chemin des menus pour Chrome et Edge, qui ont les mêmes outils, et pour Firefox quand il diffère. Safari convient pour tout le reste, mais ses outils de développement sont cachés par défaut.

## Comment ça se passe

Sept étapes, une par notion du cours, environ 1 h 40 en tout. Les deux premières observent des pages qui existent déjà ; les cinq suivantes vous font écrire du HTML et du CSS, avec de moins en moins de guidage.

Tous vos fichiers vivent dans un seul dossier, `~/byte-layers/web/basics`, que la première étape crée. Chaque étape y ajoute un ou deux fichiers, et le lab ne supprime rien : à la fin, supprimez le dossier si vous n'en avez plus besoin.

La **boucle de travail** est la même à chaque étape, et elle tient en quatre gestes : écrire dans VS Code, **enregistrer** (Cmd+S sous macOS, Ctrl+S ailleurs), passer au navigateur et **recharger** la page (Cmd+R ou Ctrl+R, ou F5), regarder ce qui a changé. Si rien ne change, c'est presque toujours l'enregistrement qui manque : un rond plein sur l'onglet de VS Code signale un fichier modifié et pas encore enregistré.

**Sous Windows**, les commandes se tapent dans **Git Bash**, installé dans l'introduction. Tapez ou collez chaque commande vous-même : le bouton ▶ ne fonctionne que dans l'extension.

> 💡 **Remarque.** Les boutons de vérification fonctionnent quand ce contenu est ouvert dans VS Code avec l'extension byte_layers, disponible pour macOS et Linux : la page [Comment ça marche](https://byte-layers.com/fr/comment-ca-marche) explique comment l'installer. Ils lisent vos fichiers sur le disque. Sinon, comparez votre résultat à ce que décrit chaque étape.
