---
title: "01 - Lire les requêtes d'une page dans l'onglet Réseau"
description: "Créer le dossier du lab, ouvrir les outils de développement, voir la requête d'une page et ses codes de statut 200, 404 et 301, et noter ce qu'on a vu dans notes.txt"
---

Le bit [Le web : une adresse, une requête, une page](https://byte-layers.com/fr/bits/web-request-response) décrivait la requête et la réponse HTTP. Votre navigateur les montre, toutes, dans ses **outils de développement** : vous allez les lire sur un vrai site, et noter ce que vous voyez dans un fichier.

## 01.1 - Créer le dossier du lab

Cette étape est un support : elle prépare le dossier où vivront tous vos fichiers. La commande `mkdir -p` crée le dossier `basics`, et avec lui les dossiers `byte-layers` et `web` s'ils n'existent pas encore. Si vous préférez, créez ces trois dossiers à la main dans l'explorateur de fichiers (le Finder sous macOS) : `byte-layers` dans votre dossier personnel, `web` dedans, puis `basics` dans `web`. Le résultat est le même.

```exec "Créer le dossier du lab"
mkdir -p ~/byte-layers/web/basics
```

Ouvrez ce dossier dans VS Code, comme au lab sur votre poste de développeur : menu **File (Fichier)**, **Open Folder… (Ouvrir le dossier…)**, puis allez dans le dossier en tapant son chemin :

| Système | Aller dans le dossier |
|---|---|
| macOS | Cmd+Maj+G, tapez `~/byte-layers/web/basics`, Entrée, puis **Ouvrir** |
| Windows | cliquez dans la barre d'adresse, tapez `%USERPROFILE%\byte-layers\web\basics`, Entrée, puis **Sélectionner un dossier** |
| Linux | Ctrl+L, tapez `~/byte-layers/web/basics`, Entrée, puis **Ouvrir** |

L'explorateur de VS Code affiche `BASICS`, vide pour l'instant.

## 01.2 - Ouvrir l'onglet Réseau

Dans votre navigateur, ouvrez la page d'accueil de MDN, la documentation du web que citent tous les bits de ce cours : `https://developer.mozilla.org/fr/`.

Ouvrez ensuite les outils de développement : **F12**, ou Cmd+Option+I sous macOS, Ctrl+Maj+I ailleurs. Un panneau s'ouvre, en bas ou à droite de la page. Cliquez sur son onglet **Réseau** (*Network* si votre navigateur est en anglais). Il est vide : il n'enregistre les requêtes qu'une fois ouvert. Rechargez la page.

Des lignes apparaissent, une par requête. Chaque colonne répond à une question :

| Colonne | Ce qu'elle dit |
|---|---|
| **Nom** (*Name*) ou **Fichier** | le chemin demandé |
| **État** (*Status*) | le code de statut de la réponse |
| **Type** | ce que contient la réponse : `document` pour le HTML, `stylesheet` pour le CSS, `script`, `png`, `svg`… |
| **Taille** (*Size*) | le poids de la réponse |

La toute première ligne, de type `document`, est la page elle-même : c'est la requête décrite dans le bit. Toutes les autres sont venues ensuite, parce que le navigateur a trouvé leurs adresses dans ce HTML. En bas du panneau, une ligne donne le nombre total de requêtes.

Cliquez sur la première ligne : un volet affiche les **en-têtes** (*Headers*) de la requête et de la réponse. Vous y retrouvez la méthode `GET`, le code de statut et l'en-tête `content-type: text/html`.

## 01.3 - Provoquer un 404, puis un 301

Gardez les outils de développement ouverts sur l'onglet Réseau, et tapez dans la barre d'adresse une page qui n'existe pas : `https://developer.mozilla.org/fr/page-qui-n-existe-pas`. MDN affiche sa page « introuvable », et la première ligne de l'onglet Réseau porte le code **404**.

Tapez maintenant `http://wikipedia.org`, avec `http` et non `https`. L'adresse change toute seule. Pour voir pourquoi, cochez **Conserver le journal** (*Preserve log*), en haut de l'onglet Réseau, puis retapez la même adresse : la première ligne porte le code **301**, la redirection, et les lignes suivantes montrent le navigateur qui suit la nouvelle adresse. Sans cette case, l'onglet se vide à chaque changement de page, et la ligne du 301 disparaît aussitôt.

## 01.4 - Noter ce que vous avez vu

Dans VS Code, créez un fichier `notes.txt` dans le dossier `BASICS` : survolez le nom du dossier dans l'explorateur, cliquez sur l'icône **New File… (Nouveau fichier…)**, tapez `notes.txt`, puis Entrée. Écrivez-y ces quatre lignes, en remplaçant chaque `…` par ce que vous avez lu dans l'onglet Réseau, puis enregistrez :

```text
page=…
introuvable=…
redirection=…
requetes=…
```

| Ligne | Ce qu'on y écrit |
|---|---|
| `page=` | le code de statut de la première requête de la page d'accueil de MDN |
| `introuvable=` | le code de la page qui n'existe pas |
| `redirection=` | le code de la première requête vers `http://wikipedia.org` |
| `requetes=` | le nombre total de requêtes de la page d'accueil de MDN, lu en bas du panneau ; il varie d'un chargement à l'autre, tout nombre lu convient |

```verify
F=~/byte-layers/web/basics/notes.txt
if [ ! -f "$F" ]; then
  echo "Le fichier $F n'existe pas. Créez notes.txt dans le dossier BASICS de VS Code, puis enregistrez."
  exit 1
fi
v() { sed -n "s/^$1[[:space:]]*=//p" "$F" | tail -1 | tr -d '[:space:]'; }
if [ "$(v page)" != 200 ]; then
  echo "La ligne page= doit donner le code de statut de la première requête de MDN : la page existe, la voici."
  exit 1
fi
if [ "$(v introuvable)" != 404 ]; then
  echo "La ligne introuvable= doit donner le code de la page qui n'existe pas."
  exit 1
fi
if [ "$(v redirection)" != 301 ]; then
  echo "La ligne redirection= doit donner le code de la première requête vers http://wikipedia.org. Cochez Conserver le journal pour la voir."
  exit 1
fi
R=$(v requetes)
case "$R" in
  ''|*[!0-9]*) echo "La ligne requetes= doit contenir un nombre, sans texte autour."; exit 1 ;;
esac
if [ "$R" -lt 2 ]; then
  echo "Une page de MDN déclenche bien plus d'une requête : relisez le total en bas de l'onglet Réseau, après avoir rechargé la page."
  exit 1
fi
echo "Vos notes sont justes : 200, 404, 301, et $R requêtes pour une seule page."
```

```hint
Si la vérification échoue alors que les lignes vous semblent justes, regardez l'onglet `notes.txt` : un rond plein veut dire que le fichier n'est pas enregistré. Chaque ligne commence par le mot, sans espace avant, puis `=` et le nombre.
```

> 📖 [Les outils de développement du navigateur (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Howto/Tools_and_setup/What_are_browser_developer_tools) · [L'onglet Réseau de Chrome (en anglais)](https://developer.chrome.com/docs/devtools/network) · [L'onglet Réseau de Firefox (en anglais)](https://firefox-source-docs.mozilla.org/devtools-user/network_monitor/)
