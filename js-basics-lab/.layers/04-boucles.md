---
title: "04 - La devinette qui redemande, et la liste des essais"
description: "Transformer le jeu en boucle while qui redemande jusqu'à trouver, arrêter proprement sur Annuler, ranger chaque essai dans un tableau et l'afficher avec for…of"
---

Le jeu de l'étape 03 n'accorde qu'un essai : il lui manquait une boucle. Au bit [Répéter : tableaux et boucles](https://byte-layers.com/fr/bits/js-arrays-loops), vous avez vu `while`, sans l'écrire : une boucle sans fin aurait figé l'aperçu. Ici, vous l'écrivez, sur votre machine, où une boucle sans fin se répare en fermant l'onglet.

> ⚠️ **Cette étape peut figer votre onglet, et c'est réparable.** Si la page ne répond plus et que la boîte revient sans cesse : fermez l'onglet (Ctrl+W, Cmd+W sous macOS ; si la boîte bloque la fermeture, quittez le navigateur), corrigez `devinette.js`, enregistrez, rouvrez la page. Rien n'est cassé, et cela arrive à tout le monde.

## 04.1 - Faire redemander le jeu avec `while`

On garde les sections 1 et 2 de `devinette.js` (les réglages, le secret). On remplace les sections 3 et 4 par une boucle, qui redemande **tant que** le joueur n'a pas trouvé. Avant d'écrire un `while`, la question à se poser : qu'est-ce qui rendra la condition fausse ? Ici, une variable `trouve`, qui passe à `true` quand le joueur trouve.

Remplacez tout ce qui suit le commentaire `// 3.` par ce squelette, puis complétez les trois commentaires `// À vous` :

```javascript
// 3. Jouer jusqu'à trouver
const essais = [];
let trouve = false;

while (!trouve) {
  const saisie = prompt("Devinez un nombre entre 1 et 10");
  // À vous : si saisie vaut null (le joueur a cliqué sur Annuler), sortir de la boucle avec break
  const proposition = Number(saisie);
  essais.push(proposition);
  // À vous : la chaîne de conditions de l'étape 03, avec deux changements :
  //   - quand c'est le secret, trouve passe à true
  //   - le message devient "Gagné en " + essais.length + " essai(s) !"
}

// 4. Le bilan
// À vous : si trouve vaut false, afficher "Partie abandonnée." dans une boîte alert
```

| Morceau | Rôle |
|---|---|
| `const essais = []` | un tableau vide, qui recevra chaque proposition |
| `while (!trouve)` | répète tant que `trouve` vaut `false` ; `!` se lit « non » |
| `essais.push(proposition)` | ajoute la proposition à la fin du tableau |
| `break` | sort de la boucle tout de suite, quelle que soit sa condition |

Le test d'annulation doit venir **avant** la conversion. À l'étape 03, vous avez vu que `Number(null)` vaut `0`. Dans une boucle, c'est un piège : le joueur annule, le programme croit qu'il propose 0, ce n'est pas le secret, il redemande. Annuler ne servirait plus à rien, et la boîte reviendrait sans fin.

Enregistrez, rechargez la page, et jouez : trop petit, trop grand, puis juste. Rechargez et cliquez sur Annuler tout de suite : la boîte « Partie abandonnée. » s'affiche, et la boucle s'arrête.

```hint
Le test d'annulation tient en trois lignes : `if (saisie === null) {`, puis `break;`, puis `}`.
```

```verify
F=~/byte-layers/web/js/devinette.js
[ -f "$F" ] || { echo "Il n'y a pas de devinette.js dans ~/byte-layers/web/js."; exit 1; }
command -v node >/dev/null 2>&1 || { echo "La vérification exécute votre jeu avec Node.js, introuvable ici."; exit 1; }
grep -q 'while' "$F" || { echo "devinette.js n'a pas encore de boucle while."; exit 1; }
node - "$F" <<'EOF'
const code = require("fs").readFileSync(process.argv[2], "utf8");
const vm = require("vm");
// Joue une partie : prompt donne les réponses de la liste, à partir du secret lu dans la console.
function partie(reponses) {
  const alertes = [];
  const logs = [];
  let vu;
  let tour = 0;
  let suite;
  const ctx = {
    console: { log: (...a) => { logs.push(a.join(" ")); for (const x of a) if (typeof x === "number" && vu === undefined) vu = x; } },
    alert: (m) => alertes.push(String(m)),
    prompt: () => {
      if (!suite) suite = reponses(vu);
      return tour < suite.length ? suite[tour++] : null;
    },
  };
  vm.createContext(ctx);
  vm.runInContext(code, ctx, { timeout: 2000 });
  return { alertes, logs };
}
let r;
try {
  r = partie((s) => [String(s - 1), String(s + 1), String(s)]);
} catch (e) {
  console.log(/timed out/.test(e.message) ? "La boucle ne s'arrête pas quand le joueur trouve : trouve passe-t-il à true ?" : "Le jeu s'arrête sur une erreur : " + e.message);
  process.exit(1);
}
const attendu = "Trop petit. / Trop grand. / Gagné en 3 essai(s) !";
if (r.alertes.join(" / ") !== attendu) {
  console.log("En jouant plus petit, plus grand, puis le secret, les boîtes devraient afficher « " + attendu + " », elles affichent « " + r.alertes.join(" / ") + " ».");
  process.exit(1);
}
try {
  r = partie(() => [null]);
} catch (e) {
  console.log(/timed out/.test(e.message) ? "Quand le joueur clique sur Annuler, la boucle ne s'arrête pas : testez saisie === null avant Number(saisie), et sortez avec break." : "Le jeu s'arrête sur une erreur : " + e.message);
  process.exit(1);
}
if (r.alertes.join(" / ") !== "Partie abandonnée.") {
  console.log("Quand le joueur annule tout de suite, une seule boîte devrait s'afficher, « Partie abandonnée. ». Elle affiche « " + r.alertes.join(" / ") + " ».");
  process.exit(1);
}
console.log("Le jeu redemande jusqu'à trouver, et s'arrête proprement sur Annuler.");
EOF
```

````solution
```javascript
// 3. Jouer jusqu'à trouver
const essais = [];
let trouve = false;

while (!trouve) {
  const saisie = prompt("Devinez un nombre entre 1 et 10");
  if (saisie === null) {
    break;
  }
  const proposition = Number(saisie);
  essais.push(proposition);
  if (Number.isNaN(proposition)) {
    alert("Ce n'est pas un nombre.");
  } else if (proposition === secret) {
    trouve = true;
    alert("Gagné en " + essais.length + " essai(s) !");
  } else if (proposition < secret) {
    alert("Trop petit.");
  } else {
    alert("Trop grand.");
  }
}

// 4. Le bilan
if (!trouve) {
  alert("Partie abandonnée.");
}
```
````

> 🔍 **Comprendre la vérification.** Comme à l'étape 03, elle exécute votre jeu avec Node.js en répondant à la place du joueur : une partie « plus petit, plus grand, le secret », puis une partie où le joueur annule tout de suite. Une boucle qui ne s'arrête pas est coupée au bout de deux secondes, et la vérification vous dit laquelle.

## 04.2 - Afficher la liste des essais avec `for…of`

Le tableau `essais` contient chaque proposition, dans l'ordre. À la fin de `devinette.js`, après le bilan, parcourez-le avec `for…of` et affichez une ligne par essai dans la console, de la forme `Essai : 4`.

Rejouez une partie en trois essais : la console affiche, sous la ligne de triche, trois lignes `Essai :`, une par proposition. Une instruction écrite, trois exécutions : c'est le travail d'une boucle.

```verify
F=~/byte-layers/web/js/devinette.js
command -v node >/dev/null 2>&1 || { echo "La vérification exécute votre jeu avec Node.js, introuvable ici."; exit 1; }
grep -Eq 'for *\( *(const|let) +[A-Za-z_]+ +of +essais *\)' "$F" || { echo "devinette.js ne parcourt pas encore essais avec for (const essai of essais)."; exit 1; }
node - "$F" <<'EOF'
const code = require("fs").readFileSync(process.argv[2], "utf8");
const vm = require("vm");
const logs = [];
let vu, tour = 0, suite;
const ctx = {
  console: { log: (...a) => { logs.push(a.join(" ")); for (const x of a) if (typeof x === "number" && vu === undefined) vu = x; } },
  alert: () => {},
  prompt: () => { if (!suite) suite = [String(vu - 1), String(vu + 1), String(vu)]; return tour < suite.length ? suite[tour++] : null; },
};
vm.createContext(ctx);
try { vm.runInContext(code, ctx, { timeout: 2000 }); } catch (e) { console.log("Le jeu s'arrête sur une erreur : " + e.message); process.exit(1); }
const lignes = logs.filter((l) => /^Essai :/.test(l));
if (lignes.length !== 3) { console.log("Après une partie en trois essais, la console devrait afficher trois lignes « Essai : … », elle en affiche " + lignes.length + "."); process.exit(1); }
console.log("La console affiche les trois essais.");
EOF
```

````solution
```javascript
for (const essai of essais) {
  console.log("Essai :", essai);
}
```
````

## 04.3 - Provoquer une boucle sans fin, volontairement

Une fois tout terminé et vérifié, voyez la panne la plus courante des boucles, pour savoir la reconnaître. Dans `devinette.js`, supprimez les trois lignes du test d'annulation, `if (saisie === null) { break; }`. Enregistrez, rechargez, et cliquez sur **Annuler**.

La boîte revient, encore et encore : `Number(null)` vaut 0, « Trop petit. », et la boucle redemande. Fermez l'onglet (ou quittez le navigateur si la boîte vous en empêche), remettez les trois lignes, enregistrez, et vérifiez que Annuler arrête de nouveau la partie.

> 📖 [while (MDN)](https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Statements/while) · [for...of (MDN)](https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Statements/for...of) · [break (MDN)](https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Statements/break)
