---
title: "05 - Une page entièrement adaptative"
description: "Voir la page sur un téléphone simulé, ajouter la meta viewport et les fondations, remplacer une largeur fixe par une largeur maximale, écrire une media query mobile-first, puis passer le test décisif de 360 à 1600 px"
---

La page a un entête, une galerie, des projets et un formulaire. Elle a été écrite sur un écran d'ordinateur ; vous allez la regarder sur un téléphone simulé, puis la rendre adaptative, du plus petit écran au plus grand.

## 05.1 - Voir la page sur un téléphone simulé

Les outils de développement ont un **mode appareil**, qui affiche la page à la taille d'un téléphone. Ouvrez-les (F12, ou clic droit, **Inspecter**), puis cliquez sur l'icône du téléphone et de la tablette en haut du panneau (raccourci Ctrl+Maj+M, ou Cmd+Maj+M sous macOS). Dans la liste en haut de la page, choisissez un téléphone, par exemple un *iPhone SE* ou un *Pixel 7*.

> **🧪 Manip — une page sans meta viewport**
>
> 1. Regardez la page en mode appareil, sur un téléphone.
>
> *Observé : tout est minuscule, comme une page d'ordinateur vue de loin. Le navigateur du téléphone, faute d'instruction, fait comme si l'écran mesurait environ 980 px de large, puis réduit l'ensemble.*

## 05.2 - La meta viewport et les fondations

Une ligne dans le `head` dit au navigateur d'utiliser la vraie largeur de l'écran. Ajoutez-la dans `index.html`, juste sous le `meta charset` :

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

Ajoutez ensuite ces deux règles **en haut** de `style.css`. La première fait compter le padding et la bordure dans la largeur d'une boîte, ce qui évite qu'une boîte à `100%` déborde de son padding ; la seconde empêche toute image de dépasser de son parent.

```css
* {
  box-sizing: border-box;
}

img {
  max-width: 100%;
  height: auto;
}
```

Rechargez en mode appareil : le texte a une taille normale, et la page occupe la largeur du téléphone.

## 05.3 - Une largeur maximale, pas une largeur fixe

Sur un grand écran, le texte s'étale sur toute la largeur, et les lignes deviennent trop longues à lire. On limite donc la largeur du contenu principal.

> **🧪 Manip — la largeur fixe**
>
> 1. Ajoutez cette règle : `main { width: 960px; margin: 0 auto; padding: 0 16px; }`. Enregistrez, rechargez.
> 2. En mode appareil, choisissez **Responsive** dans la liste, et tapez `360` dans le champ de largeur.
>
> *Observé : une barre de défilement horizontale apparaît ; `main` garde ses 960 px sur un écran de 360 px, et dépasse de 600 px.*

🚧 **À compléter :** remplacez la propriété qui fixe la largeur par celle qui ne fixe qu'une limite haute, puis vérifiez à `360px` que la barre horizontale a disparu, et à `1600px` que le contenu reste centré sur `960px`.

```css
main {
  /* TODO : au plus 960px de large, et rétrécit sur un petit écran */
  margin: 0 auto;
  padding: 0 16px;
}
```

## 05.4 - Une media query, en mobile-first

Sur un téléphone, le logo et le menu tiennent mal sur une ligne. En **mobile-first**, on écrit d'abord le style du téléphone, sans condition : le logo au-dessus du menu, centrés. Puis une media query **`min-width`** rétablit la ligne à partir de `700px`. La même media query réserve aux grands écrans les deux colonnes du projet vedette.

🚧 **À compléter :** dans `style.css`, ajoutez à la règle `.entete` la colonne du téléphone, retirez `grid-column: span 2` de la règle `.vedette`, puis écrivez la media query **à la fin** du fichier.

```css
.entete {
  display: flex;
  flex-direction: column;   /* téléphone : le logo au-dessus du menu */
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px;
  border-bottom: 1px solid rgb(203, 213, 225);
}

@media (min-width: 700px) {
  /* TODO : .entete, en ligne */
  /* TODO : .vedette, sur deux colonnes */
}
```

À `360px`, le logo est au-dessus du menu ; à partir de `700px`, ils reviennent sur une ligne. Passez lentement de `690` à `710px` dans le champ de largeur pour voir la bascule.

> **🧪 Manip — min-width ou max-width**
>
> 1. Remplacez `min-width` par `max-width` dans la media query. Enregistrez, testez à `360px`, puis à `1200px`.
>
> *Observé : tout est inversé, l'entête est en ligne sur le téléphone et en colonne sur l'ordinateur. `max-width: 700px` veut dire « au plus 700 px ». Remettez `min-width`.*

## 05.5 - Le test décisif : de 360 à 1600 px

En mode appareil **Responsive**, faites glisser le bord de la page de `360px` à `1600px`, lentement. À aucune largeur la page ne doit avoir de barre de défilement horizontale. Si une barre apparaît, survolez les éléments dans le panneau HTML : celui qui dépasse du cadre est le coupable, souvent une largeur fixe ou une image.

```verify
D=~/byte-layers/web/advanced
H=$(tr -d '\n' < "$D/index.html")
echo "$H" | grep -Eiq '<meta[^>]+name="viewport"[^>]*width=device-width' || { echo "index.html n'a pas la balise meta viewport."; exit 1; }
C=$(tr -d '\n' < "$D/style.css")
echo "$C" | grep -Eq '\*[[:space:]]*\{[^}]*box-sizing:[[:space:]]*border-box' || { echo "Il manque la règle * { box-sizing: border-box; }."; exit 1; }
echo "$C" | grep -Eq '(^|[},[:space:]])img[[:space:]]*\{[^}]*max-width:[[:space:]]*100%' || { echo "Il manque la règle img { max-width: 100%; height: auto; }."; exit 1; }
echo "$C" | grep -Eq 'main[[:space:]]*\{[^}]*max-width:[[:space:]]*960px' || { echo "main n'a pas de max-width: 960px."; exit 1; }
BIG=$(grep -oE '(^|[^-a-z])width:[[:space:]]*[0-9]+px' "$D/style.css" | grep -oE '[0-9]+' | awk '$1 >= 400' | head -1)
[ -z "$BIG" ] || { echo "style.css a encore une largeur fixe de ${BIG}px : remplacez width par max-width."; exit 1; }
echo "$C" | grep -Eq '@media[^{]*min-width[^{]*\{.*\.entete[[:space:]]*\{[^}]*flex-direction:[[:space:]]*row' || { echo "Il manque la media query (min-width: 700px) qui remet .entete en ligne."; exit 1; }
echo "La page a sa meta viewport, ses fondations, une largeur maximale et une media query mobile-first."
```

```hint
Si la vérification signale une largeur fixe, cherchez `width:` dans `style.css` (Ctrl+F, ou Cmd+F) : seules des valeurs en `%` ou des `max-width` doivent rester pour les grandes largeurs.
```

````solution
Dans `index.html`, sous le `meta charset` :

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

Dans `style.css`, les règles qui changent :

```css
* {
  box-sizing: border-box;
}

img {
  max-width: 100%;
  height: auto;
}

main {
  max-width: 960px;
  margin: 0 auto;
  padding: 0 16px;
}

.entete {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px;
  border-bottom: 1px solid rgb(203, 213, 225);
}

.vedette {
  background-color: rgb(252, 231, 243);
}

@media (min-width: 700px) {
  .entete {
    flex-direction: row;
  }

  .vedette {
    grid-column: span 2;
  }
}
```
````

> 📖 [Le responsive design (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/CSS_layout/Responsive_Design) · [La balise meta viewport (MDN)](https://developer.mozilla.org/fr/docs/Web/HTML/Guides/Viewport_meta_element) · [Le mode appareil de Chrome (en anglais)](https://developer.chrome.com/docs/devtools/device-mode)
