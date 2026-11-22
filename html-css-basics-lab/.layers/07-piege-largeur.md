---
title: "07 - Des cartes aérées, et le piège de la largeur"
description: "Transformer trois blocs collés en cartes avec padding, bordure et marge, centrer un conteneur, voir le modèle de boîte dans l'inspecteur, puis mesurer les 40 px de trop sans box-sizing"
---

Le bit [Le modèle de boîte](https://byte-layers.com/fr/bits/box-model) a fait calculer la largeur réelle d'une boîte. Dans cette dernière étape, vous écrivez seul la feuille de style d'une page de cartes, puis l'inspecteur vous montre chaque couche de la boîte, en pixels, et le piège de la largeur sur votre propre page.

## 07.1 - Créer la page des cartes

Cette section est un support. Créez `cartes.html` dans `BASICS`, collez-y la page ci-dessous, puis créez à côté un fichier vide `cartes.css` :

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Médiathèque : nos services</title>
  <link rel="stylesheet" href="cartes.css">
</head>
<body>
  <div class="conteneur">
    <header>
      <h1>Nos services</h1>
    </header>
    <main>
      <div class="carte">
        <h2>Emprunter</h2>
        <p>Jusqu'à dix documents pour trois semaines, renouvelables une fois.</p>
      </div>
      <div class="carte">
        <h2>Travailler sur place</h2>
        <p>Quarante places assises, le wifi gratuit et six postes en accès libre.</p>
      </div>
      <div class="carte carte--mise-en-avant">
        <h2>Ateliers du samedi</h2>
        <p>Lecture pour les tout-petits, initiation à l'informatique, club de lecture.</p>
      </div>
    </main>
  </div>
</body>
</html>
```

La troisième carte porte deux classes : `carte`, comme les autres, et `carte--mise-en-avant`, une variante qui ne changera que ce qui la distingue. Le double tiret n'a rien de spécial pour le navigateur : c'est une convention entre développeurs pour signaler une variante.

## 07.2 - Écrire la feuille de style des cartes

Cette fois, le tableau donne le résultat attendu et vous écrivez les règles seul, avec le bit sous la main.

| Sélecteur | Ce que la règle doit faire |
|---|---|
| `*` | `box-sizing: border-box` pour tous les éléments |
| `body` | une police sans empattements avec repli, un fond `#eef1f5`, et `margin: 0`, qui retire la marge que le navigateur met autour de la page |
| `.conteneur` | au plus `800px` de large (`max-width`), centré (`margin: 0 auto`), `20px` d'espace intérieur |
| `.carte` | un fond blanc, une bordure `1px solid #d7dee8`, `20px` d'espace intérieur, `20px` d'espace extérieur en dessous |
| `.carte--mise-en-avant` | un fond `#e8f1fb`, et une bordure gauche `5px solid #0b6bcb` (`border-left`) |

`margin: 0 auto` demande au navigateur de répartir l'espace restant à parts égales à gauche et à droite : avec une largeur limitée, le bloc se centre. Et `max-width` plutôt que `width` : le bloc ne dépasse pas 800 px sur un grand écran, mais peut rétrécir sur un petit.

Enregistrez et rechargez : trois cartes blanches, séparées par le gris de la page, et une troisième bleutée, avec un trait épais sur son bord gauche seulement.

```verify
C=~/byte-layers/web/basics/cartes.css
if [ ! -f "$C" ]; then
  echo "Le fichier $C n'existe pas. Créez cartes.css à côté de cartes.html, puis enregistrez."
  exit 1
fi
rule() { perl -0pe 's{/\*.*?\*/}{}gs; s/[\r\n]/ /g' "$C" | grep -oE '[^{}]+\{[^}]*\}' | grep -E "(^|[ ,])$1[ ,]*\{"; }
if ! rule '\*' | grep -qE 'box-sizing:[[:space:]]*border-box'; then
  echo "Il manque la règle * { box-sizing: border-box; }."
  exit 1
fi
if ! rule body | grep -qE 'margin:[[:space:]]*0'; then
  echo "La règle body doit retirer la marge de la page : margin: 0;"
  exit 1
fi
if ! rule '\.conteneur' | grep -q 'max-width'; then
  echo "La règle .conteneur doit limiter la largeur : max-width: 800px;"
  exit 1
fi
if ! rule '\.conteneur' | grep -qE 'margin(-left|-right)?:[^;}]*auto'; then
  echo "La règle .conteneur doit centrer le bloc : margin: 0 auto;"
  exit 1
fi
if ! rule '\.carte' | grep -q 'padding'; then
  echo "La règle .carte doit donner un espace intérieur : padding: 20px;"
  exit 1
fi
if ! rule '\.carte' | grep -q 'margin'; then
  echo "La règle .carte doit séparer les cartes : margin-bottom: 20px;"
  exit 1
fi
if ! rule '\.carte' | grep -qE 'border:[^;}]*solid'; then
  echo "La bordure de .carte demande trois informations : border: 1px solid #d7dee8;"
  exit 1
fi
if ! rule '\.carte--mise-en-avant' | grep -qE 'border-left:[^;}]*solid'; then
  echo "La règle .carte--mise-en-avant doit tracer une bordure gauche : border-left: 5px solid #0b6bcb;"
  exit 1
fi
echo "Les cartes sont aérées : padding dedans, marge dehors, un conteneur centré et une variante."
```

````solution
```css
* {
  box-sizing: border-box;
}

body {
  font-family: system-ui, "Segoe UI", sans-serif;
  background-color: #eef1f5;
  margin: 0;
}

.conteneur {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.carte {
  background-color: #fff;
  border: 1px solid #d7dee8;
  padding: 20px;
  margin-bottom: 20px;
}

.carte--mise-en-avant {
  background-color: #e8f1fb;
  border-left: 5px solid #0b6bcb;
}
```
````

## 07.3 - Voir la boîte, puis le piège de la largeur

Clic droit sur une carte, **Inspecter**. Dans Chrome et Edge, descendez tout en bas de l'onglet **Styles**, ou ouvrez l'onglet **Calculé** (*Computed*) ; dans Firefox, ouvrez l'onglet **Mise en page** (*Layout*). Un schéma en couches apparaît : le contenu au centre, puis *padding*, *border* et *margin*, avec leurs valeurs en pixels. Survolez chaque couche : le navigateur la surligne dans la page.

Si votre fenêtre fait plus de 800 px de large, inspectez maintenant le `<div class="conteneur">` : le schéma donne 760 de contenu, plus 20 de padding de chaque côté, soit 800 px. Faites alors l'essai du piège : transformez la règle `*` en commentaire (sélectionnez-la, Cmd+/ ou Ctrl+/), enregistrez, rechargez, et réinspectez le conteneur. Il mesure désormais **840 px** : 800 de contenu, et les 40 px de padding ajoutés autour. Les cartes ont grandi de la même façon.

Rétablissez la règle `*`, enregistrez, rechargez : le conteneur revient à 800 px.

```verify
C=~/byte-layers/web/basics/cartes.css
if ! perl -0pe 's{/\*.*?\*/}{}gs' "$C" 2>/dev/null | grep -qE 'box-sizing:[[:space:]]*border-box'; then
  echo "La règle * { box-sizing: border-box; } est absente ou encore en commentaire : rétablissez-la, puis enregistrez."
  exit 1
fi
echo "box-sizing: border-box est rétabli : width désigne de nouveau la boîte entière."
```

> 📖 [Le modèle de boîte (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Styling_basics/Box_model) · [La propriété box-sizing (MDN)](https://developer.mozilla.org/fr/docs/Web/CSS/Reference/Properties/box-sizing) · [Inspecter le modèle de boîte dans Firefox (en anglais)](https://firefox-source-docs.mozilla.org/devtools-user/page_inspector/how_to/examine_and_edit_the_box_model/)

## Récap

- L'onglet **Réseau** montre chaque requête d'une page, son code de statut et son type ; une page ouverte depuis le disque (`file://`) n'a pas de code de statut.
- Sans son CSS, une page garde tout son contenu ; sans son JavaScript, elle perd son comportement ; dans les deux cas, sans message.
- Un **squelette** valide tient en quelques lignes ; sans `charset`, les accents dépendent d'une devinette.
- Un lien interne demande un `id` ; un chemin d'image doit être exact, majuscules comprises, même si votre disque les ignore.
- Les balises **sémantiques** ne changent rien à l'écran et dessinent le plan que lisent les lecteurs d'écran.
- Une classe se crée des deux côtés, dans le HTML et dans le CSS, avec le même nom ; l'**inspecteur** montre les règles appliquées, barrées ou absentes.
- Le **modèle de boîte** se lit dans l'inspecteur ; sans `box-sizing: border-box`, le padding s'ajoute à la largeur.

## Questions

```quiz
title: "Les bases HTML et CSS, sur votre machine"
tracksProgress: false
showNotice: false
questions:
  - prompt: "Vous écrivez une règle `.banniere` dans le CSS, et elle ne fait rien. Que regardez-vous en premier ?"
    answers:
      - "Que la classe est écrite exactement pareil dans le HTML, et que les deux fichiers sont enregistrés"
      - "Que le navigateur est à jour"
      - "Le validateur HTML"
    correct: 1
    explanation: "Une classe mal orthographiée d'un côté ou un fichier non enregistré : les deux pannes les plus fréquentes, sans aucun message. L'inspecteur montre si la règle s'applique."
  - prompt: "Votre image s'affiche sur votre Mac avec `src=\"Images/ville.svg\"`, alors que le dossier s'appelle `images`. Que se passera-t-il en ligne ?"
    answers:
      - "Rien de différent"
      - "Sur un serveur Linux, l'image ne sera pas trouvée : la casse y compte"
      - "Le navigateur corrigera le chemin"
    correct: 2
    explanation: "Le disque du Mac ignore la casse par défaut ; la plupart des serveurs tournent sous Linux, où `Images` et `images` sont deux dossiers différents."
  - prompt: "Sans `box-sizing: border-box`, un conteneur a `max-width: 800px` et `padding: 20px`. Quelle largeur mesure l'inspecteur sur un grand écran ?"
    answers:
      - "800 px"
      - "760 px"
      - "840 px : 800 de contenu, plus 20 de padding de chaque côté"
    correct: 3
    explanation: "Par défaut, `width` et `max-width` ne règlent que le contenu ; le padding s'ajoute autour."
```

Vous savez écrire une page, lui donner du sens et l'habiller. Il reste à faire la vôtre, sans guide : c'est le challenge [Mon portfolio, version 1](https://byte-layers.com/fr/challenges/portfolio-v1-challenge).
