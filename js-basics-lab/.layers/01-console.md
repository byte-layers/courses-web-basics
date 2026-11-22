---
title: "01 - Parler au navigateur dans sa console"
description: "Ouvrir la console sur une page vide, y afficher des boîtes de dialogue, retrouver le piège de prompt qui rend du texte, puis créer le dossier du lab"
---

Au bit [La console JavaScript](https://byte-layers.com/fr/bits/js-console), vous tapiez dans la console d'un aperçu. Cette fois, c'est celle de votre navigateur, sur une page vide, avec les boîtes de dialogue que l'aperçu ne pouvait pas vous montrer.

## 01.1 - Ouvrir la console sur une page vide

Ouvrez un nouvel onglet, tapez `about:blank` dans la barre d'adresse, puis Entrée : une page blanche s'affiche, faite pour les essais. Ouvrez la console :

| Navigateur | Raccourci |
|---|---|
| Chrome, Edge | F12, puis l'onglet **Console** ; ou Ctrl+Maj+J (Cmd+Option+J sous macOS) |
| Firefox | F12, puis l'onglet **Console** ; ou Ctrl+Maj+K (Cmd+Option+K sous macOS) |
| Safari | dans **Réglages**, onglet **Avancés**, cochez « Afficher les fonctionnalités pour les développeurs web », puis Cmd+Option+C |

Cliquez dans la zone de saisie, en bas de la console. Tapez `2 + 3`, puis Entrée : la console répond `5`.

> ⚠️ **Coller du code dans la console.** Chrome et Edge refusent qu'on colle du code dans la console tant qu'on n'a pas tapé soi-même `allow pasting` (ou « autoriser le collage »), pour protéger des arnaques qui font coller du code inconnu. Ici, tapez vos instructions plutôt que de les coller : c'est aussi la meilleure façon de les retenir.

## 01.2 - Afficher des boîtes de dialogue

Le navigateur sait ouvrir trois boîtes de dialogue, qui interrompent la page jusqu'à ce qu'on réponde. Tapez ces instructions une par une, et répondez à chaque boîte :

```javascript
alert("Bienvenue à la médiathèque !");
```

La boîte affiche le message ; cliquez sur OK. La deuxième pose une question, et range la réponse dans une variable :

```javascript
let reponse = confirm("Voulez-vous recevoir la newsletter ?");
```

La console répond `undefined` : une déclaration avec `let` ne rend pas de valeur. Tapez maintenant `reponse`, puis Entrée : vous lisez `true` si vous avez cliqué sur OK, `false` si vous avez cliqué sur Annuler.

| Fonction | La boîte | Ce qu'elle rend |
|---|---|---|
| `alert(message)` | un message et un bouton OK | rien (`undefined`) |
| `confirm(question)` | une question, OK et Annuler | `true` ou `false` |
| `prompt(question)` | une question et un champ de saisie | le texte tapé, ou `null` si l'on annule |

Contrairement à la console de l'aperçu, celle du navigateur garde vos variables d'une ligne à l'autre, jusqu'au rechargement de la page.

## 01.3 - Retrouver le piège de `prompt`

Demandez un âge, et répondez **25** :

```javascript
let age = prompt("Quel âge avez-vous ?");
```

Puis tapez ces trois lignes, une par une, et comparez avec la réponse attendue :

| Vous tapez | La console répond |
|---|---|
| `age + 1` | `'251'` |
| `typeof age` | `'string'` |
| `Number(age) + 1` | `26` |

`prompt` rend toujours du texte, et le `+` colle le `1` au bout : c'est le piège du bit, cette fois avec une vraie saisie. Les guillemets autour de `'251'` signalent un texte ; un nombre s'affiche sans.

Si vous retapez `let age = …`, la console répond `SyntaxError: Identifier 'age' has already been declared` : on ne déclare pas deux fois le même nom. Pour repartir de zéro, rechargez la page (F5, ou Cmd+R sous macOS), qui efface toutes les variables.

## 01.4 - Calculer avec `Math`

Gardez votre `age` et comparez-le à ceux de Paul, 15 ans, et de Pierre, 21 ans. `Math.abs` rend la valeur absolue d'un nombre, c'est-à-dire l'écart sans le signe :

```javascript
console.log("Écart avec Paul :", Math.abs(Number(age) - 15));
```

Avec 25, la console écrit `Écart avec Paul : 10`. Écrivez vous-même la ligne pour Pierre : elle doit afficher `Écart avec Pierre : 4`. Puis tirez un dé : `Math.floor(Math.random() * 6) + 1` rend un entier entre 1 et 6, différent à chaque fois. Tapez-la plusieurs fois.

| Morceau | Rôle |
|---|---|
| `Math.random()` | un nombre au hasard, de 0 inclus à 1 exclu, par exemple `0.734` |
| `* 6` | étale ce nombre de 0 à 6 exclu : `4.404` |
| `Math.floor(…)` | garde la partie entière, en arrondissant vers le bas : `4` ; on obtient donc 0 à 5 |
| `+ 1` | décale : 1 à 6 |

Vous retrouverez cette formule à l'étape 03, pour tirer le nombre secret du jeu.

## 01.5 - Créer le dossier du lab et l'ouvrir dans VS Code

Ce que vous avez tapé disparaîtra au prochain rechargement. Les étapes suivantes écrivent du code dans des fichiers : ils ont besoin d'un dossier. Dans un terminal (Git Bash sous Windows), créez-le :

```exec "Créer le dossier du lab"
mkdir -p ~/byte-layers/web/js
```

`mkdir` crée un dossier ; `-p` crée aussi les dossiers parents qui manquent (`web`, et même `byte-layers` si c'est votre premier lab), et ne dit rien si le dossier existe déjà.

Ouvrez ensuite ce dossier dans VS Code : menu **File (Fichier)**, **Open Folder… (Ouvrir le dossier…)**, puis allez dans `~/byte-layers/web/js`, comme au lab « Votre poste de développeur ». L'explorateur affiche `JS`, vide pour l'instant.

```verify
if [ ! -d ~/byte-layers/web/js ]; then
  echo "Le dossier ~/byte-layers/web/js n'existe pas. Lancez mkdir -p ~/byte-layers/web/js dans un terminal."
  exit 1
fi
echo "Le dossier du lab est prêt."
```

> 📖 [Les boîtes de dialogue : alert, confirm et prompt (MDN)](https://developer.mozilla.org/fr/docs/Web/API/Window/prompt) · [Math.random (MDN)](https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Global_Objects/Math/random)
