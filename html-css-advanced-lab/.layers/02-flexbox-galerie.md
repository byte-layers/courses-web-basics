---
title: "02 - Un entête et une galerie en Flexbox"
description: "Mettre le logo à gauche et le menu à droite avec Flexbox, puis construire une galerie de quatre photos qui passe à la ligne toute seule"
---

À l'étape 1, le logo restait au-dessus du menu, parce que ce sont deux blocs. Flexbox prend la main sur ce rangement : le logo à gauche, le menu à droite, sur la même ligne. Puis vous ajoutez une galerie de photos qui passe à la ligne quand la fenêtre rétrécit.

## 02.1 - Le logo à gauche, le menu à droite

Le conteneur flex est l'élément qui **contient** ceux qu'on veut aligner : pour le logo et le menu, c'est `.entete` ; pour les trois liens, c'est `.menu`. Deux conteneurs imbriqués, chacun range ses enfants directs.

| Propriété | Sur quoi | Rôle |
|---|---|---|
| `display: flex` | `.entete` | le logo et `nav` passent côte à côte |
| `justify-content: space-between` | `.entete` | le premier à gauche, le dernier à droite |
| `align-items: center` | `.entete` | centrés en hauteur, le logo est plus grand que les liens |
| `display: flex` et `gap: 16px` | `.menu` | les liens côte à côte, espacés |

🚧 **À compléter :** dans `style.css`, **supprimez** la règle `.menu li` de l'étape 1 (Flexbox la remplace), complétez `.menu`, et ajoutez ces deux règles.

```css
.entete {
  /* TODO : conteneur flex, logo à gauche et menu à droite, centrés en hauteur */
  padding: 12px 24px;
  border-bottom: 1px solid rgb(203, 213, 225);
}

.logo {
  font-size: 28px;
  font-weight: bold;
  margin: 0;
}

/* TODO : dans .menu, ajoutez display: flex et gap: 16px */
```

Enregistrez et rechargez : le logo est à gauche, les trois liens à droite, sur une seule ligne.

> **🧪 Manip — le flex sur le mauvais élément**
>
> 1. Déplacez `display: flex` de `.entete` vers `.logo`. Enregistrez, rechargez.
> 2. Remettez-le sur `.entete`.
>
> *Observé : le logo et le menu sont de nouveau l'un sous l'autre. `display: flex` sur `.logo` range les enfants du logo, c'est-à-dire son seul texte. La règle va sur le parent.*

```verify
C=$(tr -d '\n' < ~/byte-layers/web/advanced/style.css 2>/dev/null)
echo "$C" | grep -Eq '\.entete[[:space:]]*\{[^}]*display:[[:space:]]*flex' || { echo "La règle .entete n'a pas display: flex."; exit 1; }
echo "$C" | grep -Eq '\.entete[[:space:]]*\{[^}]*justify-content:[[:space:]]*space-between' || { echo "Le logo et le menu ne sont pas encore écartés : justify-content: space-between dans .entete."; exit 1; }
echo "$C" | grep -Eq '\.entete[[:space:]]*\{[^}]*align-items:[[:space:]]*center' || { echo "Le logo et le menu ne sont pas centrés en hauteur : align-items: center dans .entete."; exit 1; }
echo "$C" | grep -Eq '\.menu[[:space:]]*\{[^}]*display:[[:space:]]*flex' || { echo "Les liens ne sont pas rangés par Flexbox : display: flex dans la règle .menu."; exit 1; }
echo "L'entête et le menu sont deux conteneurs flex."
```

```hint
Les quatre propriétés du tableau vont dans deux règles : trois dans `.entete`, deux dans `.menu`. Si la vérification échoue, vérifiez qu'elles sont bien entre les accolades de la bonne règle.
```

## 02.2 - Ajouter une image au dossier

La galerie a besoin d'une image. Cette sous-étape est un **support** : dans l'explorateur de VS Code, créez un dossier `images` (icône **New Folder…**), puis dedans un fichier `sommet.svg`, et collez-y ce dessin. Le SVG est un format d'image écrit en texte : un rectangle bleu et une montagne.

```xml
<svg xmlns="http://www.w3.org/2000/svg" width="400" height="260" viewBox="0 0 400 260">
  <rect width="400" height="260" fill="#bfdbfe"/>
  <polygon points="0,260 150,70 220,160 280,110 400,260" fill="#475569"/>
  <polygon points="150,70 178,105 122,105" fill="#ffffff"/>
</svg>
```

## 02.3 - Une galerie qui passe à la ligne

Collez cette section dans `index.html`, dans `main`, après le bouton. Chaque photo est une `figure` avec sa légende ; le chemin `images/sommet.svg` part du dossier de `index.html`.

```html
<section id="galerie">
  <h2>Galerie</h2>
  <div class="galerie">
    <figure><img src="images/sommet.svg" alt="Le pic du Midi au printemps"><figcaption>Pic du Midi</figcaption></figure>
    <figure><img src="images/sommet.svg" alt="Le cirque de Gavarnie sous la neige"><figcaption>Gavarnie</figcaption></figure>
    <figure><img src="images/sommet.svg" alt="Les crêtes de Bassiès au coucher du soleil"><figcaption>Bassiès</figcaption></figure>
    <figure><img src="images/sommet.svg" alt="Le lac d'Oô en été"><figcaption>Lac d'Oô</figcaption></figure>
  </div>
</section>
```

Rechargez : les quatre images s'empilent, chacune à sa taille réelle. Si une image est cassée et n'affiche que son texte alternatif, vérifiez le nom du dossier et du fichier, casse comprise : `images/sommet.svg`.

| Propriété | Sur quoi | Rôle |
|---|---|---|
| `display: flex`, `flex-wrap: wrap`, `gap: 16px` | `.galerie` | les photos côte à côte, avec passage à la ligne |
| `flex: 1 1 200px` | `.galerie figure` | chaque photo part de `200px`, puis partage l'espace restant |
| `margin: 0` | `.galerie figure` | retire la marge par défaut d'une `figure` |
| `width: 100%` | `.galerie img` | l'image remplit sa `figure` |

🚧 **À compléter :**

```css
.galerie {
  /* TODO : conteneur flex, passage à la ligne, 16px entre les photos */
}

.galerie figure {
  /* TODO : largeur de base de 200px, sans marge */
}

.galerie img {
  width: 100%;
}
```

> **🧪 Manip — sans flex-wrap**
>
> 1. Rétrécissez lentement la fenêtre du navigateur : les photos passent de quatre par ligne à deux, puis à une.
> 2. Retirez `flex-wrap: wrap`, enregistrez, rechargez, et rétrécissez de nouveau.
>
> *Observé : sans passage à la ligne, les quatre photos restent sur une ligne et se compriment, jusqu'à devenir minuscules. Remettez `flex-wrap: wrap`.*

```verify
D=~/byte-layers/web/advanced
[ -f "$D/images/sommet.svg" ] || { echo "Il manque l'image $D/images/sommet.svg."; exit 1; }
H=$(tr -d '\n' < "$D/index.html")
echo "$H" | grep -Eq 'class="galerie"' || { echo "index.html n'a pas encore la section de la galerie."; exit 1; }
[ "$(grep -o '<figure' "$D/index.html" | wc -l)" -ge 4 ] || { echo "La galerie doit contenir quatre figure."; exit 1; }
C=$(tr -d '\n' < "$D/style.css")
echo "$C" | grep -Eq '\.galerie[[:space:]]*\{[^}]*display:[[:space:]]*flex' || { echo "La règle .galerie n'a pas display: flex."; exit 1; }
echo "$C" | grep -Eq '\.galerie[[:space:]]*\{[^}]*flex-wrap:[[:space:]]*wrap' || { echo "La galerie ne passe pas à la ligne : flex-wrap: wrap dans .galerie."; exit 1; }
echo "$C" | grep -Eq '\.galerie figure[[:space:]]*\{[^}]*(flex:[[:space:]]*1 1 200px|flex-basis:[[:space:]]*200px)' || { echo "Les photos n'ont pas de largeur de base : flex: 1 1 200px dans .galerie figure."; exit 1; }
echo "La galerie passe à la ligne, quatre photos de 200px de base."
```

```hint
`flex: 1 1 200px` se pose sur les enfants (`.galerie figure`), et `flex-wrap` sur le conteneur (`.galerie`). Les inverser ne donne rien, sans erreur.
```

````solution
```css
.entete {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px;
  border-bottom: 1px solid rgb(203, 213, 225);
}

.logo {
  font-size: 28px;
  font-weight: bold;
  margin: 0;
}

.menu {
  display: flex;
  gap: 16px;
  list-style: none;
  padding: 0;
}

.galerie {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.galerie figure {
  flex: 1 1 200px;
  margin: 0;
}

.galerie img {
  width: 100%;
}
```
````

> 📖 [Les bases de Flexbox (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/CSS_layout/Flexbox) · [flex-wrap (MDN)](https://developer.mozilla.org/fr/docs/Web/CSS/flex-wrap)
