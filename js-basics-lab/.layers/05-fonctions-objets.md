---
title: "05 - Des fonctions, des objets et une classe, lancés avec Node.js"
description: "Écrire formes.js : une fonction qui rend son résultat, un objet et un tableau d'objets, une classe Rectangle avec ses méthodes, et le lancer avec node dans le terminal intégré"
---

Au bit [Fonctions et objets](https://byte-layers.com/fr/bits/js-functions-objects), vous avez corrigé un `return` oublié et décrit des projets. Ici, vous écrivez un fichier entier, `formes.js`, et vous le lancez **sans navigateur** : avec Node.js, installé au lab « Votre poste de développeur ». Ce code ne touche pas à une page, il ne fait que calculer et afficher : Node.js l'exécute comme le moteur du navigateur, et `console.log` écrit dans le terminal.

## 05.1 - Une fonction qui rend son résultat

Créez `formes.js` dans le dossier du lab, et commencez par cette fonction, écrite exprès avec un défaut :

```javascript
// 1. Une fonction qui rend son résultat
function prixTTC(prixHT) {
  console.log(prixHT * 1.2);
}

console.log("Deux abonnements :", prixTTC(25) * 2);
```

Enregistrez, puis lancez le fichier dans le terminal intégré de VS Code, ouvert sur le dossier du lab :

```exec "Lancer formes.js"
node formes.js
```

Le terminal affiche deux lignes, et la seconde n'est pas celle qu'on attendait :

```text
30
Deux abonnements : NaN
```

C'est le piège du bit : la fonction affiche 30, mais ne le rend pas. À vous : corrigez `prixTTC` pour qu'elle **rende** son résultat, enregistrez et relancez. Le terminal doit afficher `Deux abonnements : 60`, et plus de `30` seul.

## 05.2 - Un objet et un tableau d'objets

À la suite, dans `formes.js`, écrivez ce qui suit, sous un commentaire `// 2. Des objets` :

1. un objet `livre` avec trois clés : `titre` (`"Dune"`), `auteur` (`"Frank Herbert"`) et `pages` (`900`) ;
2. une ligne qui affiche `Titre :` puis le titre du livre ;
3. une ligne qui affiche `Éditeur :` puis `livre.editeur`, une clé qui n'existe pas ;
4. un tableau `catalogue` de trois objets : `Dune` (900 pages), `Fondation` (420 pages), `La Horde du Contrevent` (712 pages), chacun avec les clés `titre` et `pages` ;
5. une boucle `for…of` qui additionne les pages dans une variable `totalPages`, déclarée avec `let` et à 0 avant la boucle ;
6. une ligne qui affiche `Total des pages :` puis `totalPages`.

Relancez `node formes.js` : la ligne de l'éditeur affiche `Éditeur : undefined`, sans erreur, et le total vaut 2032.

## 05.3 - Une classe Rectangle

Une **classe** est un moule qui fabrique des objets de même forme. `new Rectangle(10, 5)` crée un objet à partir du moule et appelle son `constructor` ; à l'intérieur de la classe, **`this`** désigne l'objet en cours de fabrication ou d'utilisation.

Sous un commentaire `// 3. Une classe`, écrivez la classe `Rectangle` en quatre morceaux, **tous à l'intérieur de ses accolades** :

| Morceau | Ce qu'il fait |
|---|---|
| `constructor(largeur, hauteur)` | range `largeur` et `hauteur` dans l'objet, avec `this.largeur = largeur;` et la même chose pour `hauteur` |
| `calculAire()` | rend `this.largeur * this.hauteur` |
| `calculPerimetre()` | rend `2 * (this.largeur + this.hauteur)` |
| `decrire()` | rend un texte de la forme `Rectangle 10x5, aire 50`, en appelant `this.calculAire()` |

Puis, après la classe :

1. rangez dans `premier` un `new Rectangle(10, 5)` ;
2. affichez `Aire :` puis `premier.calculAire()`, `Périmètre :` puis son périmètre, `Description :` puis `premier.decrire()` ;
3. rangez dans un tableau `formes` trois rectangles : 2 sur 3, 4 sur 5 et 6 sur 7 ;
4. calculez dans `totalAires` la somme de leurs aires, avec une boucle, et affichez `Total des aires :` puis le total.

Relancez : le terminal doit afficher, en tout :

```text
Deux abonnements : 60
Titre : Dune
Éditeur : undefined
Total des pages : 2032
Aire : 50
Périmètre : 30
Description : Rectangle 10x5, aire 50
Total des aires : 68
```

Si le terminal affiche `ReferenceError: largeur is not defined`, une méthode utilise `largeur` sans `this.` : le moteur cherche alors une variable, pas la valeur rangée dans l'objet.

```hint
`decrire()` assemble des textes et des nombres : `return "Rectangle " + this.largeur + "x" + this.hauteur + ", aire " + this.calculAire();`
```

```verify
F=~/byte-layers/web/js/formes.js
[ -f "$F" ] || { echo "Il n'y a pas de formes.js dans ~/byte-layers/web/js."; exit 1; }
command -v node >/dev/null 2>&1 || { echo "La commande node est introuvable. Installez Node.js (lab « Votre poste de développeur »)."; exit 1; }
OUT=$(cd ~/byte-layers/web/js && node formes.js 2>&1) || { echo "node formes.js s'arrête sur une erreur :"; echo "$OUT" | grep -m1 Error; exit 1; }
for attendu in "Deux abonnements : 60" "Titre : Dune" "Éditeur : undefined" "Total des pages : 2032" "Aire : 50" "Périmètre : 30" "Description : Rectangle 10x5, aire 50" "Total des aires : 68"; do
  if ! echo "$OUT" | grep -qxF "$attendu"; then
    echo "Le terminal n'affiche pas la ligne « $attendu »."
    exit 1
  fi
done
grep -q 'class Rectangle' "$F" || { echo "formes.js ne déclare pas de classe Rectangle."; exit 1; }
grep -q 'return' "$F" || { echo "Aucune fonction de formes.js ne rend son résultat avec return."; exit 1; }
echo "formes.js affiche les huit lignes attendues."
```

````solution
```javascript
// 1. Une fonction qui rend son résultat
function prixTTC(prixHT) {
  return prixHT * 1.2;
}

console.log("Deux abonnements :", prixTTC(25) * 2);

// 2. Des objets
const livre = { titre: "Dune", auteur: "Frank Herbert", pages: 900 };
console.log("Titre :", livre.titre);
console.log("Éditeur :", livre.editeur);

const catalogue = [
  { titre: "Dune", pages: 900 },
  { titre: "Fondation", pages: 420 },
  { titre: "La Horde du Contrevent", pages: 712 }
];
let totalPages = 0;
for (const unLivre of catalogue) {
  totalPages = totalPages + unLivre.pages;
}
console.log("Total des pages :", totalPages);

// 3. Une classe
class Rectangle {
  constructor(largeur, hauteur) {
    this.largeur = largeur;
    this.hauteur = hauteur;
  }
  calculAire() {
    return this.largeur * this.hauteur;
  }
  calculPerimetre() {
    return 2 * (this.largeur + this.hauteur);
  }
  decrire() {
    return "Rectangle " + this.largeur + "x" + this.hauteur + ", aire " + this.calculAire();
  }
}

const premier = new Rectangle(10, 5);
console.log("Aire :", premier.calculAire());
console.log("Périmètre :", premier.calculPerimetre());
console.log("Description :", premier.decrire());

const formes = [new Rectangle(2, 3), new Rectangle(4, 5), new Rectangle(6, 7)];
let totalAires = 0;
for (const forme of formes) {
  totalAires = totalAires + forme.calculAire();
}
console.log("Total des aires :", totalAires);
```
````

> 🔍 **Comprendre la vérification.** Elle lance `node formes.js` dans le dossier du lab, puis cherche chacune des huit lignes attendues, à l'identique, dans ce que le programme affiche.

## 05.4 - Ce que JSON ne transporte pas

Une dernière ligne, pour faire le lien avec l'étape 08. Ajoutez à la fin de `formes.js` :

```javascript
console.log("En JSON :", JSON.stringify(premier));
```

Relancez : le terminal affiche `En JSON : {"largeur":10,"hauteur":5}`. Les données sont là, les méthodes ont disparu : le JSON transporte des données, jamais du comportement. Un objet qui revient d'un JSON ressemble à un rectangle, mais n'a plus de `calculAire()`.

> 📖 [Les fonctions (MDN)](https://developer.mozilla.org/fr/docs/Web/JavaScript/Guide/Functions) · [Les classes (MDN)](https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Classes) · [Exécuter un fichier avec Node.js (en anglais)](https://nodejs.org/en/learn/command-line/run-nodejs-scripts-from-the-command-line)
