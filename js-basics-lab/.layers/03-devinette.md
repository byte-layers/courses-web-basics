---
title: "03 - Le jeu de devinette, en un essai"
description: "Créer devinette.html et devinette.js, tirer un nombre secret, demander une proposition avec prompt, la convertir, et répondre avec une chaîne if / else if / else"
---

Au bit [Décider : les conditions en JavaScript](https://byte-layers.com/fr/bits/js-conditions), le jeu de devinette recevait des saisies écrites dans le code. Ici, c'est vous qui jouez : le programme tire un nombre au hasard, vous pose la question dans une vraie boîte `prompt`, et répond dans une boîte `alert`.

## 03.1 - Créer la page du jeu

Cette section est un **support**. Créez `devinette.html` dans le dossier du lab, avec ce contenu, puis enregistrez. La page ne contient presque rien : le jeu se passe dans les boîtes de dialogue et dans la console.

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Devinette</title>
  <script src="devinette.js" defer></script>
</head>
<body>
  <h1>Devinez un nombre entre 1 et 10</h1>
  <p>Rechargez la page pour rejouer.</p>
</body>
</html>
```

Créez ensuite `devinette.js`, avec ce squelette : les lignes qui commencent par `//` sont des commentaires, qui disent ce que vous allez écrire.

```javascript
// 1. Les réglages
const MINIMUM = 1;
const MAXIMUM = 10;

// 2. Le nombre secret, et une ligne de triche pour tester
const secret = Math.floor(Math.random() * MAXIMUM) + MINIMUM;
console.log("[triche] le secret est :", secret);

// 3. Demander et convertir

// 4. Répondre
```

La formule du secret est celle du dé de l'étape 01, avec `MAXIMUM` à la place de 6 : elle rend un entier de 1 à 10. Le secret s'affiche dans la console, volontairement : sans cela, vous ne pourriez pas tester chaque réponse du jeu.

## 03.2 - Demander une proposition et la convertir

Sous le commentaire `// 3.`, écrivez deux lignes :

- rangez dans une constante `saisie` la réponse à `prompt("Devinez un nombre entre 1 et 10")` ;
- rangez dans une constante `proposition` cette saisie convertie en nombre.

Sans la conversion, la comparaison de la section suivante serait fausse à tous les coups : `"7" === 7` vaut `false`. Un joueur qui trouve perdrait, sans aucune erreur rouge.

## 03.3 - Répondre avec une chaîne de conditions

Sous le commentaire `// 4.`, écrivez une chaîne `if / else if / else` qui affiche, dans une boîte `alert`, **dans cet ordre** :

| Si la proposition… | La boîte affiche |
|---|---|
| n'est pas un nombre | `Ce n'est pas un nombre.` |
| est égale au secret | `Gagné !` |
| est plus petite | `Trop petit.` |
| sinon | `Trop grand.` |

Pour le premier cas, une précision. `Number("abc")` rend **`NaN`** (*Not a Number*), une valeur de type nombre qui veut dire « pas un nombre ». Et `NaN` a une particularité : il n'est égal à rien, pas même à lui-même, donc `proposition === NaN` vaut toujours `false`. On le teste avec **`Number.isNaN(proposition)`**, qui rend `true` ou `false`. Ce test vient en premier : placé plus bas, il ne serait jamais atteint, puisque `NaN < secret` et `NaN === secret` valent tous deux `false` et qu'on tomberait dans le `else`.

Enregistrez, ouvrez `devinette.html` dans le navigateur, console ouverte, et jouez. Lisez le secret dans la console, puis rechargez et répondez volontairement de chaque façon : le bon nombre, un plus petit, un plus grand, `abc`.

```hint
La condition du premier cas : `if (Number.isNaN(proposition))`. Celle du deuxième : `else if (proposition === secret)`.
```

```verify
F=~/byte-layers/web/js/devinette.js
[ -f "$F" ] || { echo "Il n'y a pas de devinette.js dans ~/byte-layers/web/js."; exit 1; }
command -v node >/dev/null 2>&1 || { echo "La vérification exécute votre jeu avec Node.js, introuvable ici. Installez-le (lab « Votre poste de développeur »)."; exit 1; }
node - "$F" <<'EOF'
const code = require("fs").readFileSync(process.argv[2], "utf8");
const vm = require("vm");
// Joue le jeu une fois : prompt répond selon le secret affiché dans la console.
function jouer(choisir) {
  const alertes = [];
  let vu;
  const ctx = {
    console: { log: (...a) => { for (const x of a) if (typeof x === "number") vu = x; } },
    alert: (m) => alertes.push(String(m)),
    prompt: () => (vu === undefined ? null : choisir(vu)),
  };
  vm.createContext(ctx);
  vm.runInContext(code, ctx, { timeout: 2000 });
  return { alertes, vu };
}
const cas = [
  ["le secret", (s) => String(s), "Gagné !"],
  ["un nombre plus petit", (s) => String(s - 1), "Trop petit."],
  ["un nombre plus grand", (s) => String(s + 1), "Trop grand."],
  ["abc", () => "abc", "Ce n'est pas un nombre."],
];
for (const [nom, choisir, attendu] of cas) {
  let r;
  try { r = jouer(choisir); } catch (e) { console.log("Le jeu s'arrête sur une erreur : " + e.message); process.exit(1); }
  if (r.vu === undefined) { console.log("La console n'affiche pas le secret : gardez la ligne console.log(\"[triche] le secret est :\", secret);"); process.exit(1); }
  if (r.vu < 1 || r.vu > 10 || !Number.isInteger(r.vu)) { console.log("Le secret vaut " + r.vu + " : il doit être un entier de 1 à 10."); process.exit(1); }
  const obtenu = r.alertes.join(" / ");
  if (obtenu !== attendu) {
    console.log("Quand on répond " + nom + ", la boîte devrait afficher « " + attendu + " », elle affiche « " + (obtenu || "rien") + " ».");
    if (nom === "le secret") console.log("La saisie est-elle convertie avec Number() avant d'être comparée avec === ?");
    process.exit(1);
  }
}
console.log("Les quatre réponses du jeu sont justes.");
EOF
```

````solution
```javascript
// 3. Demander et convertir
const saisie = prompt("Devinez un nombre entre 1 et 10");
const proposition = Number(saisie);

// 4. Répondre
if (Number.isNaN(proposition)) {
  alert("Ce n'est pas un nombre.");
} else if (proposition === secret) {
  alert("Gagné !");
} else if (proposition < secret) {
  alert("Trop petit.");
} else {
  alert("Trop grand.");
}
```
````

> 🔍 **Comprendre la vérification.** Elle exécute votre `devinette.js` avec Node.js, quatre fois, en remplaçant `prompt` par une fonction qui répond à votre place (le secret lu dans la console, un nombre plus petit, un plus grand, `abc`) et `alert` par une fonction qui note le message. Elle compare ensuite chaque message à celui du tableau.

## 03.4 - Deux réponses qui surprennent

Rechargez, et cliquez sur OK sans rien taper : la boîte dit « Trop petit. ». Rechargez, et cliquez sur Annuler : même réponse. Une saisie vide rend `""`, une annulation rend `null`, et `Number("")` comme `Number(null)` valent `0`. Votre jeu ne peut pas les distinguer d'une vraie proposition de zéro.

Ce n'est pas une faute de votre code, c'est une limite de cette version du jeu, qui ne pose la question qu'une fois. L'étape suivante le fait redemander, et elle aura besoin de distinguer l'annulation : sinon, cliquer sur Annuler relancerait la question pour toujours.

> 📖 [Number.isNaN (MDN)](https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Global_Objects/Number/isNaN) · [if...else (MDN)](https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Statements/if...else)
