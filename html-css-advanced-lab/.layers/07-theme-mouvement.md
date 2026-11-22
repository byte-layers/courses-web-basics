---
title: "07 - Le thème en variables, survol et transitions"
description: "Ranger les couleurs de la page dans des variables CSS, changer de thème en une ligne, ajouter des effets au survol et au focus avec des transitions, une animation à l'arrivée, et respecter prefers-reduced-motion"
---

La couleur d'accent de la page est écrite à plusieurs endroits de `style.css`, la couleur des bordures aussi. Vous les rangez dans des **variables**, pour changer de thème en une ligne, puis vous faites bouger la page sans gêner ceux que le mouvement dérange.

## 07.1 - Les couleurs du thème en variables

Une variable CSS se déclare sur `:root`, avec deux tirets devant son nom, et se lit avec `var()`. Vous en déclarez trois, une par rôle de couleur.

| Variable | Valeur de départ | Où elle sert |
|---|---|---|
| `--accent` | `rgb(219, 39, 119)` | le fond de `.bouton` |
| `--texte` | `rgb(30, 41, 59)` | la couleur du texte de `body` |
| `--bordure` | `rgb(203, 213, 225)` | les bordures de `.entete` et de `.carte` |

🚧 **À compléter :** ajoutez cette règle en haut de `style.css`, sous `* { box-sizing: border-box; }`, puis remplacez chaque couleur des règles concernées par sa variable, et ajoutez `color: var(--texte);` à `body`.

```css
:root {
  --accent: rgb(219, 39, 119);
  /* TODO : --texte et --bordure */
}
```

Changez ensuite la valeur de `--accent` en `rgb(124, 58, 237)`, un violet, enregistrez et rechargez : le bouton change de couleur. Remettez le rose, ou gardez le violet : c'est votre thème.

```verify
C=$(tr -d '\n' < ~/byte-layers/web/advanced/style.css 2>/dev/null)
echo "$C" | grep -Eq ':root[[:space:]]*\{[^}]*--accent[[:space:]]*:' || { echo "Il manque la variable --accent, déclarée dans une règle :root."; exit 1; }
[ "$(echo "$C" | grep -oE ':root[[:space:]]*\{[^}]*\}' | grep -oE -- '--[a-z-]+[[:space:]]*:' | wc -l)" -ge 3 ] || { echo "La règle :root doit déclarer trois variables : --accent, --texte et --bordure."; exit 1; }
[ "$(echo "$C" | grep -oE 'var\([[:space:]]*--' | wc -l)" -ge 4 ] || { echo "Les variables ne servent pas encore assez : remplacez les couleurs de .bouton, body, .entete et .carte par var(--…)."; exit 1; }
echo "$C" | grep -Eq '\.bouton[[:space:]]*\{[^}]*background-color:[[:space:]]*var\([[:space:]]*--accent' || { echo "Le fond de .bouton n'utilise pas encore var(--accent)."; exit 1; }
echo "Les couleurs du thème sont rangées dans trois variables."
```

```hint
Dans `.entete` : `border-bottom: 1px solid var(--bordure);`. Dans `.carte` : `border: 1px solid var(--bordure);`. Une variable remplace une valeur, pas une propriété entière.
```

## 07.2 - Survol et focus, avec une transition dans les deux sens

Un effet au survol (`:hover`) s'écrit toujours avec son équivalent au clavier (`:focus-visible`), dans la même règle. La transition, elle, se déclare sur **l'état normal** : posée dans `:hover`, elle ne jouerait qu'à l'arrivée de la souris.

🚧 **À compléter :**

```css
.bouton {
  /* … ses propriétés de l'étape 1 … */
  /* TODO : une transition de 0.3s sur background-color */
}

/* TODO : une règle pour .bouton au survol ET au focus clavier, avec un fond plus foncé : rgb(157, 23, 77) */

.carte {
  /* … ses propriétés de l'étape 3 … */
  transition: transform 0.3s;
}

.carte:hover {
  transform: translateY(-4px);
}
```

Survolez le bouton, puis éloignez la souris : la couleur change doucement à l'aller **et** au retour. Appuyez sur Tab jusqu'au bouton : le même effet apparaît au clavier.

> **🧪 Manip — la transition sur le survol**
>
> 1. Déplacez `transition: background-color 0.3s;` de `.bouton` vers la règle du survol. Enregistrez, rechargez, survolez puis quittez le bouton.
>
> *Observé : l'aller est doux, le retour est sec. Au départ de la souris, c'est l'état normal qui s'applique, et il n'a plus de transition. Remettez-la dans `.bouton`.*

```verify
C=$(tr -d '\n' < ~/byte-layers/web/advanced/style.css 2>/dev/null)
echo "$C" | grep -Eq '(^|[}[:space:]])\.bouton[[:space:]]*\{[^}]*transition:' || { echo "La règle .bouton (l'état normal) n'a pas de transition."; exit 1; }
echo "$C" | grep -Eq '\.bouton:hover' || { echo "Il manque l'effet au survol : .bouton:hover."; exit 1; }
echo "$C" | grep -Eq '\.bouton:focus(-visible)?' || { echo "L'effet du survol n'existe pas au clavier : ajoutez .bouton:focus-visible à la règle du survol."; exit 1; }
echo "Le bouton réagit à la souris et au clavier, dans les deux sens."
```

## 07.3 - Une animation à l'arrivée, et moins de mouvement sur demande

Une animation joue toute seule, au chargement, d'après des étapes décrites dans `@keyframes`. Le titre va apparaître en montant de quelques pixels.

```css
@keyframes apparition {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

h1 {
  animation: apparition 0.6s ease-out;
}
```

Ajoutez ces deux règles à `style.css`, avant la media query, et rechargez : le titre monte en apparaissant.

Pour une personne qui a demandé à son système de **réduire les animations**, ce mouvement peut donner des vertiges. La media query `prefers-reduced-motion: reduce` permet de le couper, avec les transitions.

🚧 **À compléter :** à la fin de `style.css`, ajoutez la media query qui coupe l'animation du titre et les transitions du bouton et des cartes.

```css
@media (prefers-reduced-motion: reduce) {
  /* TODO : h1 sans animation ; .bouton et .carte sans transition */
}
```

Pour la tester sans changer le réglage de votre système, dans Chrome : menu ⋮ des outils de développement, **More tools**, **Rendering**, puis *Emulate CSS media feature prefers-reduced-motion* sur `reduce`. Rechargez : le titre apparaît sans bouger.

```verify
C=$(tr -d '\n' < ~/byte-layers/web/advanced/style.css 2>/dev/null)
echo "$C" | grep -Eq '@keyframes[[:space:]]+[a-zA-Z-]+' || { echo "Il manque la règle @keyframes de l'animation du titre."; exit 1; }
echo "$C" | grep -Eq 'prefers-reduced-motion:[[:space:]]*reduce[[:space:]]*\)[[:space:]]*\{.*(animation|animation-name):[[:space:]]*none' || { echo "Il manque la media query (prefers-reduced-motion: reduce) qui met animation: none sur le titre."; exit 1; }
echo "$C" | grep -Eq 'prefers-reduced-motion:[[:space:]]*reduce[[:space:]]*\)[[:space:]]*\{.*transition:[[:space:]]*none' || { echo "La media query prefers-reduced-motion doit aussi couper les transitions : transition: none."; exit 1; }
echo "La page bouge, sauf pour qui a demandé moins de mouvement."
```

````solution
```css
:root {
  --accent: rgb(219, 39, 119);
  --texte: rgb(30, 41, 59);
  --bordure: rgb(203, 213, 225);
}

body {
  font-family: system-ui, sans-serif;
  margin: 0;
  color: var(--texte);
}

.bouton {
  display: inline-block;
  background-color: var(--accent);
  color: white;
  padding: 8px 16px;
  margin-top: 24px;
  text-decoration: none;
  transition: background-color 0.3s;
}

.bouton:hover,
.bouton:focus-visible {
  background-color: rgb(157, 23, 77);
}

.carte {
  padding: 16px;
  border: 1px solid var(--bordure);
  border-radius: 8px;
  transition: transform 0.3s;
}

.carte:hover {
  transform: translateY(-4px);
}

@keyframes apparition {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

h1 {
  animation: apparition 0.6s ease-out;
}

@media (prefers-reduced-motion: reduce) {
  h1 {
    animation: none;
  }

  .bouton,
  .carte {
    transition: none;
  }
}
```

Dans `.entete`, la bordure devient `border-bottom: 1px solid var(--bordure);`.
````

> 📖 [Les propriétés personnalisées (MDN)](https://developer.mozilla.org/fr/docs/Web/CSS/Using_CSS_custom_properties) · [Les transitions CSS (MDN)](https://developer.mozilla.org/fr/docs/Web/CSS/CSS_transitions/Using_CSS_transitions) · [prefers-reduced-motion (MDN)](https://developer.mozilla.org/fr/docs/Web/CSS/@media/prefers-reduced-motion)
