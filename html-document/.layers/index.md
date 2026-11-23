---
title: "Le squelette d'une page HTML, son texte, ses liens et ses images"
description: "Balise, élément et attribut ; le squelette que tout navigateur sait lire (doctype, lang, charset, title) ; titres, paragraphes et listes ; les liens vers une autre page ou vers un endroit de la page ; les images, leur chemin relatif et leur texte alternatif."
tags:
  - bit
  - web
  - html
difficulty: beginner
duration: 15
requires: "0.9.0"
---

Une page HTML est un fichier texte qui suit une forme précise : un squelette que tout navigateur sait lire, dans lequel on pose du texte, des liens et des images. Vous saurez lire une balise et ses attributs, écrire ce squelette ligne par ligne et dire à quoi sert chacune, structurer un texte en titres, paragraphes et listes, faire un lien vers une autre page ou vers un endroit de la même page, et afficher une image avec un chemin juste et un texte alternatif.

**Prérequis** : [Une page web : HTML, CSS et JavaScript](https://byte-layers.com/fr/bits/web-page-languages), pour le rôle du HTML et le doctype.

# Le squelette d'une page HTML, son texte, ses liens et ses images

Des trois langages d'une page, le HTML vient en premier : c'est lui qui porte le contenu, et c'est lui qui cite les deux autres. Ce contenu part d'une page vide et la remplit, du squelette jusqu'aux images.

## Une balise, un élément, un attribut

Le HTML entoure chaque morceau de contenu de **balises**, qui disent au navigateur ce qu'est ce morceau. Voici un paragraphe :

```html
<p class="intro">Bonjour, je m'appelle Ada.</p>
```

| Morceau | Ce que c'est |
|---|---|
| `<p>` | la **balise ouvrante** : « ici commence un paragraphe » |
| `</p>` | la **balise fermante**, avec une barre oblique : « ici finit le paragraphe » |
| `class="intro"` | un **attribut**, un nom et une valeur entre guillemets : une information de plus, écrite dans la balise ouvrante |
| tout l'ensemble | un **élément** : le paragraphe, avec son contenu |

Les éléments s'emboîtent les uns dans les autres, comme des boîtes. Suivez le navigateur qui lit ces cinq lignes.

```scene
lesson: assets/html.scene.json
step: emboiter
```

Chaque balise ouvrante ouvre une boîte dans celle qui est ouverte, et l'on ferme toujours **le dernier ouvert en premier**. Quelques éléments n'ont pas de contenu, donc pas de balise fermante : `<meta>`, `<img>`, `<br>`. Enfin, ce qui est écrit entre `<!--` et `-->` est un **commentaire** : le navigateur ne l'affiche jamais.

## Le squelette : doctype, html, head, body

Toute page commence par le même squelette. Le voici, complet :

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Mon premier site</title>
</head>
<body>
  <h1>Ma première page</h1>
  <p>Bonjour ! J'apprends à créer des pages web, à la main.</p>
</body>
</html>
```

Chaque ligne a sa raison d'être :

| Ligne | Ce qu'elle dit, et ce qui se passe sans elle |
|---|---|
| `<!DOCTYPE html>` | « ceci est du HTML actuel », en toute première ligne. Sans elle, le navigateur imite les anciens navigateurs (le mode quirks) |
| `<html lang="fr">` | l'élément qui contient tout, et la langue de la page. Sans `lang`, un lecteur d'écran prononce mal, la traduction automatique se trompe |
| `<head>` … `</head>` | les informations sur la page, que le visiteur ne voit pas dans la page |
| `<meta charset="utf-8">` | l'**encodage** : comment lire les octets du fichier. Sans elle, les accents peuvent casser |
| `<meta name="viewport" …>` | sur un téléphone, afficher la page à la largeur de l'écran. Sans elle, une version de bureau réduite, illisible |
| `<title>` | le titre de l'**onglet**, des favoris et des résultats de recherche. Sans elle, l'onglet affiche l'adresse du fichier |
| `<body>` … `</body>` | tout ce que le visiteur voit dans la page |

Voici où va chaque partie quand le navigateur lit le fichier.

```scene
lesson: assets/html.scene.json
step: squelette
```

Le point qui surprend le plus : `<title>` et `<h1>` ne s'affichent pas au même endroit. `<title>` va dans l'onglet, jamais dans la page ; `<h1>` est le grand titre en haut de la page. Dans le squelette ci-dessus, ils ont volontairement deux textes différents.

## À toi : complète le squelette

Sans regarder plus haut, complète le squelette : cinq trous, un mot chacun.

```fill
file: assets/squelette.fill.html
solution: assets/squelette.html
title: Le squelette d'une page
blanks:
  - answers: [html]
    hint: Le doctype annonce le langage de la page, en un mot.
  - answers: [fr]
    hint: Le code de la langue française, en deux lettres.
  - answers: [charset]
    hint: L'attribut qui déclare l'encodage des caractères.
  - answers: [title]
    hint: La balise du texte affiché dans l'onglet ; sa balise fermante est déjà écrite.
  - answers: [body]
    hint: La balise de tout ce que le visiteur voit ; sa balise fermante est déjà écrite.
```

## L'encodage : pourquoi les accents cassent sans `charset`

Un fichier est une suite d'octets, des nombres. L'**encodage** est la table qui dit quel nombre correspond à quel caractère. Votre éditeur enregistre en **UTF-8**, l'encodage du web, qui couvre les accents, les emojis et presque toutes les écritures du monde. Dans UTF-8, le `é` s'écrit avec deux octets. Regarde ce qui arrive quand le navigateur les lit avec une autre table.

```scene
lesson: assets/texte.scene.json
step: encodage
```

Deux octets lus comme deux caractères : `créé` devient `crÃ©Ã©`. La ligne `<meta charset="utf-8">` lève le doute. Elle se place au début du `<head>`, parce que le navigateur ne la cherche que dans les premiers octets du fichier. Sans elle, le navigateur devine : parfois juste, parfois non, selon le navigateur et la façon dont la page est servie. On l'écrit donc toujours.

> 💡 **Remarque.** Les exercices de ce contenu se jouent dans un aperçu qui reçoit le texte déjà décodé : l'oubli du `charset` n'y casse rien. La vraie panne se voit sur un fichier ouvert depuis votre disque.

## Titres, paragraphes et listes

Dans le `<body>`, le texte se range en éléments qui disent ce qu'il est. Chacun lui donne sa forme à l'écran :

```scene
lesson: assets/texte.scene.json
step: texte
```

L'essentiel, à garder sous la main :

| Élément | Ce que c'est |
|---|---|
| `<h1>` à `<h6>` | des titres, du plus important (`h1`, un seul par page) au moins important |
| `<p>` | un paragraphe |
| `<strong>`, `<em>` | un passage important (affiché en gras), un passage sur lequel on insiste (affiché en italique) |
| `<ul>` et `<li>` | une liste à puces (*unordered list*), un élément par `<li>` |
| `<ol>` et `<li>` | une liste numérotée (*ordered list*) : le navigateur calcule les numéros |
| `<br>` | un retour à la ligne à l'intérieur d'un paragraphe, pour une adresse postale par exemple |

Le navigateur ne tient pas compte des retours à la ligne ni des espaces en trop dans le fichier : deux paragraphes séparés par une ligne vide, sans balise `<p>`, s'affichent collés en un seul bloc. C'est la balise qui fait le paragraphe, pas la mise en page du fichier.

## Les liens : vers une autre page, vers un endroit de la page

Un lien s'écrit avec l'élément `<a>` (*anchor*, ancre), et son attribut `href` dit où il mène :

```scene
lesson: assets/texte.scene.json
step: liens
```

| Lien vers | Le `href`, et ce qu'il faut savoir |
|---|---|
| un autre site | `https://fr.wikipedia.org/` : une adresse complète, protocole compris |
| une page du même site | `contact.html` : un **chemin relatif**, à partir du dossier de la page |
| un endroit de la page | `#horaires` : vise l'élément qui porte `id="horaires"` |
| une adresse e-mail | `mailto:contact@exemple.fr` : ouvre la messagerie du visiteur, s'il en a une |

Pour ouvrir un lien dans un nouvel onglet, on ajoute `target="_blank"`, et avec lui `rel="noopener"`, qui empêche la page ouverte d'agir sur la vôtre.

Le lien vers un endroit de la page demande **deux gestes** : donner un `id` à l'élément visé, puis écrire le lien avec un dièse. Le lien seul ne fait rien, et rien ne vous le signale : le clic ne mène nulle part.

## À toi : des liens qui mènent quelque part

Dans la page ci-dessous, le premier lien devrait faire descendre jusqu'aux horaires, et le lien vers Wikipédia devrait s'ouvrir dans un nouvel onglet. Corrige `index.html`.

```playground
runtime: web
title: Des liens qui mènent quelque part
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Le Capitole de Toulouse</title>
    </head>
    <body>
      <h1>Le Capitole de Toulouse</h1>
      <p>Vous venez le visiter ? Allez directement aux <a href="#horaires">horaires d'ouverture</a>.</p>
      <p>Son histoire complète est sur <a href="https://fr.wikipedia.org/wiki/Capitole_de_Toulouse">la page Wikipédia du Capitole</a>.</p>

      <h2>Un peu d'histoire</h2>
      <p>Le Capitole abrite la mairie de Toulouse depuis le Moyen Âge.</p>
      <p>Sa façade actuelle, en brique rose et pierre, date du XVIIIe siècle.</p>
      <p>La place qui s'étend devant lui porte le même nom.</p>
      <p>Une grande croix occitane est dessinée sur ses dalles.</p>

      <h2>Horaires</h2>
      <p>La salle des Illustres se visite tous les jours, de 10 h à 19 h.</p>
    </body>
    </html>
verify:
  - label: le titre « Horaires » porte l'`id` que vise le premier lien
    selector: "h2#horaires"
    text: Horaires
    hint: "Le lien vise `#horaires` : ajoute `id=\"horaires\"` dans la balise ouvrante du `<h2>` « Horaires »"
  - label: le lien vers Wikipédia s'ouvre dans un nouvel onglet
    selector: "a[href*='wikipedia']"
    attr: { target: _blank }
    hint: "Ajoute `target=\"_blank\"` dans la balise `<a>`"
  - label: et il porte `rel="noopener"`
    selector: "a[href*='wikipedia']"
    attr: { rel: /noopener/ }
solution: assets/ancre.solution
```

L'aperçu bloque l'ouverture de nouveaux onglets : le clic sur le lien Wikipédia peut n'y rien faire, alors que les contrôles passent. Dans une vraie page, il ouvre bien un onglet.

## Les images : chemin relatif, casse et texte alternatif

Une image s'affiche avec l'élément `<img>`, qui n'a pas de balise fermante :

```html
<img src="images/capitole.svg" alt="La façade du Capitole : un long bâtiment rose à colonnes">
```

L'attribut `src` donne le **chemin** du fichier image. Un chemin relatif part du dossier de la page, comme pour un lien :

| L'image est… | On écrit |
|---|---|
| dans le même dossier que la page | `src="capitole.svg"` |
| dans un sous-dossier `images/` | `src="images/capitole.svg"` |
| dans un dossier voisin (la page est dans `site/pages/`, l'image dans `site/images/`) | `src="../images/capitole.svg"` : `..` remonte d'un dossier |

Suivez le troisième cas, morceau par morceau.

```scene
lesson: assets/chemin.scene.json
step: chemin
```

Sur la plupart des serveurs, les **majuscules comptent** : `Images/capitole.svg` et `images/capitole.svg` sont deux chemins différents. Sous Windows et macOS, le disque les confond par défaut : la page marche chez vous, puis l'image disparaît une fois en ligne.

L'attribut `alt` donne le **texte alternatif** : ce qui s'affiche quand l'image ne charge pas, ce que lit un lecteur d'écran à une personne aveugle, et ce que « voit » un moteur de recherche. On y décrit ce que l'image montre, sans commencer par « image de ».

## À toi : une image qui s'affiche, et qui se décrit

Dans la page ci-dessous, l'image ne s'affiche pas, et elle n'a pas de texte alternatif. Le fichier image est fourni, en lecture seule, dans le dossier `images/`. Corrige `index.html`.

```playground
runtime: web
title: Une image qui s'affiche, et qui se décrit
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Le Capitole de Toulouse</title>
    </head>
    <body>
      <h1>Le Capitole de Toulouse</h1>
      <img src="Images/capitole.svg">
      <p>Sa façade, en brique rose et pierre, date du XVIIIe siècle.</p>
    </body>
    </html>
  images/capitole.svg: |
    <svg xmlns="http://www.w3.org/2000/svg" width="240" height="120" viewBox="0 0 240 120">
      <rect width="240" height="120" fill="rgb(224, 242, 254)"/>
      <rect x="20" y="40" width="200" height="70" fill="rgb(236, 72, 153)"/>
      <rect x="20" y="32" width="200" height="8" fill="rgb(250, 232, 220)"/>
      <g fill="rgb(250, 232, 220)">
        <rect x="40" y="48" width="8" height="62"/><rect x="70" y="48" width="8" height="62"/>
        <rect x="100" y="48" width="8" height="62"/><rect x="132" y="48" width="8" height="62"/>
        <rect x="162" y="48" width="8" height="62"/><rect x="192" y="48" width="8" height="62"/>
      </g>
      <g fill="rgb(37, 99, 235)">
        <rect x="80" y="12" width="12" height="8"/><rect x="114" y="8" width="12" height="8"/><rect x="148" y="12" width="12" height="8"/>
      </g>
    </svg>
open: [index.html, images/capitole.svg]
lock: [images/capitole.svg]
verify:
  - label: l'image s'affiche, à sa largeur de 240 px
    selector: img
    style: { width: 240px }
    hint: "Compare le chemin écrit dans `src` au nom du dossier et du fichier, lettre par lettre : la casse compte"
  - label: l'image a un texte alternatif qui la décrit
    selector: img
    attr: { alt: '/\S{3,}/' }
    hint: "Ajoute `alt=\"…\"` dans la balise `<img>`, avec une phrase qui dit ce qu'on voit"
solution: assets/image.solution
```

Avant de corriger le chemin, ajoute d'abord le texte alternatif, et regarde l'aperçu : le texte s'affiche à la place de l'image cassée. C'est ce que verra un visiteur dont la connexion a échoué.

> 📖 [Bien démarrer avec HTML (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Structuring_content/Basic_HTML_syntax) · [Ce que contient l'en-tête d'une page (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Structuring_content/Webpage_metadata) · [Créer des liens (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Structuring_content/Creating_links) · [L'élément img (MDN)](https://developer.mozilla.org/fr/docs/Web/HTML/Reference/Elements/img)

## Trois questions pour vérifier ce que vous avez retenu

```quiz
title: "Squelette, texte, liens et images"
tracksProgress: false
showNotice: false
place: stage
questions:
  - prompt: "Où s'affiche le texte de la balise `<title>` ?"
    answers:
      - "Dans l'onglet du navigateur, les favoris et les résultats de recherche, jamais dans la page"
      - "En grand, tout en haut de la page"
      - "Nulle part : il ne sert qu'aux moteurs de recherche"
    correct: 1
    explanation: "`<title>` donne le titre de l'onglet. Le grand titre dans la page, c'est `<h1>`."
  - prompt: "Un lien `<a href=\"#tarifs\">Tarifs</a>` ne fait rien quand on clique dessus. Quelle est la cause la plus probable ?"
    answers:
      - "Il manque `target=\"_blank\"`"
      - "Aucun élément de la page ne porte `id=\"tarifs\"`"
      - "Un lien interne ne marche que sur un serveur"
    correct: 2
    explanation: "Un lien vers `#tarifs` vise l'élément qui porte `id=\"tarifs\"`. Sans cet `id`, le clic ne mène nulle part, sans message."
  - prompt: "La page affiche son image sur votre Mac, mais plus une fois en ligne. Le fichier s'appelle `Logo.png`, la page écrit `src=\"logo.png\"`. Pourquoi ?"
    answers:
      - "Les images PNG ne s'affichent pas sur un serveur"
      - "Il manque le texte alternatif"
      - "Le serveur distingue les majuscules : `logo.png` n'existe pas ; le disque du Mac, lui, les confondait"
    correct: 3
    explanation: "Sur la plupart des serveurs, `Logo.png` et `logo.png` sont deux fichiers différents. Sous macOS et Windows, le disque ignore la casse par défaut : l'erreur ne se voit qu'en ligne."
```

## Récap

- Une **balise** ouvre et ferme un **élément** ; un **attribut** (`nom="valeur"`) s'écrit dans la balise ouvrante.
- Le **squelette** : `<!DOCTYPE html>` en première ligne, `<html lang="fr">`, un `<head>` avec `<meta charset="utf-8">`, le viewport et `<title>`, puis un `<body>` pour ce qu'on voit.
- Sans `charset`, le navigateur devine l'**encodage**, et les accents peuvent casser.
- Le texte se range en titres `<h1>` à `<h6>`, paragraphes `<p>`, listes `<ul>`/`<ol>` et `<li>`.
- Un **lien** `<a href="…">` mène à un autre site, une autre page (chemin relatif) ou un endroit de la page, qui doit porter l'`id` visé.
- Une **image** `<img src="…" alt="…">` : un chemin relatif exact, majuscules comprises, et un texte alternatif qui décrit ce qu'elle montre.

Votre page affiche du contenu. Elle ne dit pas encore ce qu'est chaque bloc : un menu, un article, un pied de page. C'est l'objet du contenu [Le HTML sémantique : le sens avant la forme](https://byte-layers.com/fr/bits/semantic-html).

```ack
J'ai compris
```
