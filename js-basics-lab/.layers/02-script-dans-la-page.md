---
title: "02 - Brancher un script sur une page, et le placer au bon endroit"
description: "Créer index.html et script.js, ouvrir la page et lire l'erreur du script placé trop tôt, la réparer avec defer, puis ajouter une ligne au script"
---

Au bit [Où vit le JavaScript dans une page](https://byte-layers.com/fr/bits/js-in-page), vous avez réparé une page dont le script s'exécutait trop tôt. Ici, vous créez vous-même les deux fichiers, vous ouvrez la page dans votre navigateur, et vous lisez l'erreur avant de la corriger.

## 02.1 - Créer la page et son script

Cette section est un **support** : elle prépare les fichiers, en y laissant la faute exprès. Dans l'explorateur de VS Code, survolez `JS`, cliquez sur l'icône **New File… (Nouveau fichier…)**, tapez `index.html`, puis Entrée. Copiez-y ce contenu, puis enregistrez (Cmd+S sous macOS, Ctrl+S ailleurs) :

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Médiathèque</title>
  <script src="script.js"></script>
</head>
<body>
  <h1>Médiathèque</h1>
  <p id="compteur">En attente du script…</p>
</body>
</html>
```

La balise `<script>` est dans le `<head>` : c'est la faute du bit, que vous allez constater. Créez de la même façon `script.js`, à côté, avec ce contenu, puis enregistrez :

```javascript
console.log("script.js est chargé");
const compteur = document.querySelector("#compteur");
compteur.textContent = "47 emprunts aujourd'hui";
```

L'explorateur affiche maintenant deux fichiers, `index.html` et `script.js`, sans rond plein sur leurs onglets : ils sont enregistrés.

```verify
D=~/byte-layers/web/js
for f in index.html script.js; do
  if [ ! -f "$D/$f" ]; then
    echo "Il manque $f dans ~/byte-layers/web/js. Créez-le depuis l'explorateur de VS Code, puis enregistrez."
    exit 1
  fi
done
if ! grep -q 'querySelector("#compteur")' "$D/script.js"; then
  echo "script.js ne cherche pas #compteur. Recopiez les trois lignes, puis enregistrez."
  exit 1
fi
echo "Les deux fichiers sont en place."
```

## 02.2 - Ouvrir la page et lire l'erreur

Ouvrez `index.html` dans votre navigateur. Le plus simple est une commande, depuis le terminal intégré de VS Code :

| Système | Commande |
|---|---|
| macOS | `open index.html` |
| Linux | `xdg-open index.html` |
| Windows (Git Bash) | `start index.html` |

Vous pouvez aussi double-cliquer sur le fichier dans le Finder ou l'Explorateur de fichiers. La barre d'adresse commence par `file://` : le navigateur lit le fichier directement sur votre disque.

La page affiche encore « En attente du script… ». Ouvrez la console (F12) : la première ligne dit `script.js est chargé`, la seconde est une erreur rouge. Dans Chrome :

```text
Uncaught TypeError: Cannot set properties of null (setting 'textContent')
```

À droite de l'erreur, la console indique le fichier et la ligne, `script.js:3`. Notez ce numéro : **3**, la ligne qui écrit dans `compteur`, et non la ligne 2, qui l'a cherché trop tôt. Firefox dit la même chose autrement : `Uncaught TypeError: compteur is null`. Le fichier est bien chargé, sa première ligne s'exécute ; seul le moment pose problème.

## 02.3 - Réparer avec `defer`

À vous : réparez la page **sans toucher à `script.js`**, en gardant la balise dans le `<head>`. Le bit vous a donné l'attribut qui fait attendre le script jusqu'à la fin de la lecture de la page. Enregistrez, puis rechargez la page dans le navigateur (F5, ou Cmd+R sous macOS).

La page affiche « 47 emprunts aujourd'hui », et la console n'a plus d'erreur rouge.

```hint
Un seul mot à ajouter dans la balise du `<head>`, après `src="script.js"`.
```

```verify
F=~/byte-layers/web/js/index.html
if ! grep -q 'script.js' "$F"; then
  echo "index.html ne charge plus script.js. Gardez la balise <script src=\"script.js\">."
  exit 1
fi
HEAD=$(sed -n '/<head>/,/<\/head>/p' "$F")
if ! echo "$HEAD" | grep -q '<script[^>]*src="script.js"'; then
  echo "La balise <script> n'est plus dans le <head>. Remettez-la dans le <head>, avec l'attribut qui la fait attendre."
  exit 1
fi
if ! echo "$HEAD" | grep -q '<script[^>]*defer'; then
  echo "La balise <script> du <head> n'a pas encore l'attribut defer : <script src=\"script.js\" defer></script>. Enregistrez, puis rechargez."
  exit 1
fi
echo "Le script attend la fin de la page : il trouve #compteur."
```

```solution
`<script src="script.js" defer></script>`, dans le `<head>`. Placer la balise juste avant `</body>` marche aussi, mais la consigne de cette section demande de la garder dans le `<head>`.
```

> 🔍 **Comprendre la vérification.** Elle extrait les lignes de `index.html` comprises entre `<head>` et `</head>`, puis y cherche la balise `<script>` et son attribut `defer`. Elle ne lit que le fichier : la page, c'est vous qui la regardez.

## 02.4 - Ajouter une ligne au script

Maintenant que le script trouve les éléments de la page, faites-lui en changer un second : ajoutez à la fin de `script.js` deux lignes qui remplacent le texte du titre `h1` par « Médiathèque des Trois Rivières ». Même schéma que les lignes 2 et 3 : chercher, puis écrire. Enregistrez, rechargez la page : le titre a changé.

```verify
F=~/byte-layers/web/js/script.js
if ! grep -q 'querySelector("h1")\|querySelector('"'"'h1'"'"')' "$F"; then
  echo "script.js ne cherche pas encore le titre h1 avec document.querySelector(\"h1\")."
  exit 1
fi
if ! grep -q 'Médiathèque des Trois Rivières' "$F"; then
  echo "Le texte « Médiathèque des Trois Rivières » n'est pas dans script.js."
  exit 1
fi
echo "Le script change le compteur et le titre."
```

````solution
```javascript
const titre = document.querySelector("h1");
titre.textContent = "Médiathèque des Trois Rivières";
```
````

Ouvrez le code source de la page (clic droit, **Afficher le code source de la page**) : il dit toujours « Médiathèque » et « En attente du script… ». Le script a changé ce que le navigateur affiche, pas votre fichier.

> 📖 [L'élément script (MDN)](https://developer.mozilla.org/fr/docs/Web/HTML/Reference/Elements/script)
