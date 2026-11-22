---
title: "02 - Retirer le CSS, puis le JavaScript, d'une page"
description: "Bloquer la feuille de style et désactiver le JavaScript d'un vrai site dans les outils de développement, puis créer une page en trois fichiers sur sa machine, l'ouvrir depuis le disque et retirer à la main son link et son script"
---

Le bit [Une page web : HTML, CSS et JavaScript](https://byte-layers.com/fr/bits/web-page-languages) partageait une page entre trois langages. Pour voir ce que fait chacun, le plus parlant est de les retirer un par un : d'abord sur un vrai site, avec les outils de développement, puis sur une page que vous créez.

## 02.1 - Retirer le CSS et le JavaScript d'un vrai site

Ouvrez un site que vous aimez bien, un site d'information par exemple, et ouvrez les outils de développement (F12). Les menus diffèrent selon le navigateur :

| Pour retirer | Chrome et Edge | Firefox |
|---|---|---|
| le CSS | onglet **Réseau**, rechargez, filtre **CSS** ; clic droit sur une ligne, **Bloquer l'URL de la requête** (*Block request URL*), pour chaque feuille de style, puis rechargez | menu **Affichage**, **Style de la page**, **Aucun style** (sous Windows, appuyez sur Alt pour voir la barre de menus) |
| le JavaScript | dans les outils, Cmd+Maj+P ou Ctrl+Maj+P, tapez `JavaScript`, choisissez **Désactiver JavaScript** (*Disable JavaScript*), puis rechargez | pas de bouton simple : faites la section suivante, sur votre propre page |

Sans le CSS, la page devient une longue colonne de texte noir sur fond blanc, avec des liens bleus soulignés et des images à leur taille d'origine : il ne reste que le HTML, avec l'apparence par défaut du navigateur. Tout le contenu est là, dans l'ordre où le HTML l'écrit. Sans le JavaScript, la page s'affiche souvent presque normalement, mais les menus déroulants, les carrousels ou les boutons « voir plus » ne réagissent plus ; certains sites, construits entièrement en JavaScript, n'affichent plus rien du tout.

Remettez tout en place : dans Chrome et Edge, la case **Activer le blocage des requêtes** (*Enable request blocking*) de l'onglet du même nom se décoche, et le JavaScript se réactive avec la même commande, **Activer JavaScript**. Il se réactive aussi tout seul à la fermeture des outils de développement.

## 02.2 - Créer une page en trois fichiers

On refait l'expérience sur une page à vous, pour voir les balises qui relient les fichiers. Cette section est un support : elle crée la page, que vous n'avez pas à écrire vous-même. Dans VS Code, créez trois fichiers dans `BASICS`, et collez dans chacun le contenu ci-dessous. Le premier, `trois-langages.html`, contient la page :

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Trois langages</title>
  <link rel="stylesheet" href="trois-langages.css">
</head>
<body>
  <h1 id="titre">Bonjour !</h1>
  <p>Cette page parle trois langages.</p>
  <button type="button" id="bouton">Clique-moi</button>
  <script src="trois-langages.js"></script>
</body>
</html>
```

Le deuxième, `trois-langages.css`, donne au bouton sa couleur :

```css
#bouton {
  background-color: rgb(219, 39, 119);
  color: white;
  border: none;
  padding: 8px 16px;
}
```

Le troisième, `trois-langages.js`, change le titre au clic :

```javascript
document.querySelector('#bouton').addEventListener('click', function () {
  document.querySelector('#titre').textContent = 'Merci !';
});
```

Enregistrez les trois. Ouvrez ensuite la page dans le navigateur : dans l'explorateur de VS Code, clic droit sur `trois-langages.html`, **Reveal in Finder (Afficher dans le Finder)** sous macOS, **Reveal in File Explorer (Afficher dans l'Explorateur de fichiers)** sous Windows, puis double-clic sur le fichier. Le bouton est rose, et un clic change le titre en « Merci ! ».

```verify
D=~/byte-layers/web/basics
for f in trois-langages.html trois-langages.css trois-langages.js; do
  if [ ! -f "$D/$f" ]; then
    echo "Il manque $f dans $D. Créez-le dans VS Code, collez son contenu, puis enregistrez."
    exit 1
  fi
done
if ! grep -q 'background-color' "$D/trois-langages.css"; then
  echo "trois-langages.css ne contient pas la règle du bouton : collez-la, puis enregistrez."
  exit 1
fi
if ! grep -q 'addEventListener' "$D/trois-langages.js"; then
  echo "trois-langages.js ne contient pas le script : collez-le, puis enregistrez."
  exit 1
fi
echo "Les trois fichiers de la page sont en place."
```

## 02.3 - Une page ouverte depuis le disque

Regardez la barre d'adresse : elle commence par `file://`, suivi du chemin du fichier sur votre disque. Ouvrez l'onglet Réseau et rechargez : les trois fichiers y sont, mais aucun ne porte de code comme 200 ou 404. Aucun serveur n'a répondu : le navigateur a lu les fichiers directement sur le disque, comme le décrit le bit sur le web.

> 💡 **Remarque.** Si vous avez installé l'extension **Live Preview** de VS Code (éditeur Microsoft), clic droit sur `trois-langages.html`, **Show Preview** : la page s'ouvre par un petit serveur, à une adresse comme `http://127.0.0.1:3000/trois-langages.html`, et elle se recharge seule à chaque enregistrement. Dans un navigateur, à cette adresse, l'onglet Réseau montre alors de vrais codes 200. Elle n'est pas obligatoire pour ce lab.

## 02.4 - Retirer le link, puis le script

Dans `trois-langages.html`, transformez la ligne du `<link>` en commentaire, pour que le navigateur l'ignore : placez le curseur sur la ligne et tapez Cmd+/ sous macOS, Ctrl+/ ailleurs. VS Code l'entoure de `<!--` et `-->`. Enregistrez, rechargez : le bouton redevient gris, le bouton par défaut du navigateur. Cliquez dessus : le titre change quand même, le JavaScript ne dépend pas du CSS.

Refaites le même raccourci sur la ligne du `<link>` pour la rétablir, puis faites de même avec la ligne du `<script>`. Enregistrez, rechargez : le bouton est rose, mais le clic ne fait plus rien. Rétablissez enfin la ligne du `<script>`, enregistrez, et vérifiez que tout remarche.

Aucune erreur ne s'est affichée dans la page, ni sans le CSS ni sans le JavaScript : une page qui perd un fichier ne vous prévient pas.

```verify
F=~/byte-layers/web/basics/trois-langages.html
if [ ! -f "$F" ]; then
  echo "Le fichier $F n'existe pas : refaites la section 02.2."
  exit 1
fi
T=$(grep -v '<!--' "$F")
if ! echo "$T" | grep -q '<link rel="stylesheet" href="trois-langages.css">'; then
  echo "La ligne du <link> est absente ou encore en commentaire : rétablissez-la, puis enregistrez."
  exit 1
fi
if ! echo "$T" | grep -q '<script src="trois-langages.js"></script>'; then
  echo "La ligne du <script> est absente ou encore en commentaire : rétablissez-la, puis enregistrez."
  exit 1
fi
echo "Le link et le script sont rétablis : la page a retrouvé son style et son comportement."
```

> 📖 [Bloquer des requêtes dans Chrome (en anglais)](https://developer.chrome.com/docs/devtools/network/reference#block) · [Désactiver JavaScript dans Chrome (en anglais)](https://developer.chrome.com/docs/devtools/javascript/disable) · [Live Preview (en anglais)](https://marketplace.visualstudio.com/items?itemName=ms-vscode.live-server)
