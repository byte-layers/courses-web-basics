---
title: "08 - Refaire un bloc du portfolio avec Bootstrap"
description: "Refaire les projets du portfolio dans une page à part avec Bootstrap : le charger depuis un CDN, sa grille container, row et col, ses cartes et ses boutons, puis comparer avec ce que vous avez écrit à la main"
---

Aux étapes 2 et 3, vous avez écrit à la main la disposition des projets, avec Flexbox et Grid. Vous refaites ce bloc dans une page à part avec **Bootstrap**, pour voir ce que le framework fait à votre place, et ce qu'il vous laisse.

## 08.1 - Une page qui charge Bootstrap

Créez un fichier `bootstrap.html` dans votre dossier, à côté de `index.html`, et collez-y ce squelette. Il ne charge pas `style.css` : seul Bootstrap habille cette page.

🚧 **À compléter :**

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Projets, version Bootstrap</title>
  <!-- TODO : la balise link vers Bootstrap 5.3.8 sur jsDelivr -->
</head>
<body>
  <main class="container py-4">
    <h1>Projets</h1>
    <!-- TODO : une rangée de trois colonnes, une carte par projet -->
  </main>
</body>
</html>
```

La balise qui charge la feuille de style de Bootstrap, avec sa version écrite dans l'adresse, est celle du bit sur Bootstrap :

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css">
```

Ouvrez `bootstrap.html` dans le navigateur : la police et les marges ont déjà changé. C'est la remise à zéro de Bootstrap, qui s'applique avant même la première classe.

## 08.2 - Trois cartes dans la grille

Chaque projet est une **carte** Bootstrap, rangée dans une colonne `col-md-4`. Voici la carte du premier projet, à écrire trois fois, avec le nom et le texte de chaque projet de votre page :

```html
<div class="col-md-4">
  <article class="card h-100">
    <img src="images/sommet.svg" class="card-img-top" alt="Le site du club de rando : une montagne sur fond bleu">
    <div class="card-body">
      <h2 class="h5 card-title">Club de rando</h2>
      <p class="card-text">Le site du club, avec son formulaire d'inscription.</p>
      <a href="index.html#projets" class="btn btn-primary">Voir le projet</a>
    </div>
  </article>
</div>
```

| Classe | Ce qu'elle fait | Ce que vous aviez écrit |
|---|---|---|
| `row` | `display: flex; flex-wrap: wrap;` | `.galerie`, étape 2 |
| `col-md-4` | un tiers de la largeur à partir de `768px`, toute la largeur en dessous | la media query de l'étape 5 |
| `g-4` (sur `row`) | l'espace entre les colonnes | `gap`, étapes 2 et 3 |
| `card`, `card-body` | la bordure, les coins arrondis, le padding | `.carte`, étape 3 |
| `h-100` | des cartes de même hauteur sur une ligne | rien |
| `btn btn-primary` | un bouton bleu, avec ses états de survol et de focus | `.bouton`, étapes 1 et 7 |

Mettez les trois colonnes dans une `<div class="row g-4">`, enregistrez, rechargez, puis réduisez la fenêtre sous `768px` : les cartes s'empilent.

> **🧪 Manip — sans la feuille de Bootstrap**
>
> 1. Mettez la balise `<link>` de Bootstrap en commentaire (`<!--` avant, `-->` après), enregistrez, rechargez.
>
> *Observé : les classes sont toujours dans le HTML, mais elles ne font plus rien ; les images s'affichent à leur taille réelle, les cartes s'empilent. Une classe n'est qu'un nom : sans la feuille qui la définit, rien ne s'applique. Retirez le commentaire.*

## 08.3 - Ce que Bootstrap ne fait pas

Bootstrap a donné la disposition, les cartes et les boutons. Il n'a rien fait pour le **sens** : l'`alt` de chaque image, le niveau de chaque titre, l'ordre du contenu restent ceux que vous avez écrits. Vérifiez votre page avec la grille de l'étape 6 : chaque image a-t-elle un `alt` qui la décrit, les titres vont-ils de `h1` à `h2` sans saut ?

Comparez aussi le poids : votre `style.css` fait quelques kilo-octets, la feuille de Bootstrap environ `230 Ko`. Onglet **Network** (Réseau) des outils de développement, rechargez : la ligne `bootstrap.min.css` donne sa taille transférée.

```verify
F=~/byte-layers/web/advanced/bootstrap.html
[ -f "$F" ] || { echo "Il n'y a pas de bootstrap.html dans ~/byte-layers/web/advanced."; exit 1; }
H=$(tr -d '\n' < "$F")
echo "$H" | grep -Eq '<link[^>]+href="https://cdn\.jsdelivr\.net/npm/bootstrap@5\.3\.8/dist/css/bootstrap(\.min)?\.css"' || { echo "bootstrap.html ne charge pas Bootstrap 5.3.8 : recopiez la balise link dans le head."; exit 1; }
echo "$H" | grep -Eq 'class="([^"]* )?container[ "]' || { echo "Il manque l'élément de classe container."; exit 1; }
echo "$H" | grep -Eq 'class="row[ "]' || { echo "Il manque la rangée : <div class=\"row g-4\">."; exit 1; }
[ "$(grep -o 'col-md-4' "$F" | wc -l)" -ge 3 ] || { echo "La rangée doit contenir trois colonnes col-md-4."; exit 1; }
[ "$(grep -oE 'class="card[ "]' "$F" | wc -l)" -ge 3 ] || { echo "Chaque colonne doit contenir une carte, de classe card."; exit 1; }
[ "$(grep -o '<img' "$F" | wc -l)" -eq "$(grep -oE '<img[^>]*alt="[^"]+"' "$F" | wc -l)" ] || { echo "Une image de bootstrap.html n'a pas de texte alternatif : Bootstrap ne l'écrit pas pour vous."; exit 1; }
grep -Eq '<h[3-6]' "$F" && ! grep -q '<h2' "$F" && { echo "Les titres des cartes sautent un niveau : après le h1, des h2."; exit 1; }
echo "Les trois projets sont dans la grille de Bootstrap, avec leurs alt."
```

```hint
L'ordre d'imbrication compte : `container`, puis `row g-4`, puis trois `col-md-4`, chacune avec sa `card`. Une `card` directement dans la `row`, sans colonne, prend toute la largeur.
```

````solution
```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Projets, version Bootstrap</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css">
</head>
<body>
  <main class="container py-4">
    <h1>Projets</h1>
    <div class="row g-4">
      <div class="col-md-4">
        <article class="card h-100">
          <img src="images/sommet.svg" class="card-img-top" alt="Le site du club de rando : une montagne sur fond bleu">
          <div class="card-body">
            <h2 class="h5 card-title">Club de rando</h2>
            <p class="card-text">Le site du club, avec son formulaire d'inscription.</p>
            <a href="index.html#projets" class="btn btn-primary">Voir le projet</a>
          </div>
        </article>
      </div>
      <div class="col-md-4">
        <article class="card h-100">
          <img src="images/sommet.svg" class="card-img-top" alt="La météo du jour : un sommet sous un ciel clair">
          <div class="card-body">
            <h2 class="h5 card-title">Météo du jour</h2>
            <p class="card-text">La météo de Toulouse en une page.</p>
            <a href="index.html#projets" class="btn btn-primary">Voir le projet</a>
          </div>
        </article>
      </div>
      <div class="col-md-4">
        <article class="card h-100">
          <img src="images/sommet.svg" class="card-img-top" alt="Le quiz Pyrénées : un sommet enneigé">
          <div class="card-body">
            <h2 class="h5 card-title">Quiz Pyrénées</h2>
            <p class="card-text">Dix questions sur les sommets.</p>
            <a href="index.html#projets" class="btn btn-primary">Voir le projet</a>
          </div>
        </article>
      </div>
    </div>
  </main>
</body>
</html>
```
````

> 📖 [Bootstrap, bien démarrer (en anglais)](https://getbootstrap.com/docs/5.3/getting-started/introduction/) · [Les cartes de Bootstrap (en anglais)](https://getbootstrap.com/docs/5.3/components/card/) · [Les gouttières de la grille (en anglais)](https://getbootstrap.com/docs/5.3/layout/gutters/)
