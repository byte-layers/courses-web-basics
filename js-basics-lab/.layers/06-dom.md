---
title: "06 - Lire un vrai site, puis construire une liste avec le DOM"
description: "Interroger le DOM d'un site réel dans la console avec querySelector et querySelectorAll, puis écrire catalogue.js, qui construit une liste de livres à partir d'un tableau de données"
---

Au bit [Le DOM : la page vue par JavaScript](https://byte-layers.com/fr/bits/dom), les pages étaient petites et faites pour l'exercice. Ici, vous interrogez d'abord le DOM d'un vrai site, dans la console, puis vous écrivez un script qui construit une page à partir de données.

## 06.1 - Interroger le DOM d'un vrai site

Ouvrez la page d'accueil de [MDN en français](https://developer.mozilla.org/fr/), puis sa console (F12). Tapez ces instructions une par une, et lisez chaque réponse :

| Vous tapez | La console répond |
|---|---|
| `document.querySelector("h1")` | le premier titre `h1` de la page ; survolez-le dans la console, il s'éclaire dans la page |
| `document.querySelector("a")` | le **premier** lien seulement |
| `document.querySelectorAll("a").length` | le nombre de liens de la page, plusieurs dizaines |
| `document.querySelector(".nexiste-pas")` | `null` : aucun élément n'a cette classe |
| `document.querySelectorAll(".nexiste-pas").length` | `0` : une liste vide, pas `null` |
| `Array.isArray(document.querySelectorAll("a"))` | `false` : une `NodeList` n'est pas un tableau |

Puis changez un texte, pour voir que le DOM se modifie en direct :

```javascript
document.querySelector("h1").textContent = "Bonjour depuis la console";
```

Le titre change dans la page. Rechargez : il revient. Vous avez modifié le DOM affiché dans votre onglet, pas le site, ni ses fichiers sur le serveur. Les pages changent selon les versions du site : si `h1` ne trouve rien, essayez `"h2"`.

## 06.2 - Créer la page du catalogue

Cette section est un **support**. Créez `catalogue.html` dans le dossier du lab, avec ce contenu, puis enregistrez. La liste `#catalogue` est vide : c'est votre script qui la remplira. La classe `volumineux` existe dans le CSS, sans être posée sur rien.

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Catalogue</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 600px; margin: 2rem auto; }
    #catalogue li { padding: 0.5rem; margin: 0.25rem 0; border: 1px solid #cbd5e1; }
    #catalogue li.volumineux { background-color: #fef3c7; }
  </style>
  <script src="catalogue.js" defer></script>
</head>
<body>
  <h1>Catalogue de la médiathèque</h1>
  <p id="compteur">— livres</p>
  <ul id="catalogue"></ul>
</body>
</html>
```

Créez ensuite `catalogue.js`, avec les données de départ :

```javascript
const livres = [
  { titre: "La Horde du Contrevent", pages: 712 },
  { titre: "Dune", pages: 900 },
  { titre: "Fondation", pages: 420 },
  { titre: "Le Nom du vent", pages: 850 },
  { titre: "Les Fourmis", pages: 300 }
];
```

## 06.3 - Construire la liste à partir des données

À vous : complétez `catalogue.js` pour que la page respecte ces critères.

- La liste `#catalogue` contient **une ligne par livre**, dans l'ordre du tableau, de la forme `Dune (900 pages)`.
- Les livres de **plus de 700 pages** portent la classe `volumineux` : leur fond devient crème. Il y en a trois.
- Le paragraphe `#compteur` affiche `5 livres, dont 3 de plus de 700 pages`, avec des nombres **calculés** : ni 5 ni 3 ne sont écrits à la main.
- Aucune couleur dans votre fichier : vous posez une classe, le CSS fait le reste.

Faites d'abord une seule ligne, en dur, jusqu'à ce qu'elle s'affiche ; entourez-la ensuite d'une boucle. Enregistrez, ouvrez `catalogue.html` dans le navigateur, et regardez : cinq lignes, trois sur fond crème, le compteur à jour.

```hint
Pour chaque livre : `document.createElement("li")`, puis `textContent`, puis `classList.add("volumineux")` si `livre.pages > 700`, puis `liste.append(li)`. Un compteur `let volumineux = 0;`, déclaré avant la boucle, compte les gros livres.
```

```hint
Le nombre total de livres, c'est `livres.length`.
```

```verify
F=~/byte-layers/web/js/catalogue.js
[ -f "$F" ] || { echo "Il n'y a pas de catalogue.js dans ~/byte-layers/web/js."; exit 1; }
[ -f ~/byte-layers/web/js/catalogue.html ] || { echo "Il n'y a pas de catalogue.html dans ~/byte-layers/web/js."; exit 1; }
if command -v node >/dev/null 2>&1 && ! node --check "$F" 2>/dev/null; then
  echo "catalogue.js contient une erreur de syntaxe :"; node --check "$F" 2>&1 | grep -m1 Error; exit 1
fi
grep -q 'createElement' "$F" || { echo "catalogue.js ne fabrique pas encore d'élément avec document.createElement(\"li\")."; exit 1; }
grep -Eq '\.(append|appendChild)\(' "$F" || { echo "Les éléments fabriqués ne sont pas insérés : il manque liste.append(li)."; exit 1; }
grep -q 'volumineux' "$F" || { echo "catalogue.js ne pose pas encore la classe volumineux."; exit 1; }
grep -q 'livres.length' "$F" || { echo "Le nombre de livres doit venir de livres.length, pas d'un 5 écrit à la main."; exit 1; }
grep -Eq '\.style\b|innerHTML' "$F" && { echo "catalogue.js écrit du style ou du HTML brut : posez des classes avec classList, créez les éléments avec createElement."; exit 1; }
grep -Eq '"5 livres|3 de plus' "$F" && { echo "Le compteur est écrit à la main : assemblez-le avec livres.length et votre compteur de gros livres."; exit 1; }
echo "catalogue.js construit la liste à partir des données."
```

````solution
```javascript
const liste = document.querySelector("#catalogue");
const compteur = document.querySelector("#compteur");

let volumineux = 0;
for (const livre of livres) {
  const li = document.createElement("li");
  li.textContent = livre.titre + " (" + livre.pages + " pages)";
  if (livre.pages > 700) {
    li.classList.add("volumineux");
    volumineux = volumineux + 1;
  }
  liste.append(li);
}

compteur.textContent = livres.length + " livres, dont " + volumineux + " de plus de 700 pages";
```
````

> 🔍 **Comprendre la vérification.** Elle relit `catalogue.js` : syntaxe valide (`node --check`), `createElement`, un `append`, la classe `volumineux`, `livres.length`, et ni style ni compteur écrit à la main. Elle ne voit pas la page : les cinq lignes et les trois fonds crème, c'est vous qui les regardez.

## 06.4 - Le code source ne change pas

Ouvrez le code source de la page (clic droit, **Afficher le code source de la page**) : la liste y est toujours vide. Ouvrez maintenant l'onglet **Éléments** des outils de développement (**Inspecteur** dans Firefox) : les cinq `<li>` y sont, trois avec `class="volumineux"`. Le premier montre le fichier, le second le DOM.

Pour finir, essayez volontairement ceci : sortez la ligne `const li = document.createElement("li");` de la boucle, en la plaçant juste avant. Enregistrez, rechargez : une seule ligne apparaît, celle du dernier livre. `append` ne copie pas, il **déplace** : le même élément a été rempli et déplacé cinq fois. Remettez la ligne dans la boucle.

> 📖 [Introduction au DOM (MDN)](https://developer.mozilla.org/fr/docs/Web/API/Document_Object_Model/Introduction) · [Element.append (MDN)](https://developer.mozilla.org/fr/docs/Web/API/Element/append)
