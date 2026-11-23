---
title: "Les standards du web et les moteurs des navigateurs"
description: "Qui écrit les standards du HTML, du CSS et de JavaScript (WHATWG, W3C, Ecma), ce que font le moteur de rendu et le moteur JavaScript d'un navigateur, et pourquoi une même page s'est longtemps affichée différemment d'un navigateur à l'autre : balises maison, mode quirks, Interop."
tags:
  - bit
  - web
difficulty: beginner
duration: 10
requires: "0.8.0"
---

Chrome, Firefox et Safari affichent la même page à peu près de la même façon, et ce n'est pas un hasard. Vous saurez qui écrit les **standards** du HTML, du CSS et de JavaScript, ce que font les deux **moteurs** d'un navigateur, et pourquoi une même page s'est longtemps affichée différemment selon le navigateur.

**Prérequis** : [Une page web : HTML, CSS et JavaScript](https://byte-layers.com/fr/bits/web-page-languages), pour les trois langages d'une page et leurs rôles.

# Les standards du web et les moteurs des navigateurs

Une page est écrite en HTML, en CSS et en JavaScript, et des navigateurs très différents savent tous la lire. Ce contenu regarde qui décide de ce que ces langages veulent dire, et qui l'applique.

## Des standards : WHATWG, W3C et Ecma

Si tous les navigateurs savent lire ces trois langages, c'est parce qu'ils sont décrits par des **standards** : des textes publics qui disent ce que chaque balise, chaque propriété, chaque instruction doit faire.

```scene
lesson: assets/standards.scene.json
step: standards
```

Personne ne possède le web : chaque standard est écrit par un organisme où se retrouvent les éditeurs de navigateurs. Le **WHATWG** tient le standard du HTML, le **W3C** ceux du CSS, **Ecma International** celui de JavaScript, qui s'appelle **ECMAScript**. Clique sur un bloc du schéma pour en savoir plus.

## Le navigateur et ses moteurs

Un navigateur contient deux programmes qui font le gros du travail. Le **moteur de rendu** lit le HTML et le CSS et dessine la page ; le **moteur JavaScript** exécute les scripts.

```scene
lesson: assets/moteurs.scene.json
step: moteurs
```

Ce sont eux qui appliquent les standards, et il n'en existe plus que trois familles :

| Navigateurs | Moteur de rendu | Moteur JavaScript |
|---|---|---|
| Chrome, Edge, Opera, Brave | Blink | V8 (le même que dans Node.js) |
| Firefox | Gecko | SpiderMonkey |
| Safari | WebKit | JavaScriptCore |

Sur iPhone et iPad, Apple a longtemps imposé **WebKit** à tous les navigateurs : Chrome pour iPhone dessine donc les pages avec le moteur de Safari. Depuis 2024, l'Union européenne a obtenu que d'autres moteurs y soient autorisés.

## Pourquoi une page s'affichait différemment selon le navigateur

Les standards n'ont pas toujours été suivis. À la fin des années 1990, Netscape Navigator et Internet Explorer se disputaient le marché, et chacun ajoutait ses **propres balises** : `<blink>` faisait clignoter un texte dans Netscape, `<marquee>` le faisait défiler dans Internet Explorer.

```scene
lesson: assets/histoire.scene.json
step: histoire
```

Une même page s'affichait donc différemment, et beaucoup de sites affichaient « optimisé pour Internet Explorer ». Les navigateurs ont convergé sans casser les vieilles pages : c'est la **rétrocompatibilité**. Sans la ligne `<!DOCTYPE html>`, une page passe en **mode quirks** (« bizarreries »), qui imite les anciens navigateurs ; c'est pourquoi cette ligne ouvre toute page.

Aujourd'hui, les écarts portent surtout sur les fonctions récentes, que le projet **Interop** réduit chaque année depuis 2022. Avant d'en utiliser une, *Can I use* dit quels navigateurs la connaissent.

> 📖 [Le HTML Living Standard (WHATWG, en anglais)](https://html.spec.whatwg.org/) · [ECMA-262 (Ecma International, en anglais)](https://tc39.es/ecma262/) · [Modes quirks et standard (MDN)](https://developer.mozilla.org/fr/docs/Web/HTML/Guides/Quirks_mode_and_standards_mode) · [Can I use (en anglais)](https://caniuse.com/)

## Trois questions pour vérifier ce que vous avez retenu

```quiz
title: "Standards et moteurs"
tracksProgress: false
showNotice: false
place: stage
questions:
  - prompt: "Qui écrit le standard du HTML que suivent aujourd'hui les navigateurs ?"
    answers:
      - "Chaque navigateur écrit le sien"
      - "Le WHATWG, et le W3C le reconnaît comme le seul standard HTML depuis 2019"
      - "Ecma International, avec ECMAScript"
    correct: 2
    explanation: "Le HTML Living Standard est tenu par le WHATWG. Ecma International publie ECMAScript, le standard de JavaScript, et le W3C les modules CSS."
  - prompt: "Dans un navigateur, quel programme dessine la page à partir du HTML et du CSS ?"
    answers:
      - "Le moteur de rendu, par exemple Blink, Gecko ou WebKit"
      - "Le moteur JavaScript, par exemple V8"
      - "Le serveur web, avant d'envoyer la page"
    correct: 1
    explanation: "Le moteur de rendu lit le HTML et le CSS et dessine la page ; le moteur JavaScript exécute les scripts. Le serveur envoie du texte, c'est le navigateur qui dessine."
  - prompt: "Pourquoi une page commence-t-elle par `<!DOCTYPE html>` ?"
    answers:
      - "Pour que le serveur sache qu'il doit envoyer du HTML"
      - "Pour charger le moteur JavaScript"
      - "Pour que le navigateur applique les standards actuels au lieu d'imiter les anciens navigateurs (le mode quirks)"
    correct: 3
    explanation: "Sans doctype, le navigateur passe en mode quirks, qui reproduit les bizarreries des anciens navigateurs pour ne pas casser les vieilles pages. Avec, il suit les standards."
```

## Récap

- Des **standards** publics décrivent les langages du web : le HTML Living Standard du WHATWG, les modules CSS du W3C, ECMAScript d'Ecma International.
- Chaque navigateur a un **moteur de rendu** et un **moteur JavaScript** : Blink et V8, Gecko et SpiderMonkey, WebKit et JavaScriptCore.
- Les navigateurs ont longtemps divergé, avec leurs balises maison ; la **rétrocompatibilité** garde les vieilles pages lisibles, d'où le **mode quirks** sans doctype.
- Les écarts qui restent portent sur les fonctions récentes : **Interop** les réduit chaque année, *Can I use* les liste.

Ces langages et ces moteurs ne servent plus seulement à afficher des pages : on en fait des applications, des apps mobiles et des logiciels de bureau. C'est l'objet du contenu [Le web partout](https://byte-layers.com/fr/bits/web-everywhere).

```ack
J'ai compris
```
