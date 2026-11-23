---
title: "Le web partout : sites, applications, mobile et bureau"
description: "Ce que l'on fait aujourd'hui avec HTML, CSS et JavaScript : des applications web riches et responsives, des PWA qu'on installe, des apps mobiles avec React Native, des logiciels de bureau avec Electron, et pourquoi ces langages sont devenus le standard de fait des interfaces."
tags:
  - bit
  - web
difficulty: beginner
duration: 15
requires: "0.9.0"
---

HTML, CSS et JavaScript ne servent plus seulement à faire des pages qu'on lit : ils font des applications complètes dans le navigateur, des applications qu'on installe, des apps mobiles et des logiciels de bureau. Vous saurez reconnaître ces quatre usages, ce que chacun ajoute au navigateur, et pourquoi ces trois langages sont devenus le standard de fait des interfaces graphiques.

**Prérequis** : [Une page web : HTML, CSS et JavaScript](https://byte-layers.com/fr/bits/web-page-languages), pour les trois langages et le moteur d'un navigateur.

# Le web partout : sites, applications, mobile et bureau

Une page web, c'est d'abord un titre, un bouton, un clic qui change un texte. Avec les mêmes langages, on construit aujourd'hui une messagerie, un tableur ou un éditeur de code. Ce contenu fait le tour de ce qu'ils permettent, du navigateur jusqu'au bureau.

## Des pages aux applications web

Un **site** se lit : des pages d'information, des liens de l'une à l'autre. Une **application web** se manipule : une messagerie comme Gmail, un traitement de texte comme Google Docs, un outil de dessin comme Figma. Elle tourne entièrement dans le navigateur, sans rien installer, et c'est le JavaScript qui la fait réagir à chaque clic, souvent sans recharger la page.

Voici la différence, clic après clic.

```scene
lesson: assets/everywhere.scene.json
step: appli
```

On parle de **client léger** : l'interface vit dans le navigateur, les données sur un serveur. Une nouvelle version se déploie une seule fois, sur le serveur, et chacun l'a à son prochain chargement.

## Une seule page pour tous les écrans : le responsive

La même application s'ouvre sur un écran d'ordinateur de 1 600 pixels de large et sur un téléphone de 360 pixels. Plutôt que d'écrire deux sites, on écrit une seule page dont la disposition s'adapte à la largeur de l'écran.

```scene
lesson: assets/cibles.scene.json
step: responsive
```

C'est le **responsive design** (*responsive* : qui réagit, qui s'adapte ; on dit aussi « design adaptatif »). Le HTML ne change pas : c'est la feuille de style qui range les blocs, avec des règles qui ne s'appliquent qu'à partir d'une certaine largeur, les *media queries* (requêtes sur le média, ici l'écran).

## Installer une PWA : le manifeste

Une **PWA** (*Progressive Web App*, application web progressive) est une application web qu'on peut installer depuis le navigateur. Pour cela, elle fournit un **manifeste** : un petit fichier, `manifest.json`, qui donne son nom, son icône, ses couleurs et sa façon de s'ouvrir. Regardez ce que le navigateur en fait.

```scene
lesson: assets/everywhere.scene.json
step: installer
```

L'application reçoit une icône sur l'écran d'accueil ou dans le menu des applications, et s'ouvre dans sa propre fenêtre. L'installation dépend du navigateur : Chrome et Edge la proposent sur ordinateur, Safari sur iPhone par le menu « Sur l'écran d'accueil ».

## Hors connexion : le service worker

Une PWA peut aussi marcher sans réseau. Elle installe pour cela un **service worker** (littéralement « travailleur de service ») : un fichier JavaScript qui tourne en arrière-plan, entre la page et le réseau. Voici comment il sert l'application quand le réseau manque.

```scene
lesson: assets/everywhere.scene.json
step: pwa
```

Le service worker garde des fichiers en réserve et les sert à la place du serveur. Une PWA reste pourtant une page web : elle n'a pas accès à tout ce qu'une application native peut faire.

## Le mobile : React Native

Une app mobile **native** (écrite pour le système lui-même) vise un seul système, iOS ou Android, avec ses langages : Swift pour l'un, Kotlin pour l'autre. **React Native** permet d'écrire une seule app en JavaScript pour les deux. **Capacitor** prend un autre chemin. Voici la différence à l'écran.

```scene
lesson: assets/cibles.scene.json
step: mobile
```

Avec React Native, l'écran n'est pas une page web : on écrit du JavaScript et des styles proches du CSS, mais l'app affiche les vrais boutons et les vraies listes du système. Capacitor, lui, glisse une vraie page HTML, CSS et JavaScript dans une app qu'on publie sur les boutiques d'applications (App Store, Google Play). Dans les deux cas, ce que vous apprenez sur le web resservira.

## Le bureau : Electron

**Electron** fabrique des logiciels de bureau pour Windows, macOS et Linux à partir d'une application web. Il emporte deux programmes avec chaque logiciel : **Chromium**, le navigateur libre sur lequel Chrome est construit, et **Node.js**, qui fait tourner du JavaScript hors du navigateur. Regardez ce qui se passe quand on ouvre un fichier.

```scene
lesson: assets/cibles.scene.json
step: electron
```

Chromium affiche l'interface ; Node.js lit et écrit les fichiers, ce qu'une page web n'a pas le droit de faire. Vous en utilisez sans doute : **VS Code** est une application Electron, tout comme Slack, Discord ou Obsidian. Le prix de cette facilité : chaque logiciel embarque son propre Chromium, et pèse donc plus lourd qu'un logiciel natif.

## Le standard de fait des interfaces

Le navigateur, la PWA, l'app mobile, le logiciel de bureau : une même équipe peut couvrir ces quatre cibles avec les mêmes langages.

```scene
lesson: assets/cibles.scene.json
step: cibles
```

Souvent, une bonne part du code est même partagée. Aucune loi ne l'impose, mais l'usage s'est installé : on parle de **standard de fait** (*de facto*, par opposition à une norme imposée). HTML, CSS et JavaScript sont devenus une façon courante de dessiner une interface graphique, du navigateur au bureau, et c'est la raison de les comprendre vraiment, plutôt que de les laisser écrire à votre place sans savoir les relire.

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

- Une **application web** tourne entièrement dans le navigateur : un client léger, déployé une seule fois sur le serveur.
- Le **responsive design** adapte une seule page à toutes les largeurs d'écran : la feuille de style range les blocs selon la largeur.
- Une **PWA** est une application web qu'on installe, grâce à un **manifeste** et à un **service worker**, qui la fait marcher hors connexion.
- **React Native** écrit des apps mobiles en JavaScript avec les composants natifs ; **Capacitor** emballe une vraie page web dans une app.
- **Electron** fait des logiciels de bureau avec Chromium et Node.js : VS Code, Slack, Discord.
- HTML, CSS et JavaScript sont devenus le **standard de fait** des interfaces graphiques.

Toutes ces interfaces commencent par le même premier pas : une page HTML bien construite. C'est l'objet du contenu [Le squelette d'une page HTML, son texte, ses liens et ses images](https://byte-layers.com/fr/bits/html-document).

```ack
J'ai compris
```
