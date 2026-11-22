---
title: "Une page web : HTML, CSS et JavaScript"
description: "Les trois langages d'une page et leurs rôles, comment une page relie sa feuille de style et son script, les standards (WHATWG, W3C, Ecma) et les moteurs des navigateurs, et pourquoi une même page s'est longtemps affichée différemment d'un navigateur à l'autre."
tags:
  - bit
  - web
  - html
  - css
difficulty: beginner
duration: 15
requires: "0.9.0"
---

Le texte qu'un navigateur reçoit pour afficher une page est écrit dans trois langages : **HTML** pour le contenu, **CSS** pour l'apparence, **JavaScript** pour le comportement. Vous saurez reconnaître chacun, relier une page à sa feuille de style et à son script, qui écrit les standards de ces langages, ce que sont les moteurs d'un navigateur, et pourquoi une même page s'est longtemps affichée différemment selon le navigateur.

**Prérequis** : [Le web : une adresse, une requête, une page](https://byte-layers.com/fr/bits/web-request-response), pour la requête, la réponse et les fichiers qu'une page demande.

# Une page web : HTML, CSS et JavaScript

Dans le contenu précédent, le navigateur recevait le texte d'une page, y trouvait l'adresse d'une feuille de style, puis la demandait au serveur. Ce contenu regarde ce que contiennent ces fichiers, et qui décide de la façon de les écrire.

## Trois langages, trois rôles

Une page web se partage entre trois langages, et chacun répond à une seule question :

| Langage | Fichier habituel | La question à laquelle il répond | Exemple |
|---|---|---|---|
| **HTML** (*HyperText Markup Language*) | `index.html` | qu'est-ce que la page contient ? | un titre, un paragraphe, un bouton |
| **CSS** (*Cascading Style Sheets*) | `style.css` | à quoi ça ressemble ? | le bouton est rose, le texte fait 20 pixels |
| **JavaScript** | `script.js` | que se passe-t-il quand on agit ? | un clic sur le bouton change le titre |

Voici les trois fichiers d'une toute petite page. Le HTML décrit le contenu, et c'est lui qui cite les deux autres fichiers :

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Trois langages</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <h1 id="titre">Bonjour !</h1>
  <button type="button" id="bouton">Clique-moi</button>
  <script src="script.js"></script>
</body>
</html>
```

La feuille de style dit à quoi ressemble le bouton :

```css
#bouton {
  background-color: rgb(219, 39, 119);
  color: white;
}
```

Le script, lui, attend un clic sur le bouton, puis remplace le texte du titre :

```javascript
document.querySelector('#bouton').addEventListener('click', function () {
  document.querySelector('#titre').textContent = 'Merci !';
});
```

Vous n'avez pas à comprendre chaque ligne : la suite du cours détaille le HTML et le CSS, et le JavaScript a son propre cours. Ce qui compte ici, c'est la séparation. Sans le CSS, la page garde tout son contenu, avec l'apparence par défaut du navigateur. Sans le JavaScript, elle s'affiche normalement, mais le clic ne fait plus rien.

## Relier la feuille de style et le script : `<link>` et `<script>`

Le HTML cite les deux autres fichiers par deux balises, et chacune a sa forme exacte :

| Pour relier | On écrit | Où |
|---|---|---|
| une feuille de style | `<link rel="stylesheet" href="style.css">` | dans le `<head>` |
| un script | `<script src="script.js"></script>` | ici, juste avant `</body>` |

Le nom du fichier doit être écrit **exactement** : `Script.js` et `script.js` sont deux fichiers différents pour un serveur. Et si la balise est fausse ou le nom mal écrit, la page ne vous prévient pas : elle s'affiche sans le style, ou sans le comportement, en silence.

La page ci-dessous a été écrite par quelqu'un qui s'est trompé deux fois. Le bouton devrait être rose, et un clic devrait changer le titre en « Merci ! ». Ni l'un ni l'autre ne marche. `style.css` et `script.js` sont justes et en lecture seule : corrige `index.html`.

```playground
runtime: web
title: Relie la feuille de style et le script
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Trois langages</title>
      <style src="style.css"></style>
    </head>
    <body>
      <h1 id="titre">Bonjour !</h1>
      <p class="texte">Cette page parle trois langages.</p>
      <button type="button" id="bouton">Clique-moi</button>
      <script src="Script.js"></script>
    </body>
    </html>
  style.css: |
    #bouton {
      background-color: rgb(219, 39, 119);
      color: white;
      border: none;
      padding: 8px 16px;
    }

    .texte {
      font-size: 20px;
    }
  script.js: |
    document.querySelector('#bouton').addEventListener('click', function () {
      document.querySelector('#titre').textContent = 'Merci !';
    });
open: [index.html, style.css, script.js]
lock: [style.css, script.js]
show: [editor, preview, console]
verify:
  - label: le bouton est rose, la feuille de style est donc chargée
    selector: "#bouton"
    style: { background-color: "rgb(219, 39, 119)" }
    hint: "`<style>` n'a pas d'attribut `src` : une feuille de style se relie par `<link rel=\"stylesheet\" href=\"style.css\">`"
  - label: le texte du paragraphe fait 20 px
    selector: .texte
    style: { font-size: 20px }
  - label: un clic sur le bouton change le titre en « Merci ! »
    click: "#bouton"
    selector: "#titre"
    text: Merci !
    hint: "Compare lettre par lettre le nom écrit dans `<script src=…>` et le nom de l'onglet du fichier : la casse compte"
solution: assets/relier.solution
```

Les deux fautes de cette page sont classiques. `<style>` sert à écrire du CSS directement dans la page, entre ses balises ; il ne sait pas charger un fichier, et un attribut qu'il ne connaît pas est simplement ignoré. Le `S` majuscule de `Script.js` désigne un fichier qui n'existe pas. Dans les deux cas, rien ne s'affiche à l'écran pour vous le dire : il faut savoir où regarder.

## Des standards : WHATWG, W3C et Ecma

Si tous les navigateurs savent lire ces trois langages, c'est parce qu'ils sont décrits par des **standards** : des documents publics qui disent ce que chaque balise, chaque propriété, chaque instruction doit faire. Personne ne possède le web ; ces textes sont écrits par des organismes où se retrouvent les éditeurs de navigateurs et d'autres membres.

| Langage | Standard | Écrit par |
|---|---|---|
| HTML | le *HTML Living Standard*, mis à jour en continu | le **WHATWG**, un groupe fondé par des éditeurs de navigateurs ; depuis 2019, le W3C le reconnaît comme le seul standard HTML |
| CSS | une série de **modules** (couleurs, boîtes, polices…), chacun avec sa version | le groupe de travail CSS du **W3C** (*World Wide Web Consortium*) |
| JavaScript | **ECMAScript** (le texte s'appelle ECMA-262), une nouvelle édition chaque année depuis 2015 | le comité TC39 d'**Ecma International** |

```fill
text: "Le standard du langage JavaScript s'appelle _____, et celui du HTML est tenu par le _____."
blanks:
  - answers: [ECMAScript, ECMA-262, ECMA Script]
    hint: Il porte le nom de l'organisme qui le publie, Ecma International.
  - answers: [WHATWG]
    hint: Un sigle de six lettres, pour Web Hypertext Application Technology Working Group.
```

## Le navigateur et ses moteurs

Un navigateur contient deux programmes qui font le gros du travail. Le **moteur de rendu** lit le HTML et le CSS et dessine la page ; le **moteur JavaScript** exécute les scripts. Ce sont eux qui appliquent les standards, et il n'en existe plus que trois familles :

| Navigateurs | Moteur de rendu | Moteur JavaScript |
|---|---|---|
| Chrome, Edge, Opera, Brave | Blink | V8 (le même que dans Node.js) |
| Firefox | Gecko | SpiderMonkey |
| Safari | WebKit | JavaScriptCore |

Sur iPhone et iPad, Apple a longtemps imposé WebKit à tous les navigateurs : Chrome pour iPhone dessine donc les pages avec le moteur de Safari. Depuis 2024, l'Union européenne a obtenu que d'autres moteurs y soient autorisés.

## Pourquoi une page s'affichait différemment selon le navigateur

Les standards n'ont pas toujours été suivis. À la fin des années 1990, Netscape Navigator et Internet Explorer se disputaient le marché, et chacun ajoutait ses propres balises pour attirer les créateurs de sites : `<blink>` faisait clignoter un texte dans Netscape, `<marquee>` le faisait défiler dans Internet Explorer. Les navigateurs appliquaient aussi les standards à leur rythme, et parfois à leur façon : Internet Explorer 5 calculait la largeur d'un bloc autrement que le standard, un écart que vous retrouverez dans le contenu sur le modèle de boîte. Une même page s'affichait donc différemment d'un navigateur à l'autre, et beaucoup de sites affichaient « optimisé pour Internet Explorer ».

Les navigateurs ont fini par converger vers les standards, mais ils ne pouvaient pas casser les millions de pages écrites pour les anciens comportements. C'est la **rétrocompatibilité** : une page de 1998 doit encore s'afficher aujourd'hui. Deux traces le montrent :

- une page sans la première ligne `<!DOCTYPE html>` est affichée en **mode quirks** (« bizarreries »), qui imite les anciens navigateurs ; avec cette ligne, le navigateur applique les standards actuels. C'est pourquoi elle ouvre toute page que vous écrirez ;
- `<marquee>` est classé obsolète, mais le standard HTML demande encore aux navigateurs de l'afficher.

Aujourd'hui, les écarts entre navigateurs portent surtout sur les fonctions récentes. Depuis 2022, les éditeurs des trois moteurs mènent chaque année un projet commun, **Interop**, pour les réduire. Avant d'utiliser une fonction récente, un site comme *Can I use* dit quels navigateurs la connaissent.

> 📖 [Qu'est-ce que le HTML ? (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Structuring_content) · [Qu'est-ce que le CSS ? (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Styling_basics/What_is_CSS) · [Qu'est-ce que JavaScript ? (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Scripting/What_is_JavaScript) · [Le HTML Living Standard (WHATWG, en anglais)](https://html.spec.whatwg.org/) · [ECMA-262 (Ecma International, en anglais)](https://tc39.es/ecma262/) · [Modes quirks et standard (MDN)](https://developer.mozilla.org/fr/docs/Web/HTML/Guides/Quirks_mode_and_standards_mode) · [Can I use (en anglais)](https://caniuse.com/)

## Trois questions pour vérifier ce que vous avez retenu

```quiz
title: "HTML, CSS et JavaScript"
tracksProgress: false
showNotice: false
place: stage
questions:
  - prompt: "Un bouton doit devenir rose et, au clic, afficher un message. Quel langage fait quoi ?"
    answers:
      - "Le HTML crée le bouton, le CSS le rend rose, le JavaScript réagit au clic"
      - "Le CSS crée le bouton et le rend rose, le HTML réagit au clic"
      - "Le JavaScript fait les trois : créer, colorer, réagir"
    correct: 1
    explanation: "Le HTML dit ce que la page contient, le CSS à quoi elle ressemble, le JavaScript ce qui se passe quand on agit."
  - prompt: "Une page écrit `<link rel=\"stylesheet\" href=\"Style.css\">`, mais le fichier s'appelle `style.css`. Que se passe-t-il sur un serveur ?"
    answers:
      - "Le navigateur affiche une erreur à la place de la page"
      - "La page s'affiche sans son style, sans aucun message à l'écran"
      - "Le navigateur corrige le nom tout seul"
    correct: 2
    explanation: "Pour la plupart des serveurs, `Style.css` et `style.css` sont deux fichiers différents. Le fichier n'est pas trouvé, et la page s'affiche avec l'apparence par défaut, en silence."
  - prompt: "Pourquoi une page commence-t-elle par `<!DOCTYPE html>` ?"
    answers:
      - "Pour que le serveur sache qu'il doit envoyer du HTML"
      - "Pour charger le moteur JavaScript"
      - "Pour que le navigateur applique les standards actuels au lieu d'imiter les anciens navigateurs (le mode quirks)"
    correct: 3
    explanation: "Sans doctype, le navigateur passe en mode quirks, qui reproduit les bizarreries des anciens navigateurs pour ne pas casser les vieilles pages. Avec, il suit les standards."
```

## Récap

- Une page parle trois langages : **HTML** pour le contenu, **CSS** pour l'apparence, **JavaScript** pour le comportement.
- Le HTML relie les deux autres par `<link rel="stylesheet" href="…">` et `<script src="…"></script>`, avec le nom exact du fichier ; une erreur ne s'affiche pas, la page perd son style ou son comportement en silence.
- Des **standards** décrivent ces langages : le HTML Living Standard du WHATWG, les modules CSS du W3C, ECMAScript d'Ecma International.
- Chaque navigateur a un **moteur de rendu** et un **moteur JavaScript** : Blink et V8, Gecko et SpiderMonkey, WebKit et JavaScriptCore.
- Les navigateurs ont longtemps divergé ; la **rétrocompatibilité** garde les vieilles pages lisibles, d'où le **mode quirks** sans doctype.

Ces trois langages ne servent plus seulement à faire des pages : on en fait des applications, des apps mobiles et des logiciels de bureau. C'est l'objet du contenu [Le web partout](https://byte-layers.com/fr/bits/web-everywhere).

```ack
J'ai compris
```
