---
title: "Le web partout : sites, applications, mobile et bureau"
description: "Ce que l'on fait aujourd'hui avec HTML, CSS et JavaScript : des applications web riches et responsives, des PWA qu'on installe, des apps mobiles avec React Native, des logiciels de bureau avec Electron, et pourquoi ces langages sont devenus le standard de fait des interfaces."
tags:
  - bit
  - web
difficulty: beginner
duration: 10
requires: "0.8.0"
---

HTML, CSS et JavaScript ne servent plus seulement à faire des pages qu'on lit : ils font des applications complètes dans le navigateur, des applications qu'on installe, des apps mobiles et des logiciels de bureau. Vous saurez reconnaître ces quatre usages, ce que chacun ajoute au navigateur, et pourquoi ces trois langages sont devenus le standard de fait des interfaces graphiques.

**Prérequis** : [Une page web : HTML, CSS et JavaScript](https://byte-layers.com/fr/bits/web-page-languages), pour les trois langages et le moteur d'un navigateur.

# Le web partout : sites, applications, mobile et bureau

Le contenu précédent décrivait une page : un titre, un bouton, un clic qui change un texte. Avec les mêmes langages, on construit aujourd'hui une messagerie, un tableur ou un éditeur de code. Ce contenu fait le tour de ce qu'ils permettent, du navigateur jusqu'au bureau.

## Des pages aux applications web

Un **site** se lit : des pages d'information, des liens de l'une à l'autre. Une **application web** se manipule : une messagerie comme Gmail, un traitement de texte comme Google Docs, un outil de dessin comme Figma. Elle tourne entièrement dans le navigateur, sans rien installer, et c'est le JavaScript qui la fait réagir à chaque clic, souvent sans recharger la page.

C'est le client léger du contenu sur les architectures : l'interface vit dans le navigateur, les données sur un serveur. Une nouvelle version se déploie une seule fois, sur le serveur, et chacun l'a à son prochain chargement.

## Une seule page pour tous les écrans : le responsive

La même application s'ouvre sur un écran de bureau de 1 600 pixels de large et sur un téléphone de 360 pixels. Plutôt que d'écrire deux sites, on écrit une seule page dont la disposition s'adapte à la largeur de l'écran : c'est le **responsive design** (on dit aussi « adaptatif »). Sur un ordinateur, trois colonnes côte à côte ; sur un téléphone, les mêmes blocs les uns sous les autres. Tout se fait en CSS, et le cours qui suit celui-ci y consacre une étape.

## Les PWA : une application web qu'on installe

Une **PWA** (*Progressive Web App*) est une application web qu'on peut installer depuis le navigateur. Elle reçoit une icône sur l'écran d'accueil ou dans le menu des applications, s'ouvre dans sa propre fenêtre, sans barre d'adresse, et peut fonctionner hors connexion. Deux fichiers de plus suffisent pour cela :

| Fichier | Ce qu'il apporte |
|---|---|
| le **manifeste** (`manifest.json`) | le nom de l'application, son icône, ses couleurs : ce dont le système a besoin pour l'installer |
| le **service worker** (un fichier JavaScript) | un script qui tourne en arrière-plan, garde des fichiers en réserve et sert la page sans réseau |

L'installation dépend du navigateur : Chrome et Edge la proposent sur ordinateur, Safari sur iPhone par le menu « Sur l'écran d'accueil ». Une PWA reste une page web : elle n'a pas accès à tout ce qu'une application native peut faire.

## Le mobile : React Native

Une app mobile **native** est écrite pour un système précis, iOS ou Android, avec ses langages : Swift pour l'un, Kotlin pour l'autre. **React Native** permet d'écrire une seule app en JavaScript pour les deux. Attention : l'écran n'y est pas une page web. On écrit du JavaScript et des styles proches du CSS, mais React Native affiche les composants du système, les vrais boutons et les vraies listes d'iOS ou d'Android.

D'autres outils, comme **Capacitor**, font l'inverse : ils glissent une vraie page HTML, CSS et JavaScript dans une app qu'on publie sur les stores. Dans les deux cas, ce que vous apprenez sur le web resservira.

## Le bureau : Electron

**Electron** fabrique des logiciels de bureau pour Windows, macOS et Linux à partir d'une application web. Il emporte deux programmes avec chaque logiciel : **Chromium**, la partie libre de Chrome, qui affiche l'interface écrite en HTML, CSS et JavaScript, et **Node.js**, qui donne accès aux fichiers et au système, ce qu'une page web n'a pas le droit de faire.

Vous en utilisez sans doute : **VS Code**, l'éditeur de ce parcours, est une application Electron, tout comme Slack, Discord ou Obsidian. Le prix de cette facilité : chaque logiciel embarque son propre Chromium, et pèse donc plus lourd qu'un logiciel natif.

```fill
text: "Electron réunit deux programmes : _____, pour afficher l'interface, et _____, pour accéder aux fichiers et au système."
blanks:
  - answers: [Chromium, Chrome]
    hint: La partie libre d'un navigateur bien connu.
  - answers: [Node.js, Node, NodeJS]
    hint: Le runtime JavaScript qui tourne hors du navigateur, vu dans l'introduction.
```

## Le standard de fait des interfaces

Le navigateur, la PWA, l'app mobile, le logiciel de bureau : une même équipe peut couvrir ces quatre cibles avec les mêmes langages, et souvent une bonne part du même code. Aucune loi ne l'impose, mais l'usage s'est installé : on parle de **standard de fait**. HTML, CSS et JavaScript sont devenus une façon courante de dessiner une interface graphique, du navigateur au bureau, et c'est la raison de les comprendre vraiment, plutôt que de les laisser écrire à votre place sans savoir les relire.

> 📖 [Les applications web progressives (MDN)](https://developer.mozilla.org/fr/docs/Web/Progressive_web_apps) · [Le responsive design (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/CSS_layout/Responsive_Design) · [Electron (en anglais)](https://www.electronjs.org/) · [React Native (en anglais)](https://reactnative.dev/) · [Capacitor (en anglais)](https://capacitorjs.com/)

## Quatre questions pour vérifier ce que vous avez retenu

```quiz
title: "Web, PWA, mobile ou bureau ?"
tracksProgress: false
showNotice: false
place: stage
questions:
  - prompt: "VS Code s'installe sur votre ordinateur et s'ouvre dans sa propre fenêtre, mais son interface est écrite en HTML, CSS et JavaScript. Sur quoi repose-t-il ?"
    answers:
      - "Electron : Chromium pour l'interface, Node.js pour le système"
      - "React Native"
      - "C'est une PWA installée depuis Chrome"
    correct: 1
    explanation: "VS Code est une application Electron : elle embarque Chromium pour afficher son interface et Node.js pour lire et écrire vos fichiers."
  - prompt: "Depuis le navigateur, vous cliquez sur « Installer » : l'application reçoit une icône, s'ouvre sans barre d'adresse et marche dans le train sans réseau. Qu'est-ce que c'est ?"
    answers:
      - "Une application native, écrite en Swift ou en Kotlin"
      - "Une PWA : une application web avec un manifeste et un service worker"
      - "Un logiciel Electron"
    correct: 2
    explanation: "Une PWA s'installe depuis le navigateur grâce à son manifeste, et son service worker lui permet de fonctionner hors connexion."
  - prompt: "Une app mobile est écrite en JavaScript avec React Native. Qu'est-ce qui s'affiche à l'écran ?"
    answers:
      - "Une page HTML, dans un navigateur caché"
      - "Une image de la page, envoyée par un serveur"
      - "Les composants natifs du système, les vrais boutons et listes d'iOS ou d'Android"
    correct: 3
    explanation: "React Native s'écrit en JavaScript, mais il affiche les composants du système, pas une page web. C'est Capacitor qui, au contraire, glisse une vraie page dans une app."
  - prompt: "Une même page s'affiche en trois colonnes sur un ordinateur et en une seule sur un téléphone. Comment s'appelle cette façon de faire ?"
    answers:
      - "Le responsive design : une seule page, dont la disposition s'adapte à la largeur de l'écran"
      - "Une PWA"
      - "Deux sites différents, un par écran"
    correct: 1
    explanation: "Le responsive design adapte la disposition d'une même page à la largeur de l'écran, en CSS."
```

## Récap

- Une **application web** tourne entièrement dans le navigateur : le client léger, déployé une seule fois sur le serveur.
- Le **responsive design** adapte une seule page à toutes les largeurs d'écran, en CSS.
- Une **PWA** est une application web qu'on installe, grâce à un **manifeste** et à un **service worker**, qui la fait marcher hors connexion.
- **React Native** écrit des apps mobiles en JavaScript avec les composants natifs ; **Capacitor** emballe une vraie page web dans une app.
- **Electron** fait des logiciels de bureau avec Chromium et Node.js : VS Code, Slack, Discord.
- HTML, CSS et JavaScript sont devenus le **standard de fait** des interfaces graphiques.

Toutes ces interfaces commencent par le même premier pas : une page HTML bien construite. C'est l'objet du contenu [Le squelette d'une page HTML, son texte, ses liens et ses images](https://byte-layers.com/fr/bits/html-document).

```ack
J'ai compris
```
