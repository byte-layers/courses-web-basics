---
title: "03 - Écrire le squelette d'une page, et casser ses accents"
description: "Écrire à la main une page minimale valide (doctype, lang, charset, title, h1, p), voir la différence entre title et h1, puis retirer le charset pour voir ce qu'il protège"
---

Le bit [Le squelette d'une page HTML](https://byte-layers.com/fr/bits/html-document) faisait compléter un squelette à trous. Cette fois, vous l'écrivez en entier, dans un vrai fichier, et vous voyez ce que la ligne `charset` change sur une page ouverte depuis votre disque.

![Live coding : écrire le squelette d'une page, puis retirer son charset](https://media.byte-layers.com/v/94555c1e3dd3587bdfba03df0b003b76e306144f512933f08a73982b1ee8eccd.mp4)

## 03.1 - Écrire le squelette

Créez `premiere-page.html` dans `BASICS`. Écrivez-y une page qui contient, dans l'ordre :

| Élément | Ce qu'il doit contenir |
|---|---|
| le doctype | sur la toute première ligne du fichier, rien avant |
| la balise `<html>` | la langue de la page, le français |
| le `<head>` | l'encodage UTF-8, puis un `<title>` : votre prénom ou « Mon premier site », un texte **différent** du titre de la page |
| le `<body>` | un `<h1>` dont le texte est exactement « Ma première page », puis un paragraphe qui vous présente en une phrase, avec au moins un accent |

VS Code vous aide : en tapant `<h1` puis `>`, il écrit lui-même la balise fermante. Tapez quand même chaque ligne, sans copier le squelette du bit : c'est en l'écrivant qu'on le retient.

Enregistrez, puis ouvrez la page dans le navigateur, comme à l'étape précédente. Regardez deux endroits : l'**onglet** du navigateur affiche le texte du `<title>`, la **page** affiche le `<h1>` en grand. Deux textes différents, deux endroits différents.

```verify
F=~/byte-layers/web/basics/premiere-page.html
if [ ! -f "$F" ]; then
  echo "Le fichier $F n'existe pas. Créez premiere-page.html dans le dossier BASICS, puis enregistrez."
  exit 1
fi
if ! head -n 1 "$F" | tr -d '\r' | grep -qi '^<!doctype html>$'; then
  echo "La première ligne doit être le doctype, <!DOCTYPE html>, et rien d'autre."
  exit 1
fi
T=$(tr '\n\r' '  ' < "$F")
if ! echo "$T" | grep -qi '<html[^>]*lang="fr"'; then
  echo "La balise <html> doit déclarer la langue : lang=\"fr\"."
  exit 1
fi
if ! echo "$T" | grep -qiE '<meta[^>]*charset="?utf-8'; then
  echo "Il manque l'encodage dans le <head> : <meta charset=\"utf-8\">."
  exit 1
fi
TITLE=$(echo "$T" | sed -n 's/.*<title>[[:space:]]*\([^<]*[^<[:space:]]\)[[:space:]]*<\/title>.*/\1/p')
if [ -z "$TITLE" ]; then
  echo "Il manque un <title> avec un texte, dans le <head>."
  exit 1
fi
if ! echo "$T" | grep -qE '<h1[^>]*>[[:space:]]*Ma première page[[:space:]]*</h1>'; then
  echo "Il faut un <h1> dont le texte est exactement « Ma première page »."
  exit 1
fi
if [ "$TITLE" = "Ma première page" ]; then
  echo "Le <title> et le <h1> ont le même texte : changez le <title>, pour voir qu'ils ne s'affichent pas au même endroit."
  exit 1
fi
if ! echo "$T" | grep -qE '<p[^>]*>[^<]*[éèêàçùâîôû]'; then
  echo "Il faut un paragraphe <p> qui vous présente, avec au moins un accent."
  exit 1
fi
echo "Votre squelette est complet : doctype, langue, encodage, « $TITLE » dans l'onglet et « Ma première page » dans la page."
```

```hint
Si la vérification parle du doctype alors qu'il est écrit, regardez s'il n'y a pas une ligne vide ou un commentaire au-dessus : le doctype doit être sur la ligne 1.
```

````solution
```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Mon premier site</title>
</head>
<body>
  <h1>Ma première page</h1>
  <p>Bonjour ! J'apprends à créer des pages web, et c'est ma première.</p>
</body>
</html>
```
````

## 03.2 - Retirer le charset pour voir ce qu'il protège

Supprimez la ligne `<meta charset="utf-8">`, enregistrez, rechargez la page dans le navigateur. Selon le navigateur, deux choses peuvent arriver :

- les accents cassent : « première » s'affiche `premiÃ¨re`. Le navigateur a lu les deux octets UTF-8 du `è` avec une autre table, et dessiné deux caractères ;
- les accents tiennent : le navigateur a deviné le bon encodage. Les navigateurs récents devinent souvent juste pour un fichier ouvert depuis le disque, mais pas toujours, et un serveur peut annoncer un autre encodage que celui du fichier.

Dans les deux cas, la conclusion est la même : on ne compte pas sur la devinette. Remettez la ligne, au début du `<head>`, enregistrez et rechargez : la vérification de la section précédente doit repasser.

> 📖 [Ce que contient l'en-tête d'une page (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Structuring_content/Webpage_metadata) · [Le validateur HTML du W3C, par envoi de fichier](https://validator.w3.org/#validate_by_upload)
