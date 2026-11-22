---
title: "08 - Un tableau rempli depuis un fichier JSON"
description: "Créer emprunts.json et registre.html, constater que fetch est refusé sur une page en file://, servir le dossier en http avec Live Preview ou python3, puis écrire registre.js : fetch, un statut calculé pour chaque emprunt, un résumé"
---

Au bit [Données JSON et fetch](https://byte-layers.com/fr/bits/json-fetch), l'aperçu servait le fichier JSON pour vous. Sur votre machine, une page ouverte par un double-clic ne peut pas faire de `fetch` : il faut un serveur. C'est le dernier piège du cours, et il ne se rencontre que là.

## 08.1 - Créer les données et la page du registre

Cette section est un **support**. Créez `emprunts.json` dans le dossier du lab, avec ce contenu, puis enregistrez. `jours` est le nombre de jours restants avant le retour du livre ; un nombre négatif veut dire que l'emprunt est en retard.

```json
[
  { "livre": "Dune", "lecteur": "Karim", "jours": 21 },
  { "livre": "Fondation", "lecteur": "Léa", "jours": 5 },
  { "livre": "Les Fourmis", "lecteur": "Tomas", "jours": 14 },
  { "livre": "Le Nom du vent", "lecteur": "Amina", "jours": -3 },
  { "livre": "Chroniques martiennes", "lecteur": "Léa", "jours": -12 }
]
```

Créez ensuite `registre.html`. Le corps du tableau, `#lignes`, est vide ; la classe `retard` colore une ligne en rouge.

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Registre des emprunts</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 700px; margin: 2rem auto; }
    table { width: 100%; border-collapse: collapse; }
    th, td { border: 1px solid #cbd5e1; padding: 0.5rem; text-align: left; }
    tr.retard { background-color: #fee2e2; }
  </style>
  <script src="registre.js" defer></script>
</head>
<body>
  <h1>Registre des emprunts</h1>
  <table>
    <thead>
      <tr><th>Livre</th><th>Lecteur</th><th>Jours restants</th><th>Statut</th></tr>
    </thead>
    <tbody id="lignes"></tbody>
  </table>
  <p id="resume"></p>
</body>
</html>
```

Créez enfin `registre.js`, avec seulement ces lignes, pour un premier essai :

```javascript
fetch("emprunts.json")
  .then((reponse) => reponse.json())
  .then((emprunts) => {
    console.log("Emprunts reçus :", emprunts.length);
  });
console.log("Demande envoyée");
```

```verify
D=~/byte-layers/web/js
for f in emprunts.json registre.html registre.js; do
  [ -f "$D/$f" ] || { echo "Il manque $f dans ~/byte-layers/web/js."; exit 1; }
done
command -v node >/dev/null 2>&1 || { echo "La vérification lit le JSON avec Node.js, introuvable ici."; exit 1; }
node -e '
const fs = require("fs");
let d;
try { d = JSON.parse(fs.readFileSync(process.argv[1], "utf8")); }
catch (e) { console.log("emprunts.json n'"'"'est pas un JSON valide : " + e.message); process.exit(1); }
if (!Array.isArray(d) || d.length !== 5) { console.log("emprunts.json doit contenir un tableau de cinq emprunts."); process.exit(1); }
' "$D/emprunts.json" || exit 1
echo "Les données, la page et le script sont en place."
```

## 08.2 - Ouvrir la page sans serveur : `fetch` refusé

Ouvrez `registre.html` comme les pages précédentes, par un double-clic ou avec `open` (`xdg-open`, `start`). La barre d'adresse commence par `file://`. Ouvrez la console : elle affiche des erreurs rouges et `Demande envoyée`, mais jamais `Emprunts reçus`. Dans Chrome, les erreurs disent :

```text
Fetch API cannot load file:///…/emprunts.json. URL scheme "file" is not supported.
Uncaught (in promise) TypeError: Failed to fetch
```

Firefox écrit `CORS request not HTTP`. Le navigateur refuse qu'une page ouverte depuis le disque lise d'autres fichiers du disque avec `fetch`, pour qu'une page téléchargée ne puisse pas lire vos fichiers. Le mot **CORS** (*Cross-Origin Resource Sharing*) désigne les règles qui disent quelle page peut lire quelle ressource. Pour `fetch`, la page doit être servie par un **serveur**, en `http://`.

Notez aussi où se place `Demande envoyée` : **avant** `Failed to fetch`, alors qu'elle est écrite après `fetch` dans le fichier. `fetch` ne bloque pas : la dernière ligne s'exécute pendant que la demande part, et l'échec n'arrive qu'ensuite.

## 08.3 - Servir le dossier en `http://`

Un serveur local, sur votre machine, sert les fichiers du dossier à l'adresse `http://localhost`, ou son équivalent `http://127.0.0.1`. Deux façons, au choix :

| Outil | Comment | Ce qu'il faut avoir |
|---|---|---|
| **Live Preview**, une extension de VS Code éditée par Microsoft | dans VS Code, panneau **Extensions** (Cmd+Maj+X sous macOS, Ctrl+Maj+X ailleurs), cherchez « Live Preview », **Install** ; puis clic droit sur `registre.html` dans l'explorateur, **Show Preview** ; le bouton d'ouverture dans le navigateur, en haut de l'aperçu, ouvre la même adresse dans votre navigateur | VS Code |
| le serveur intégré à Python | dans le terminal intégré, ouvert sur le dossier du lab, la commande ci-dessous, puis `http://localhost:8000/registre.html` dans le navigateur | Python 3, déjà présent sous Linux, et sous macOS une fois les outils de développement d'Apple installés |

Avec Python, la commande sert le dossier courant sur le port 8000, et occupe le terminal tant qu'elle tourne :

```exec "Servir le dossier du lab sur le port 8000"
python3 -m http.server 8000
```

`-m http.server` lance le module serveur web de Python, et `8000` est le **port**, le numéro de porte sur lequel il écoute. Pour l'arrêter, Ctrl+C dans le terminal. Sous Windows, la commande s'appelle souvent `py` au lieu de `python3`.

Ouvrez la page par le serveur : l'adresse commence par `http://`. La console affiche `Demande envoyée`, puis `Emprunts reçus : 5`, sans erreur rouge. Ce sont les mêmes fichiers ; seule la façon de les servir a changé.

## 08.4 - Remplir le tableau à partir des données

À vous : complétez `registre.js` pour que la page respecte ces critères. Gardez la page ouverte par le serveur, et rechargez-la après chaque enregistrement.

- Le tableau affiche **une ligne par emprunt**, dans l'ordre du fichier, avec quatre cellules : le livre, le lecteur, les jours restants, le statut.
- Le **statut est calculé**, jamais écrit dans les données : `En retard` si les jours sont négatifs, `Bientôt dû` jusqu'à 7 jours inclus, `En cours` au-delà.
- Les lignes en retard portent la classe `retard` : elles deviennent rouges. Il y en a deux.
- Le paragraphe `#resume` affiche `5 emprunt(s) · 2 en retard`, avec les deux nombres calculés.
- Tout ce qui utilise les données est **dans** le `.then` : écrit après, il s'exécuterait avant leur arrivée.

Découpez le travail en deux fonctions : `statut(jours)`, qui rend le texte du statut, et `afficher(emprunts)`, qui construit les lignes et le résumé. Le `.then` n'a plus qu'à appeler `afficher(emprunts)`.

```hint
Une ligne de tableau se construit comme un `<li>` : `document.createElement("tr")`, puis, pour chaque valeur, un `document.createElement("td")` rempli avec `textContent` et inséré dans le `tr` avec `append`.
```

```hint
Les frontières du statut, là où se cachent les erreurs : 0 jour donne `Bientôt dû` (zéro n'est pas négatif), 7 donne `Bientôt dû`, 8 donne `En cours`. La deuxième condition s'écrit donc `jours <= 7`.
```

```verify
F=~/byte-layers/web/js/registre.js
[ -f "$F" ] || { echo "Il n'y a pas de registre.js dans ~/byte-layers/web/js."; exit 1; }
command -v node >/dev/null 2>&1 || { echo "La vérification utilise Node.js, introuvable ici."; exit 1; }
node --check "$F" 2>/dev/null || { echo "registre.js contient une erreur de syntaxe :"; node --check "$F" 2>&1 | grep -m1 Error; exit 1; }
grep -Eq "fetch\([\"']\.?/?emprunts\.json[\"']\)" "$F" || { echo "registre.js ne demande pas emprunts.json avec fetch(\"emprunts.json\")."; exit 1; }
grep -q 'createElement("tr")\|createElement('"'"'tr'"'"')' "$F" || { echo "registre.js ne fabrique pas encore de ligne de tableau avec document.createElement(\"tr\")."; exit 1; }
grep -q 'function statut' "$F" || { echo "Il manque la fonction statut(jours), qui rend le texte du statut."; exit 1; }
node - "$F" <<'EOF'
// Extrait la fonction statut de registre.js et la teste aux frontières.
const code = require("fs").readFileSync(process.argv[2], "utf8");
const debut = code.indexOf("function statut");
let i = code.indexOf("{", debut), prof = 0, fin = i;
for (; fin < code.length; fin++) { if (code[fin] === "{") prof++; if (code[fin] === "}" && --prof === 0) break; }
let statut;
try { statut = new Function(code.slice(debut, fin + 1) + "\nreturn statut;")(); }
catch (e) { console.log("La fonction statut ne se lit pas seule : " + e.message); process.exit(1); }
const cas = [[-12, "En retard"], [-1, "En retard"], [0, "Bientôt dû"], [7, "Bientôt dû"], [8, "En cours"], [21, "En cours"]];
for (const [jours, attendu] of cas) {
  const obtenu = statut(jours);
  if (obtenu !== attendu) { console.log("statut(" + jours + ") devrait rendre « " + attendu + " », il rend « " + obtenu + " »."); process.exit(1); }
}
EOF
[ $? -eq 0 ] || exit 1
grep -q 'emprunts.length' "$F" || { echo "Le nombre d'emprunts du résumé doit venir de emprunts.length."; exit 1; }
grep -Eq '\.style\b|innerHTML' "$F" && { echo "registre.js écrit du style ou du HTML brut : posez la classe retard avec classList, créez les cellules avec createElement."; exit 1; }
echo "Le registre se remplit depuis emprunts.json, avec un statut calculé."
```

````solution
```javascript
const lignes = document.querySelector("#lignes");
const resume = document.querySelector("#resume");

function statut(jours) {
  if (jours < 0) {
    return "En retard";
  } else if (jours <= 7) {
    return "Bientôt dû";
  } else {
    return "En cours";
  }
}

function afficher(emprunts) {
  let retards = 0;
  for (const emprunt of emprunts) {
    const tr = document.createElement("tr");
    for (const valeur of [emprunt.livre, emprunt.lecteur, emprunt.jours, statut(emprunt.jours)]) {
      const td = document.createElement("td");
      td.textContent = valeur;
      tr.append(td);
    }
    if (emprunt.jours < 0) {
      tr.classList.add("retard");
      retards = retards + 1;
    }
    lignes.append(tr);
  }
  resume.textContent = emprunts.length + " emprunt(s) · " + retards + " en retard";
}

fetch("emprunts.json")
  .then((reponse) => reponse.json())
  .then((emprunts) => {
    console.log("Emprunts reçus :", emprunts.length);
    afficher(emprunts);
  });
console.log("Demande envoyée");
```
````

> 🔍 **Comprendre la vérification.** Elle relit `registre.js` (syntaxe, `fetch("emprunts.json")`, `createElement("tr")`), puis extrait votre fonction `statut` et l'appelle aux frontières : -12, -1, 0, 7, 8 et 21 jours. Le tableau dans la page, c'est vous qui le regardez.

Pour voir le piège de `fetch` une dernière fois, faites une copie de `registre.js`, puis modifiez-le ainsi : une ligne `let donnees = [];` avant le `fetch`, `donnees = emprunts;` à la place de `afficher(emprunts);` dans le `.then`, et `afficher(donnees);` tout à la fin du fichier. Rechargez : le tableau reste vide et le résumé dit `0 emprunt(s) · 0 en retard`. `afficher` s'est exécutée avant l'arrivée des données, avec le tableau vide. Remettez votre version.

## Récap

- La **console** du navigateur exécute du JavaScript tout de suite ; `alert`, `confirm` et `prompt` parlent au visiteur, et `prompt` rend toujours du texte.
- Un script se branche avec **`<script src="…" defer>`** : sans `defer` dans le `<head>`, il trouve `null`.
- Les **conditions** choisissent (`===`, `else if`, `Number.isNaN`), les **boucles** répètent (`while` jusqu'à trouver, `for…of` sur un tableau), et un `while` a toujours une sortie : ici `break` sur Annuler.
- Une **fonction** rend son résultat avec `return` ; un **objet** décrit, une **classe** fabrique ; Node.js exécute le même JavaScript hors du navigateur.
- Le **DOM** se lit avec `querySelector`, se construit avec `createElement` et `append`, se colore avec `classList` ; les **événements** déclenchent le code, et `preventDefault` garde un formulaire sur la page.
- **`fetch`** lit un fichier JSON par un serveur, en `http://`, jamais en `file://`, et ne bloque pas : tout ce qui utilise les données va dans le `.then`.

Vous avez tout ce qu'il faut pour rendre votre portfolio interactif : un formulaire de contact qui valide ses champs, des projets qui se chargent depuis un fichier JSON. C'est le challenge [Portfolio v3 : une page qui réagit](https://byte-layers.com/fr/challenges/portfolio-v3-challenge).

## Questions

```quiz
title: "Les bases de JavaScript"
tracksProgress: false
showNotice: false
questions:
  - prompt: "Dans le jeu de devinette, pourquoi tester `saisie === null` avant `Number(saisie)` ?"
    answers:
      - "Parce que Number(null) vaut 0 : sans ce test, Annuler serait pris pour la proposition 0, et la boucle redemanderait sans fin"
      - "Parce que Number(null) lève une erreur"
      - "Pour que le jeu soit plus rapide"
    correct: 1
    explanation: "Number(null) vaut 0, sans erreur. Testé après la conversion, Annuler ressemble à une proposition de zéro, et la boucle continue. Le test doit venir avant."
  - prompt: "Une page ouverte en `file://` fait `fetch(\"emprunts.json\")`. Que se passe-t-il ?"
    answers:
      - "Les données arrivent normalement"
      - "Le navigateur refuse la demande : il faut servir la page par un serveur, en http://"
      - "La page se recharge"
    correct: 2
    explanation: "Le navigateur interdit à une page ouverte depuis le disque de lire d'autres fichiers avec fetch. Un serveur local, Live Preview ou python3 -m http.server, résout le problème."
  - prompt: "Pourquoi la vérification de l'étape 05 peut-elle lancer `formes.js` avec Node.js, alors que celle de l'étape 06 ne lance pas `catalogue.js` ?"
    answers:
      - "Parce que formes.js est plus court"
      - "Parce que formes.js ne fait que calculer et afficher, alors que catalogue.js agit sur une page, que Node.js n'a pas"
      - "Parce que Node.js ne connaît pas les boucles"
    correct: 2
    explanation: "Node.js exécute le langage JavaScript, mais sans navigateur il n'y a ni page ni document : document.querySelector n'existe pas. Le code qui touche au DOM se teste dans un navigateur."
```
