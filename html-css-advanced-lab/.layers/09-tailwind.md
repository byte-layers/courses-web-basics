---
title: "09 - Installer Tailwind et lancer son traitement"
description: "Créer un petit projet npm, installer Tailwind en version épinglée, lancer le traitement, lire le CSS produit, constater qu'une classe ajoutée après coup ne fait rien et qu'une classe retirée disparaît, puis garder le traitement en surveillance"
---

Avec Bootstrap, vous avez chargé un CSS tout fait. Tailwind, lui, **fabrique** le CSS à partir des classes de vos fichiers. Vous l'installez sur votre machine, vous lancez le traitement, et vous regardez ce qu'il produit, y compris quand il n'a pas tourné.

Cette étape utilise **Node.js** et sa commande **`npm`**, installés par le lab [Votre poste de développeur](https://byte-layers.com/fr/labs/dev-setup-lab). Vérifiez-le dans le terminal intégré de VS Code : `node --version` doit afficher un numéro de version.

## 09.1 - Un dossier et un projet npm

Tailwind vit dans un sous-dossier à part, pour ne pas mélanger ses fichiers avec ceux de la page des étapes précédentes. Créez-le :

```exec "Créer le dossier tailwind"
mkdir -p ~/byte-layers/web/advanced/tailwind
```

Puis placez le terminal dedans avec `cd` : toutes les commandes de cette étape se lancent depuis ce dossier.

```exec "Se placer dans le dossier"
cd ~/byte-layers/web/advanced/tailwind
```

Un projet JavaScript se décrit dans un fichier `package.json` : son nom, et la liste des paquets dont il a besoin. La commande `npm init` le crée ; l'option `-y` accepte toutes les réponses par défaut au lieu de poser des questions.

```exec "Créer package.json"
npm init -y
```

## 09.2 - Installer Tailwind, en version épinglée

**npm** (*Node package manager*) télécharge des paquets depuis le registre public de npm. Tailwind en a deux : `tailwindcss`, le moteur, et `@tailwindcss/cli`, la commande qui le lance. Le `@4.3.5` après chaque nom **épingle la version** : celle avec laquelle ce lab a été vérifié. Sans lui, npm installerait la dernière version parue, qui peut changer de comportement.

```exec "Installer Tailwind 4.3.5"
npm install tailwindcss@4.3.5 @tailwindcss/cli@4.3.5
```

L'installation prend quelques secondes, puis se termine par une ligne comme celle-ci :

```text
found 0 vulnerabilities
```

Le dossier contient maintenant `node_modules`, où sont rangés les paquets et ceux dont ils dépendent, et `package-lock.json`, qui note la version exacte de chacun pour qu'une autre machine installe exactement les mêmes. Ni l'un ni l'autre ne s'ouvre à la main.

```verify
P=~/byte-layers/web/advanced/tailwind/node_modules/tailwindcss/package.json
[ -f "$P" ] || { echo "Tailwind n'est pas installé dans ~/byte-layers/web/advanced/tailwind. Placez le terminal dans ce dossier (cd), puis relancez npm install."; exit 1; }
grep -q '"version": "4.3.5"' "$P" || { echo "La version installée n'est pas 4.3.5 : relancez npm install tailwindcss@4.3.5 @tailwindcss/cli@4.3.5."; exit 1; }
[ -f ~/byte-layers/web/advanced/tailwind/node_modules/@tailwindcss/cli/package.json ] || { echo "Le paquet @tailwindcss/cli manque : relancez la commande d'installation."; exit 1; }
echo "Tailwind 4.3.5 et sa commande sont installés."
```

## 09.3 - Le fichier d'entrée et la page

Dans l'explorateur de VS Code, ouvrez le dossier `tailwind` et créez-y deux fichiers. Le premier, `input.css`, est le **fichier d'entrée** du traitement ; il tient en une ligne :

```css
@import "tailwindcss";
```

Le second, `index.html`, est une petite page habillée seulement avec des classes de Tailwind. Elle charge **`output.css`**, le fichier que le traitement va produire, et qui n'existe pas encore :

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Camille Martin, version Tailwind</title>
  <link rel="stylesheet" href="output.css">
</head>
<body class="p-8 font-sans text-slate-800">
  <h1 class="text-3xl font-bold">Camille Martin</h1>
  <p class="mt-2 text-lg">Développeuse web à Toulouse.</p>
  <a class="mt-4 inline-block rounded-lg bg-blue-700 px-4 py-2 text-white" href="#contact">Me contacter</a>
</body>
</html>
```

Enregistrez les deux fichiers et ouvrez `index.html` dans le navigateur : la page n'a aucun style. Les classes sont là, mais aucune feuille ne les définit encore.

## 09.4 - Lancer le traitement et lire le CSS produit

**`npx`** lance une commande fournie par un paquet installé dans le projet, ici celle de `@tailwindcss/cli`. L'option `-i` donne le fichier d'entrée, `-o` le fichier à produire :

```exec "Lancer le traitement de Tailwind"
npx @tailwindcss/cli -i input.css -o output.css
```

Le traitement dure quelques millisecondes :

```text
≈ tailwindcss v4.3.5

Done in 19ms
```

Rechargez la page : le titre est grand et gras, le bouton bleu. Ouvrez `output.css` dans VS Code. Après la remise à zéro des styles du navigateur, environ 170 lignes, vous trouvez les règles de **vos** classes, et seulement elles : `.text-3xl`, `.bg-blue-700`, `.px-4`… Pour compter les lignes qui citent une classe, `grep -c` affiche un nombre :

```exec "Chercher bg-blue-700 dans le CSS produit"
grep -c "bg-blue-700" output.css
```

Le terminal affiche `1` : la règle `.bg-blue-700` est dans le fichier.

## 09.5 - Une classe ajoutée après le traitement

Ajoutez la classe `uppercase` au titre, dans `index.html` : `<h1 class="text-3xl font-bold uppercase">`. Elle doit l'écrire en majuscules. Enregistrez, rechargez la page.

Le titre n'est pas en majuscules, et rien ne dit pourquoi. Cherchez la classe dans le CSS produit :

```exec "Chercher uppercase dans le CSS produit"
grep -c "uppercase" output.css
```

Le terminal affiche `0` : `output.css` a été produit **avant** que vous écriviez `uppercase`. Relancez le traitement, puis rechargez la page :

```exec "Relancer le traitement"
npx @tailwindcss/cli -i input.css -o output.css
```

Le titre est en majuscules. C'est le piège du bit sur Tailwind : le CSS produit est une photographie de vos classes au moment du traitement.

## 09.6 - Une classe retirée disparaît du CSS produit

Dans `index.html`, remplacez `bg-blue-700` par `bg-pink-600` sur le bouton, enregistrez, puis relancez le traitement :

```exec "Relancer le traitement après le changement"
npx @tailwindcss/cli -i input.css -o output.css
```

Le bouton est rose. Cherchez l'ancienne classe :

```exec "Chercher bg-blue-700 de nouveau"
grep -c "bg-blue-700" output.css
```

Le terminal affiche `0` : plus aucune balise n'utilise `bg-blue-700`, alors le traitement ne l'a pas écrite. C'est ce qui garde le fichier léger : quelques kilo-octets, contre `230 Ko` pour Bootstrap.

```verify
D=~/byte-layers/web/advanced/tailwind
[ -f "$D/output.css" ] || { echo "Il n'y a pas encore de output.css : lancez le traitement depuis le dossier tailwind."; exit 1; }
grep -q 'uppercase' "$D/index.html" || { echo "Le titre de index.html n'a pas encore la classe uppercase."; exit 1; }
grep -q 'bg-pink-600' "$D/index.html" || { echo "Le bouton de index.html n'a pas encore la classe bg-pink-600."; exit 1; }
grep -q 'bg-blue-700' "$D/index.html" && { echo "Le bouton a encore la classe bg-blue-700 : remplacez-la par bg-pink-600."; exit 1; }
grep -q '\.uppercase' "$D/output.css" || { echo "output.css n'a pas la règle .uppercase : relancez le traitement."; exit 1; }
grep -q '\.bg-pink-600' "$D/output.css" || { echo "output.css n'a pas la règle .bg-pink-600 : relancez le traitement après avoir enregistré index.html."; exit 1; }
grep -q '\.bg-blue-700' "$D/output.css" && { echo "output.css contient encore .bg-blue-700 : relancez le traitement après avoir enregistré index.html."; exit 1; }
echo "Le CSS produit contient exactement les classes de la page."
```

```hint
Si `output.css` ne change pas, vérifiez que le terminal est bien dans le dossier `tailwind` : la commande `pwd` affiche le dossier courant, qui doit finir par `/web/advanced/tailwind`.
```

## 09.7 - Le traitement en surveillance

Relancer la commande à chaque modification devient vite pénible. Avec l'option **`--watch`**, le traitement ne s'arrête pas : il surveille vos fichiers et réécrit `output.css` à chaque enregistrement.

```exec "Lancer le traitement en surveillance"
npx @tailwindcss/cli -i input.css -o output.css --watch
```

Ajoutez `italic` au paragraphe, enregistrez, rechargez : il est en italique, sans rien relancer. Le terminal reste occupé tant que la surveillance tourne ; arrêtez-la avec Ctrl+C quand vous avez fini.

Dans un vrai projet, ce traitement est souvent confié à un outil de build, Vite par exemple, qui le lance avec le reste. L'idée ne change pas : ce que reçoit le navigateur est fabriqué à partir de ce que vous écrivez.

> 📖 [Tailwind CSS, installation avec la CLI (en anglais)](https://tailwindcss.com/docs/installation/tailwind-cli) · [Comment Tailwind détecte les classes (en anglais)](https://tailwindcss.com/docs/detecting-classes-in-source-files) · [npm install (en anglais)](https://docs.npmjs.com/cli/commands/npm-install) · [npx (en anglais)](https://docs.npmjs.com/cli/commands/npx)

## Récap

- Le **flux normal** empile les blocs ; **Flexbox** aligne sur une ligne, **Grid** sur des lignes et des colonnes, et l'on choisit pour chaque conteneur.
- Un **formulaire** n'envoie que les champs qui ont un **`name`**, et chaque étiquette se relie par **`for`** et **`id`** ; `method="get"` montre l'envoi dans l'adresse.
- Une page **adaptative** a sa **meta viewport**, des **`max-width`** et des media queries **mobile-first** ; le test décisif va de 360 à 1600 px.
- **Lighthouse** trouve une partie des erreurs d'accessibilité, la **grille RGAA** et le clavier trouvent le reste.
- Les **variables CSS** gardent le thème au même endroit ; les **transitions** se déclarent sur l'état normal ; **`prefers-reduced-motion`** coupe le mouvement sur demande.
- **Bootstrap** fournit un CSS tout fait ; **Tailwind** fabrique le CSS à partir de vos classes, et une classe ajoutée après le traitement ne fait rien.

Vous avez tout ce qu'il faut pour reprendre votre propre portfolio et le rendre adaptatif, accessible, avec un formulaire de contact : c'est le challenge [Mon portfolio v2](https://byte-layers.com/fr/challenges/portfolio-v2-challenge).
