---
title: "Les formulaires HTML"
description: "Un formulaire recueille des informations et les envoie au serveur : form, action et method, input et ses types, label relié par for et id, name, required. Les pièges : le champ sans name, le label non relié, le contrôle du navigateur pris pour une sécurité."
tags:
  - bit
  - html
difficulty: beginner
duration: 15
requires: "0.9.0"
---

Une page peut **recueillir** des informations avec un formulaire, et les envoyer au serveur. Vous saurez écrire un formulaire dont chaque champ est relié à son étiquette, bien envoyé, et contrôlé par le navigateur.

**Prérequis** : le bit [Le squelette d'une page HTML](https://byte-layers.com/fr/bits/html-document), pour les balises et leurs attributs.

# Les formulaires HTML

Jusqu'ici, la page montre : du texte, des images, des liens. Ce contenu ajoute une structure du HTML qui fait l'inverse : le formulaire, pour que le visiteur réponde.

## Un formulaire : ce que la page envoie au serveur

Un formulaire, c'est le chemin inverse d'une page : au lieu de recevoir du texte du serveur, le navigateur lui **envoie** ce que le visiteur a saisi. Tous les champs vivent dans un `<form>` ; son attribut `action` donne l'adresse qui reçoit les données. L'**étiquette** d'un champ s'écrit dans un `<label>`.

```scene
lesson: assets/forms.scene.json
step: formulaire
```

Le `for` de l'étiquette reprend **exactement** l'`id` du champ : le clic sur l'étiquette met le curseur dans le champ (ou coche la case). Chaque champ a trois attributs qui ne servent pas à la même chose :

| Attribut | Pour qui, et à quoi |
|---|---|
| `id` | **la page** : un nom unique, que vise le `for` de l'étiquette |
| `name` | **le serveur** : le nom sous lequel la valeur est envoyée, `email=camille%40exemple.fr` |
| `type` | **le navigateur** : le genre de champ, `text`, `email`, `tel`, `date`, `checkbox`, `radio` |

## Comment les données partent : method

Le formulaire a un second attribut, **`method`** : il dit comment les données voyagent jusqu'au serveur. Deux valeurs, `get` et `post`, et une différence qui se voit dans la barre d'adresse.

```scene
lesson: assets/forms.scene.json
step: methode
```

Avec `method="get"`, les données s'ajoutent à l'adresse, après un `?` : elles s'affichent, restent dans l'historique et se partagent avec le lien. C'est le bon choix pour une recherche. Avec `method="post"`, elles voyagent dans la requête, sans s'afficher dans l'adresse : c'est le choix d'un message ou d'une inscription.

## Contrôler la saisie : required et type

Le navigateur peut vérifier un champ **avant** d'envoyer le formulaire : un champ obligatoire, une adresse e-mail.

```scene
lesson: assets/forms.scene.json
step: controle
```

Deux attributs suffisent, sur la balise du champ :

```html
<label for="email">Votre e-mail</label>
<input type="email" id="email" name="email" required>
```

L'attribut **`required`** fait refuser l'envoi tant que le champ est vide, et `type="email"` fait vérifier la présence d'un `@`. Ces contrôles rendent service au visiteur, mais ils se contournent : n'importe quel programme peut écrire au serveur sans passer par le formulaire. Le serveur doit tout revérifier.

## Les pièges : un champ sans name, une étiquette non reliée

Deux fautes ne se voient pas à l'écran. La première tient à ce que le navigateur envoie vraiment.

```scene
lesson: assets/forms.scene.json
step: envoi
```

Un champ **sans `name`** s'affiche et se remplit normalement, mais sa valeur **n'est pas envoyée** : le serveur ne la reçoit jamais. Une étiquette dont le **`for` ne correspond à aucun `id`** s'affiche aussi normalement, mais elle n'est plus reliée : le clic ne fait rien, et le lecteur d'écran annonce « zone de texte » sans dire laquelle. Aucun message d'erreur dans les deux cas.

## À toi : un formulaire de contact bien relié

Le champ Nom est le modèle, complet. Les trois autres ont chacun un défaut : trouve-les et corrige-les. Clique sur chaque étiquette dans l'aperçu : celle qui ne réagit pas n'est pas reliée. Le formulaire n'envoie rien dans l'aperçu, c'est voulu.

```playground
runtime: web
title: Un formulaire de contact bien relié
files:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
      <meta charset="utf-8">
      <title>Contact</title>
      <link rel="stylesheet" href="style.css">
    </head>
    <body>
      <form action="/contact" method="post">
        <p>
          <label for="nom">Votre nom</label>
          <input type="text" id="nom" name="nom" required>
        </p>
        <p>
          <label for="mail">Votre e-mail</label>
          <input type="text" id="email">
        </p>
        <p>
          <label for="message">Votre message</label>
          <textarea id="message" rows="5"></textarea>
        </p>
        <p>
          <input type="checkbox" id="newsletter" name="newsletter">
          <label>Je souhaite recevoir la lettre d'information</label>
        </p>
        <button type="submit">Envoyer</button>
      </form>
    </body>
    </html>
  style.css: |
    body {
      font-family: system-ui, sans-serif;
    }

    label {
      display: block;
    }

    #newsletter + label {
      display: inline;
    }
open: [index.html, style.css]
lock: [style.css]
check: ask
verify:
  - label: chaque champ a un `name`, sinon sa valeur n'est pas envoyée
    selector: "form input, form textarea"
    attr: { name: "/\\S/" }
    hint: "Comme le champ Nom : `name=\"email\"`, `name=\"message\"`."
  - label: l'étiquette de l'e-mail vise l'`id` du champ
    selector: "label[for=email]"
    count: 1
    hint: "Le `for` de l'étiquette dit `mail`, l'`id` du champ dit `email` : un seul des deux doit changer."
  - label: l'e-mail est vérifié par le navigateur et obligatoire
    selector: "#email"
    attr: { type: email, required: true }
    hint: "`type=\"email\"` et l'attribut `required`, écrit seul."
  - label: un clic sur l'étiquette de la lettre coche la case
    click: "#newsletter + label"
    selector: "#newsletter:checked"
    hint: "L'étiquette n'a pas de `for` : `<label for=\"newsletter\">`."
solution: assets/contact.solution
```

Les quatre défauts avaient un point commun : la page s'affichait exactement pareil avant et après. C'est le genre de faute qu'un générateur de code laisse passer, et que seul un test (cliquer sur les étiquettes, regarder ce que reçoit le serveur) fait apparaître.

> 📖 [Votre premier formulaire (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Extensions/Forms/Your_first_form) · [L'élément label (MDN)](https://developer.mozilla.org/fr/docs/Web/HTML/Element/label) · [Les types de champ input (MDN)](https://developer.mozilla.org/fr/docs/Web/HTML/Element/input#les_différents_types_de_champs_input) · [Envoyer les données d'un formulaire (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Extensions/Forms/Sending_and_retrieving_form_data)

## Trois questions pour vérifier

Trois situations tirées des formulaires de ce contenu : choisis la réponse, l'explication suit.

```quiz
title: "Les formulaires HTML"
tracksProgress: false
showNotice: false
place: stage
questions:
  - prompt: "Un champ a un `id` et une étiquette reliée, mais pas de `name`. Que reçoit le serveur à l'envoi ?"
    answers:
      - "La valeur du champ, sous le nom de son `id`"
      - "Rien pour ce champ : sans `name`, sa valeur n'est pas envoyée"
      - "Un message d'erreur"
    correct: 2
    explanation: "name est le nom d'envoi ; id sert seulement dans la page. Un champ sans name s'affiche, mais n'est pas envoyé."
  - prompt: "Comment vérifier qu'une étiquette est bien reliée à son champ ?"
    answers:
      - "Cliquer sur l'étiquette : le curseur doit aller dans le champ, ou la case se cocher"
      - "Regarder si l'étiquette est bien à côté du champ"
      - "Ouvrir la console : une erreur s'affiche si le lien est cassé"
    correct: 1
    explanation: "Le lien for/id ne se voit pas et ne produit aucune erreur ; le clic est le test le plus simple."
  - prompt: "Le champ e-mail a `type=\"email\"` et `required`. Le serveur peut-il se passer de vérifier l'adresse ?"
    answers:
      - "Oui : le navigateur a déjà refusé les adresses vides ou sans @"
      - "Non : une requête peut arriver au serveur sans passer par le formulaire, donc sans ces contrôles"
      - "Oui, si le formulaire utilise `method=\"post\"`"
    correct: 2
    explanation: "Les contrôles du navigateur aident le visiteur honnête ; un script écrit directement au serveur. post cache les données de l'adresse, il ne les vérifie pas."
```

## Récap

- Un **formulaire** envoie des données au serveur, à l'adresse de son `action` : chaque champ a un **`name`** (le nom d'envoi), un **`id`** (le nom dans la page) et un **`type`**.
- **`method`** dit comment elles partent : `get` les ajoute à l'adresse, `post` les met dans la requête.
- Le **`label`** est relié par son **`for`**, qui reprend exactement l'`id` du champ ; le clic sur l'étiquette le vérifie.
- **`required`** et `type="email"` font contrôler la saisie par le navigateur, sans remplacer la vérification par le serveur.

Cette page, avec son formulaire, sera lue sur un écran de `1600px` comme sur un téléphone de `360px` : c'est l'objet du bit [Le responsive design](https://byte-layers.com/fr/bits/responsive-design).

```ack
J'ai compris
```
