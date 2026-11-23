---
title: "Une page web : HTML, CSS et JavaScript"
description: "Les trois langages d'une page et leurs rôles, puis une petite page construite pas à pas : les balises HTML, la structure html, head et body, les attributs, et comment la page relie sa feuille de style et son script."
tags:
  - bit
  - web
  - html
  - css
difficulty: beginner
duration: 30
requires: "0.9.0"
---

Le texte qu'un navigateur reçoit pour afficher une page est écrit dans trois langages : **HTML** pour le contenu, **CSS** pour l'apparence, **JavaScript** pour le comportement. Vous allez construire, pas à pas, une petite page qui les utilise tous les trois : un titre et un bouton.

**Prérequis** : [Le web : une adresse, une requête, une page](https://byte-layers.com/fr/bits/web-request-response), pour la requête, la réponse et les fichiers qu'une page demande. Aucune connaissance en programmation n'est demandée.

# Une page web : HTML, CSS et JavaScript

Quand le navigateur reçoit une page, il reçoit du texte. Ce contenu montre ce qu'il y a dans ce texte, et comment l'écrire vous-même.

## Trois langages, trois rôles

Une page web se partage entre trois langages, et chacun répond à une seule question :

| Langage | Fichier habituel | La question à laquelle il répond | Exemple |
|---|---|---|---|
| **HTML** (*HyperText Markup Language*) | `index.html` | qu'est-ce que la page contient ? | un titre, un paragraphe, un bouton |
| **CSS** (*Cascading Style Sheets*) | `style.css` | à quoi ça ressemble ? | le bouton est rose, le texte fait 20 pixels |
| **JavaScript** | `script.js` | que se passe-t-il quand on agit ? | un clic sur le bouton change le titre |

Regardez ce que chacun apporte à une même petite page, puis ce qui reste quand on en retire un.

```scene
lesson: assets/langages.scene.json
step: trois
```

C'est cette page, un titre et un bouton, que vous allez construire. Retenez la **séparation** : sans le CSS, la page garde tout son contenu ; sans le JavaScript, elle s'affiche, mais le clic ne fait plus rien.

## Le HTML : des balises

Tout commence par un fichier HTML. Le HTML est un langage fait de **balises** : des mots entre chevrons, `<` et `>`, qui disent le rôle de ce qu'ils entourent. Pour un titre principal, c'est la balise `h1` (*heading 1*, titre de niveau 1) :

```html
<h1>Bonjour !</h1>
```

`<h1>` **ouvre** le titre, `</h1>` le **ferme** : la barre oblique `/` marque la fin. Entre les deux, le texte qui s'affiche. Pour un bouton, la balise s'appelle `button` : complète le code sur le plateau.

```fill
file: assets/bouton.fill.html
solution: assets/bouton.html
title: Un titre et un bouton
blanks:
  - answers: [button]
    hint: La balise porte le nom du bouton en anglais, sans chevrons dans la case.
  - answers: [/button]
    hint: "Une balise ouverte se ferme : le même nom, précédé d'une barre oblique `/`."
```

Une balise s'ouvre et se **ferme**, et l'oubli de la fermeture est le piège le plus courant : le navigateur ne signale rien, il devine, souvent mal. Quelques balises n'ont pas de fermeture, parce qu'elles n'ont pas de contenu, comme `<img>` pour une image ou `<br>` pour un retour à la ligne : on les dit **auto-fermantes**.

Il existe une centaine de balises, et personne ne les connaît toutes par cœur. Ce qui compte, c'est de savoir **où chercher** : la [référence des éléments HTML de MDN](https://developer.mozilla.org/fr/docs/Web/HTML/Reference/Elements) les décrit toutes. Les principales, vous les reconnaîtrez vite, par habitude.

## La structure d'une page : html, head et body

Des balises seules ne suffisent pas : le navigateur a besoin d'une **structure**, et de quelques informations pour bien afficher la page. Une page HTML est une enveloppe, `<html>`, qui porte deux parties :

- l'**en-tête**, `<head>` : les informations pour le navigateur, comme le nom de l'onglet, les **métadonnées**, ou la feuille de style à charger ;
- le **corps**, `<body>` : ce qui s'affiche, nos balises de titre et de contenu.

Regardez-la se construire, ligne par ligne :

```scene
lesson: assets/page.scene.json
step: structure
```

La première ligne, `<!DOCTYPE html>`, n'est pas une balise : elle annonce au navigateur une page en HTML d'aujourd'hui. Ensuite, l'**en-tête** puis le **corps**, toujours dans cet ordre, tous deux dans `<html>`.

## La structure de base, ligne par ligne

Voici la structure de base d'une page, que vous retrouverez en tête de toutes les pages que vous écrirez. Une balise peut porter des **attributs** : des précisions écrites `nom="valeur"` dans la balise ouvrante.

```scene
lesson: assets/page.scene.json
step: base
```

`<html lang="fr">` dit que le contenu est en **français** : les lecteurs d'écran le prononcent correctement, et le navigateur ne propose pas de le traduire. `<meta charset="utf-8">` dit comment les caractères sont **codés** : sans lui, les accents peuvent s'afficher en signes bizarres. `<title>` donne le texte de l'**onglet**, pas un titre dans la page.

## À toi : ta première page complète

Bienvenue sur le **playground** : comme sur un ordinateur quand on écrit une page, un éditeur pour le code, et un aperçu pour voir le résultat. Complète la structure : la langue française, un titre d'onglet, puis, dans le corps, le titre `Bonjour !` et le bouton `Clique-moi`.

```playground
runtime: web
title: Ta première page
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="">
    <head>
      <meta charset="utf-8">
      <title></title>
    </head>
    <body>
      <!-- À toi : un titre h1 « Bonjour ! », puis un bouton « Clique-moi » -->
    </body>
    </html>
verify:
  - label: la page est en français
    file: index.html
    includes: /<html lang="fr">/
    hint: "Le code de la langue française tient en deux lettres, entre les guillemets de `lang=\"\"`."
  - label: l'onglet a un titre
    file: index.html
    includes: /<title>[^<]+<\/title>/
    hint: "Écris un texte entre `<title>` et `</title>`."
  - label: la page affiche le titre « Bonjour ! »
    selector: h1
    text: Bonjour !
    hint: "`<h1>Bonjour !</h1>`, dans le `<body>`"
  - label: la page affiche un seul bouton « Clique-moi »
    selector: button
    count: 1
    text: Clique-moi
    hint: "Deux boutons ? Un `<button>` non fermé : vérifie le `</button>`."
solution: assets/page.solution
```

Si le contrôle du bouton échoue alors que l'aperçu en montre un, regarde la fermeture : `<button>Clique-moi<button>` ouvre un **second** bouton, vide, au lieu de fermer le premier.

## Ajouter du CSS : `<link>` dans l'en-tête

Le CSS peut s'écrire dans la page, entre `<style>` et `</style>`, mais on le range le plus souvent dans un fichier à part, la **feuille de style**, que la page relie par une balise `<link>` dans son en-tête.

```scene
lesson: assets/page.scene.json
step: css
```

Pourquoi dans l'**en-tête** ? Le navigateur lit la page de haut en bas : les règles sont chargées avant le corps, et la page s'affiche stylée **dès le premier affichage**. Pourquoi `href="style.css"` et pas une adresse en `https://` ? C'est un chemin **relatif** : le fichier est à côté de la page, que la page soit sur un serveur ou sur votre disque. Avec une barre au début, `/style.css` partirait de la racine du site.

## À toi : relie la feuille de style

La feuille `style.css` est prête, et en lecture seule : elle rend le bouton rose. Relie-la dans l'en-tête de `index.html`. Le fonctionnement du CSS, ses règles et sa syntaxe, fait l'objet d'un autre contenu : ici, il s'agit seulement de **relier** le fichier.

```playground
runtime: web
title: Relie la feuille de style
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Ma page</title>
      <!-- À toi : relie la feuille de style style.css -->
    </head>
    <body>
      <h1>Bonjour !</h1>
      <button type="button" id="bouton">Clique-moi</button>
    </body>
    </html>
  style.css: |
    #bouton {
      background-color: rgb(219, 39, 119);
      color: white;
      border: none;
      padding: 8px 16px;
    }
open: [index.html, style.css]
lock: [style.css]
verify:
  - label: le bouton est rose, la feuille de style est donc chargée
    selector: "#bouton"
    style: { background-color: "rgb(219, 39, 119)" }
    hint: "`<link rel=\"stylesheet\" href=\"style.css\">`, dans le `<head>`"
  - label: la feuille de style est reliée dans l'en-tête
    file: index.html
    includes: /<head>[\s\S]*<link[^>]*href="style\.css"[\s\S]*<\/head>/
    hint: "La balise `<link>` va entre `<head>` et `</head>`."
solution: assets/css.solution
```

> 💡 **Remarque.** Le nom du fichier s'écrit **exactement** : pour un serveur, `Style.css` et `style.css` sont deux fichiers différents, et un nom faux ne donne aucun message, seulement une page sans style.

## Ajouter du JavaScript : `<script>` à la fin du corps

Le JavaScript, lui aussi, peut s'écrire dans la page, entre `<script>` et `</script>`, ou dans un fichier à part, relié par `<script src="script.js"></script>`. On place souvent cette balise **juste avant** `</body>`.

```scene
lesson: assets/page.scene.json
step: js
```

À la fin du corps, le titre et le bouton sont **déjà lus** quand le script s'exécute : il peut les trouver. Placé plus haut, il chercherait un bouton qui n'existe pas encore. Il existe une autre solution, l'attribut `defer`, que le cours de JavaScript détaille.

## À toi : relie le script

Le script `script.js` est prêt, et en lecture seule : au clic sur le bouton, il change le titre en « Merci ! ». Relie-le, juste avant `</body>`, puis clique sur le bouton de l'aperçu.

```playground
runtime: web
title: Relie le script
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Ma page</title>
      <link rel="stylesheet" href="style.css">
    </head>
    <body>
      <h1 id="titre">Bonjour !</h1>
      <button type="button" id="bouton">Clique-moi</button>
      <!-- À toi : relie le script script.js -->
    </body>
    </html>
  style.css: |
    #bouton {
      background-color: rgb(219, 39, 119);
      color: white;
      border: none;
      padding: 8px 16px;
    }
  script.js: |
    document.querySelector('#bouton').addEventListener('click', function () {
      document.querySelector('#titre').textContent = 'Merci !';
    });
open: [index.html, script.js]
lock: [style.css, script.js]
show: [editor, preview, console]
verify:
  - label: un clic sur le bouton change le titre en « Merci ! »
    click: "#bouton"
    selector: "#titre"
    text: Merci !
    hint: "`<script src=\"script.js\"></script>`, juste avant `</body>`"
  - label: aucune erreur dans la console
    errors: none
solution: assets/js.solution
```

Vous n'avez pas à comprendre le contenu de `script.js` : le JavaScript a son propre cours. Ici aussi, il s'agit de **relier** le bon fichier, au bon endroit.

## Le tout : une page avec deux erreurs

Voici la page complète, écrite par quelqu'un qui s'est trompé deux fois. Le bouton devrait être rose, et un clic devrait changer le titre en « Merci ! ». Ni l'un ni l'autre ne marche. `style.css` et `script.js` sont justes et en lecture seule : corrige `index.html`.

```playground
runtime: web
title: Trouve les deux erreurs
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

Les deux fautes sont classiques. `<style>` sert à écrire du CSS directement dans la page ; il ne sait pas charger un fichier, et un attribut qu'il ne connaît pas est simplement ignoré. Le `S` majuscule de `Script.js` désigne un fichier qui n'existe pas. Dans les deux cas, **rien ne s'affiche** pour vous le dire : il faut savoir où regarder.

> 📖 [Qu'est-ce que le HTML ? (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Structuring_content) · [Référence des éléments HTML (MDN)](https://developer.mozilla.org/fr/docs/Web/HTML/Reference/Elements) · [Qu'est-ce que le CSS ? (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Styling_basics/What_is_CSS) · [Qu'est-ce que JavaScript ? (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Scripting/What_is_JavaScript)

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
  - prompt: "Dans quelle partie de la page relie-t-on la feuille de style, et pourquoi ?"
    answers:
      - "Dans le `<head>`, pour que les règles soient chargées avant l'affichage du corps"
      - "À la fin du `<body>`, pour que la page s'affiche plus vite"
      - "N'importe où : le navigateur la trouve toujours"
    correct: 1
    explanation: "Le navigateur lit la page de haut en bas. Reliée dans l'en-tête, la feuille de style est chargée avant le corps : la page s'affiche stylée dès le premier affichage."
  - prompt: "Une page écrit `<link rel=\"stylesheet\" href=\"Style.css\">`, mais le fichier s'appelle `style.css`. Que se passe-t-il sur un serveur ?"
    answers:
      - "Le navigateur affiche une erreur à la place de la page"
      - "La page s'affiche sans son style, sans aucun message à l'écran"
      - "Le navigateur corrige le nom tout seul"
    correct: 2
    explanation: "Pour la plupart des serveurs, `Style.css` et `style.css` sont deux fichiers différents. Le fichier n'est pas trouvé, et la page s'affiche avec l'apparence par défaut, en silence."
```

## Récap

- Une page parle trois langages : **HTML** pour le contenu, **CSS** pour l'apparence, **JavaScript** pour le comportement.
- Le HTML est fait de **balises** qui s'ouvrent et se ferment (`<h1>…</h1>`) ; quelques-unes, sans contenu, n'ont pas de fermeture. La référence de MDN les décrit toutes.
- Une page est une enveloppe `<html>` qui porte un **en-tête** `<head>` (pour le navigateur) puis un **corps** `<body>` (ce qui s'affiche), après la ligne `<!DOCTYPE html>`.
- Les **attributs** précisent une balise : `lang="fr"` pour la langue, `charset="utf-8"` pour les accents.
- La feuille de style se relie dans l'en-tête par `<link rel="stylesheet" href="style.css">`, le script à la fin du corps par `<script src="script.js"></script>`, avec le nom exact du fichier : une erreur ne s'affiche pas.

Qui décide de ce que fait chaque balise, et pourquoi une page peut s'afficher différemment d'un navigateur à l'autre ? C'est l'objet du contenu [Les standards du web et les moteurs des navigateurs](https://byte-layers.com/fr/bits/web-standards-browsers).

```ack
J'ai compris
```
