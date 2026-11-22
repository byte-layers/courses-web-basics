---
title: "03 - La grille de projets en CSS Grid"
description: "Ranger six projets dans une grille qui choisit seule son nombre de colonnes, puis mettre un projet en vedette sur deux colonnes"
---

La galerie de l'étape 2 range ses photos ligne par ligne : une photo de la deuxième ligne ne s'aligne pas forcément sous une photo de la première. Pour les projets, on veut des colonnes alignées : c'est le travail de CSS Grid.

## 03.1 - Six projets dans une grille

Collez cette section dans `index.html`, dans `main`, après la galerie. Chaque projet est un `article` de classe `carte`, et le premier a aussi la classe `vedette`.

```html
<section id="projets">
  <h2>Projets</h2>
  <div class="projets">
    <article class="carte vedette"><h3>Club de rando</h3><p>Le site du club, avec son formulaire d'inscription.</p></article>
    <article class="carte"><h3>Météo du jour</h3><p>La météo de Toulouse en une page.</p></article>
    <article class="carte"><h3>Quiz Pyrénées</h3><p>Dix questions sur les sommets.</p></article>
    <article class="carte"><h3>Liste de courses</h3><p>Une liste qu'on coche.</p></article>
    <article class="carte"><h3>Recettes</h3><p>Mes recettes préférées, en tableau.</p></article>
    <article class="carte"><h3>Portfolio v1</h3><p>La première version de cette page.</p></article>
  </div>
</section>
```

Pour que la grille s'adapte sans aucune règle par largeur d'écran, ses colonnes s'écrivent avec `repeat(auto-fit, minmax(220px, 1fr))`, comme dans le bit sur Grid.

| Propriété | Sur quoi | Rôle |
|---|---|---|
| `display: grid` | `.projets` | ses enfants se rangent dans une grille |
| `grid-template-columns: repeat(auto-fit, minmax(220px, 1fr))` | `.projets` | autant de colonnes que possible, d'au moins `220px` |
| `gap: 24px` | `.projets` | l'espace entre les lignes et entre les colonnes |
| `grid-column: span 2` | `.vedette` | le projet occupe deux colonnes |

🚧 **À compléter :**

```css
.projets {
  /* TODO : une grille, des colonnes d'au moins 220px, 24px d'espace */
}

.carte {
  padding: 16px;
  border: 1px solid rgb(203, 213, 225);
  border-radius: 8px;
}

.vedette {
  /* TODO : deux colonnes */
  background-color: rgb(252, 231, 243);
}
```

Rechargez, puis faites varier la largeur de la fenêtre : trois ou quatre colonnes sur un grand écran, deux sur une fenêtre moyenne, une seule sur une fenêtre étroite.

> **🧪 Manip — l'inspecteur de grille**
>
> 1. Clic droit sur une carte, **Inspecter**. Dans le panneau HTML, à côté de `<div class="projets">`, un badge **grid** est apparu.
> 2. Cliquez dessus.
>
> *Observé : le navigateur trace les colonnes et les lignes de la grille par-dessus la page, avec leurs numéros. Le projet vedette couvre deux colonnes.*

```verify
D=~/byte-layers/web/advanced
[ "$(grep -o 'class="carte' "$D/index.html" | wc -l)" -ge 6 ] || { echo "index.html doit contenir les six projets de classe carte."; exit 1; }
C=$(tr -d '\n' < "$D/style.css")
echo "$C" | grep -Eq '\.projets[[:space:]]*\{[^}]*display:[[:space:]]*grid' || { echo "La règle .projets n'a pas display: grid."; exit 1; }
echo "$C" | grep -Eq '\.projets[[:space:]]*\{[^}]*grid-template-columns:[^;]*(auto-fit|auto-fill)' || { echo "Les colonnes de .projets sont fixes : écrivez grid-template-columns: repeat(auto-fit, minmax(220px, 1fr))."; exit 1; }
echo "$C" | grep -Eq '\.vedette[[:space:]]*\{[^}]*grid-column:[[:space:]]*span 2' || { echo "Le projet vedette n'occupe pas deux colonnes : grid-column: span 2 dans .vedette."; exit 1; }
echo "La grille de projets s'adapte seule, et la vedette couvre deux colonnes."
```

```hint
`grid-template-columns` et `gap` vont sur le conteneur, `.projets` ; `grid-column` va sur l'enfant, `.vedette`. Vérifiez aussi l'orthographe : `auto-fit`, `minmax`, et une virgule entre les deux valeurs de `minmax`.
```

> 💡 **Remarque.** Sur une fenêtre étroite, la grille n'a qu'une colonne, et `span 2` lui en ajoute une seconde, vide et de largeur nulle : la carte vedette dépasse alors les autres de la largeur d'un `gap`. Pour l'éviter, on réserve `span 2` aux grands écrans, dans une media query : c'est l'outil de l'étape 5.

````solution
```css
.projets {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 24px;
}

.carte {
  padding: 16px;
  border: 1px solid rgb(203, 213, 225);
  border-radius: 8px;
}

.vedette {
  grid-column: span 2;
  background-color: rgb(252, 231, 243);
}
```
````

> 📖 [Les grilles CSS (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/CSS_layout/Grids) · [Inspecter une grille dans Firefox (MDN, en anglais)](https://firefox-source-docs.mozilla.org/devtools-user/page_inspector/how_to/examine_grid_layouts/index.html)
