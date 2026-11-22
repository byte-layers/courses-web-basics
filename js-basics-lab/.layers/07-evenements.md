---
title: "07 - Une lampe qui réagit au clic, un formulaire qui ne recharge pas"
description: "Écrire lampe.js : un écouteur de clic qui bascule une classe et compte les clics, et le piège de f() ; puis contact.js : un formulaire écouté sur submit, preventDefault, des champs validés avec trim"
---

Au bit [Les événements : réagir aux actions du visiteur](https://byte-layers.com/fr/bits/dom-events), l'aperçu ne savait pas envoyer de formulaire. Ici, vous écrivez deux petites pages complètes : une lampe qui répond aux clics, puis un formulaire de contact, et vous voyez de vos yeux ce que fait un formulaire sans `preventDefault`.

## 07.1 - Créer la page de la lampe

Cette section est un **support**. Créez `lampe.html` dans le dossier du lab, avec ce contenu, puis enregistrez. La classe `allumee` existe déjà dans le CSS.

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Lampe</title>
  <style>
    body { font-family: system-ui, sans-serif; margin: 2rem; }
    #lampe { width: 100px; height: 100px; border-radius: 50%; background-color: #cbd5e1; }
    #lampe.allumee { background-color: #facc15; }
  </style>
  <script src="lampe.js" defer></script>
</head>
<body>
  <div id="lampe"></div>
  <p id="etat">La lampe est éteinte</p>
  <p id="compteur">0 clic(s)</p>
  <button id="basculer">Allumer / Éteindre</button>
</body>
</html>
```

Créez aussi `lampe.js`, vide pour l'instant.

## 07.2 - Allumer et éteindre au clic

À vous : écrivez `lampe.js` pour que la page respecte ces critères.

- Chaque clic sur le bouton **bascule** la classe `allumee` de la lampe : jaune, puis grise, puis jaune…
- Le paragraphe `#etat` dit `La lampe est allumée` ou `La lampe est éteinte`, en accord avec la couleur.
- Le paragraphe `#compteur` affiche le nombre de clics, suivi de `clic(s)` ; il continue de monter quand on éteint.
- À chaque clic, la console affiche `Clic n°` suivi du numéro.
- Aucune couleur dans le JavaScript : la classe, et le CSS fait le reste.

Écrivez une fonction `basculer`, puis confiez-la au bouton avec `addEventListener`. Enregistrez, ouvrez `lampe.html` dans le navigateur, console ouverte, et cliquez trois fois : la lampe est allumée, le compteur dit `3 clic(s)`, la console a trois lignes.

```hint
Le compteur est une variable `let clics = 0;`, déclarée hors de la fonction : déclarée dedans, elle repartirait de 0 à chaque clic.
```

```verify
F=~/byte-layers/web/js/lampe.js
[ -f "$F" ] || { echo "Il n'y a pas de lampe.js dans ~/byte-layers/web/js."; exit 1; }
if command -v node >/dev/null 2>&1 && ! node --check "$F" 2>/dev/null; then
  echo "lampe.js contient une erreur de syntaxe :"; node --check "$F" 2>&1 | grep -m1 Error; exit 1
fi
grep -Eq "addEventListener\(\s*[\"']click[\"']" "$F" || { echo "lampe.js n'écoute pas encore le clic : bouton.addEventListener(\"click\", basculer)."; exit 1; }
if grep -Eq "addEventListener\(\s*[\"']click[\"']\s*,\s*[A-Za-z_][A-Za-z0-9_]*\(\)" "$F"; then
  echo "La fonction est appelée au chargement : retirez les parenthèses après son nom dans addEventListener."
  exit 1
fi
grep -Eq 'classList\.(toggle|add|remove)' "$F" || { echo "lampe.js ne pose pas encore la classe allumee avec classList."; exit 1; }
grep -q 'clic(s)' "$F" || { echo "Le compteur n'affiche pas encore « clic(s) »."; exit 1; }
grep -Eq '\.style\b' "$F" && { echo "lampe.js écrit un style : basculez la classe allumee, la couleur reste dans le CSS."; exit 1; }
echo "La lampe écoute le clic et bascule sa classe."
```

````solution
```javascript
const lampe = document.querySelector("#lampe");
const etat = document.querySelector("#etat");
const compteur = document.querySelector("#compteur");
const bouton = document.querySelector("#basculer");

let clics = 0;

function basculer() {
  lampe.classList.toggle("allumee");
  clics = clics + 1;
  if (lampe.classList.contains("allumee")) {
    etat.textContent = "La lampe est allumée";
  } else {
    etat.textContent = "La lampe est éteinte";
  }
  compteur.textContent = clics + " clic(s)";
  console.log("Clic n°", clics);
}

bouton.addEventListener("click", basculer);
```
````

Une fois la lampe vérifiée, ajoutez volontairement des parenthèses : `addEventListener("click", basculer())`. Enregistrez, rechargez **sans cliquer** : la lampe est déjà jaune, le compteur dit `1 clic(s)`, la console affiche `Clic n° 1`, et le bouton ne répond plus. La fonction a été appelée au chargement, au lieu d'être confiée. Retirez les parenthèses.

## 07.3 - Créer le formulaire de contact

Cette section est un **support**. Créez `contact.html`, avec ce contenu, puis enregistrez. L'attribut `novalidate` du `<form>` coupe la validation automatique du navigateur, pour que la vôtre, en JavaScript, soit la seule : c'est elle que vous écrivez ici.

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Contact</title>
  <style>
    body { font-family: system-ui, sans-serif; margin: 2rem; }
    label, input { display: block; margin: 0.25rem 0; }
    #message { color: #166534; }
    #message.erreur { color: #b91c1c; }
  </style>
  <script src="contact.js" defer></script>
</head>
<body>
  <h1>Me contacter</h1>
  <form id="contact" novalidate>
    <label for="nom">Nom</label>
    <input id="nom" name="nom">
    <label for="email">E-mail</label>
    <input id="email" name="email" type="email">
    <button type="submit">Envoyer</button>
  </form>
  <p id="message"></p>
</body>
</html>
```

Avant d'écrire une ligne de JavaScript, ouvrez la page dans le navigateur, tapez un nom et appuyez sur Entrée : la page se recharge, les champs se vident, et l'adresse se termine maintenant par `?nom=…&email=`. C'est le comportement par défaut d'un formulaire : envoyer ses champs, ici à la page elle-même, en rechargeant. C'est lui que votre code doit couper.

Créez ensuite `contact.js`, vide pour l'instant.

## 07.4 - Valider sans recharger la page

À vous : écrivez `contact.js` pour que le formulaire respecte ces critères.

- L'écouteur se pose sur le **`<form>`**, pour l'événement **`submit`** : il couvre le clic sur le bouton et la touche Entrée dans un champ.
- La page **ne se recharge pas** : l'adresse ne change plus, la console garde ses messages.
- Si l'un des deux champs est vide, **ou ne contient que des espaces**, le message affiche `Remplissez les deux champs.` et porte la classe `erreur` (il devient rouge). Les champs ne sont pas vidés.
- Si l'adresse ne contient pas de `@`, le message affiche `L'adresse e-mail doit contenir un @.`, avec la classe `erreur`.
- Sinon, le message affiche `Merci Ada, message envoyé.` (avec le nom saisi), **sans** la classe `erreur`, et les champs sont vidés.

Deux outils nouveaux : `texte.includes("@")` rend `true` si le texte contient `@` ; `formulaire.reset()` remet tous les champs du formulaire à vide.

Enregistrez, rechargez, et testez les trois cas : deux champs pleins d'espaces, une adresse sans `@`, puis une saisie correcte. Après un refus, une saisie correcte doit rendre le message vert.

```hint
L'écouteur reçoit l'événement : `formulaire.addEventListener("submit", function (evenement) { evenement.preventDefault(); … });`. Lisez ensuite chaque champ avec `.value.trim()`.
```

```hint
Après un refus, la classe `erreur` reste posée tant que rien ne la retire : dans le cas correct, `message.classList.remove("erreur")`.
```

```verify
F=~/byte-layers/web/js/contact.js
[ -f "$F" ] || { echo "Il n'y a pas de contact.js dans ~/byte-layers/web/js."; exit 1; }
if command -v node >/dev/null 2>&1 && ! node --check "$F" 2>/dev/null; then
  echo "contact.js contient une erreur de syntaxe :"; node --check "$F" 2>&1 | grep -m1 Error; exit 1
fi
grep -Eq "addEventListener\(\s*[\"']submit[\"']" "$F" || { echo "contact.js n'écoute pas encore l'envoi : formulaire.addEventListener(\"submit\", …), sur le <form>."; exit 1; }
grep -q 'preventDefault()' "$F" || { echo "Sans evenement.preventDefault(), la page se recharge à l'envoi et efface tout."; exit 1; }
grep -q 'trim()' "$F" || { echo "Un champ plein d'espaces passe encore pour rempli : lisez les champs avec .value.trim()."; exit 1; }
grep -q 'includes("@")\|includes('"'"'@'"'"')' "$F" || { echo "contact.js ne vérifie pas encore que l'adresse contient un @ : email.includes(\"@\")."; exit 1; }
grep -q 'classList.remove' "$F" || { echo "Après un refus, la classe erreur n'est jamais retirée : message.classList.remove(\"erreur\") dans le cas correct."; exit 1; }
echo "Le formulaire est validé en JavaScript, sans rechargement."
```

````solution
```javascript
const formulaire = document.querySelector("#contact");
const champNom = document.querySelector("#nom");
const champEmail = document.querySelector("#email");
const message = document.querySelector("#message");

formulaire.addEventListener("submit", function (evenement) {
  evenement.preventDefault();
  const nom = champNom.value.trim();
  const email = champEmail.value.trim();

  if (nom === "" || email === "") {
    message.textContent = "Remplissez les deux champs.";
    message.classList.add("erreur");
  } else if (!email.includes("@")) {
    message.textContent = "L'adresse e-mail doit contenir un @.";
    message.classList.add("erreur");
  } else {
    message.textContent = "Merci " + nom + ", message envoyé.";
    message.classList.remove("erreur");
    formulaire.reset();
  }
});
```
````

Une fois le formulaire vérifié, mettez en commentaire la ligne `evenement.preventDefault();` (un `//` devant), enregistrez, rechargez, remplissez correctement et envoyez. La page se recharge, l'adresse reprend son `?nom=…`, la console se vide : votre code s'est bien exécuté, puis le rechargement a tout effacé, sans erreur rouge. Retirez le `//`.

> 📖 [addEventListener (MDN)](https://developer.mozilla.org/fr/docs/Web/API/EventTarget/addEventListener) · [L'événement submit (MDN)](https://developer.mozilla.org/fr/docs/Web/API/HTMLFormElement/submit_event) · [String.prototype.includes (MDN)](https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Global_Objects/String/includes)
