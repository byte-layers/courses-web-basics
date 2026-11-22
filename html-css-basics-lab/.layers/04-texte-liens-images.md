---
title: "04 - La fiche d'une ville : texte, listes, liens et image"
description: "Écrire la fiche d'une ville avec titres, mise en valeur et deux listes, trois sortes de liens dont un lien interne, puis une image rangée dans un sous-dossier, avec un chemin exact et un texte alternatif"
---

Le bit [Le squelette d'une page HTML, son texte, ses liens et ses images](https://byte-layers.com/fr/bits/html-document) présentait les éléments du texte, les liens et les images. Vous les réunissez ici dans une page : la fiche d'une ville de votre choix. Le squelette, vous savez l'écrire ; cette étape porte sur ce qu'on met dans le `<body>`.

## 04.1 - Le texte et les listes

Créez `ville.html` dans `BASICS`, écrivez-y le squelette de l'étape précédente, avec un `<title>` à votre goût, puis remplissez le `<body>` :

| Élément | Ce qu'il doit contenir |
|---|---|
| un `<h1>` | le nom de la ville |
| un paragraphe | une présentation, avec au moins un mot en `<strong>` et un mot en `<em>` |
| un `<h2>` « À voir » | suivi d'une liste à puces de trois monuments |
| un `<h2>` « Bonnes adresses » | suivi d'une liste numérotée de trois restaurants |

Enregistrez et rechargez. Puis faites l'essai qui montre l'intérêt de `<ol>` : insérez un nouveau `<li>` entre le premier et le deuxième restaurant. Les numéros se recalculent seuls, ce qu'on perd en les tapant à la main. Retirez ensuite ce quatrième restaurant, ou gardez-le : les deux conviennent.

## 04.2 - Trois sortes de liens

Ajoutez, sous les listes, un paragraphe avec trois liens :

| Lien | Ce qu'il fait |
|---|---|
| un lien externe | vers le site de l'office de tourisme ou la page Wikipédia de la ville, dans un nouvel onglet : `target="_blank"` et `rel="noopener"` |
| un lien interne | vers le titre « Bonnes adresses » : `href="#bonnes-adresses"` |
| un lien e-mail | `mailto:` suivi d'une adresse, par exemple `contact@exemple.fr` |

Enregistrez, rechargez, cliquez sur le lien interne : rien ne se passe. C'est le piège du bit : le lien vise un `id` qui n'existe encore nulle part. Ajoutez `id="bonnes-adresses"` dans la balise ouvrante du `<h2>` « Bonnes adresses », enregistrez, rechargez et recliquez : la page saute jusqu'au titre, et l'adresse se termine par `#bonnes-adresses`. Si la page est trop courte pour défiler, réduisez la hauteur de la fenêtre.

Le lien e-mail propose d'ouvrir votre messagerie. Si aucune n'est configurée sur votre poste, il ne se passe rien de visible : ce n'est pas une erreur de votre part.

```verify
F=~/byte-layers/web/basics/ville.html
if [ ! -f "$F" ]; then
  echo "Le fichier $F n'existe pas. Créez ville.html dans le dossier BASICS, puis enregistrez."
  exit 1
fi
T=$(grep -v '<!--' "$F" | tr '\n\r' '  ')
for tag in h1 strong em ul ol; do
  if ! echo "$T" | grep -q "<$tag[ >]"; then
    echo "Il manque un élément <$tag> dans ville.html."
    exit 1
  fi
done
if [ "$(echo "$T" | grep -o '<h2[ >]' | wc -l)" -lt 2 ]; then
  echo "Il faut deux titres <h2> : « À voir » et « Bonnes adresses »."
  exit 1
fi
if [ "$(echo "$T" | grep -o '<li[ >]' | wc -l)" -lt 6 ]; then
  echo "Les deux listes doivent avoir trois éléments <li> chacune."
  exit 1
fi
if ! echo "$T" | grep -q 'href="#bonnes-adresses"'; then
  echo "Il manque le lien interne : <a href=\"#bonnes-adresses\">."
  exit 1
fi
if ! echo "$T" | grep -q '<h2[^>]*id="bonnes-adresses"'; then
  echo "Le lien interne ne mène nulle part : ajoutez id=\"bonnes-adresses\" dans la balise <h2> « Bonnes adresses »."
  exit 1
fi
if ! echo "$T" | grep -q 'href="mailto:'; then
  echo "Il manque le lien e-mail : href=\"mailto:…\"."
  exit 1
fi
EXT=$(echo "$T" | grep -o '<a [^>]*href="https\{0,1\}://[^>]*>' | grep 'target="_blank"')
if [ -z "$EXT" ]; then
  echo "Il manque un lien externe (href=\"https://…\") qui s'ouvre dans un nouvel onglet : target=\"_blank\"."
  exit 1
fi
if ! echo "$EXT" | grep -q 'rel="[^"]*noopener'; then
  echo "Le lien qui s'ouvre dans un nouvel onglet doit porter aussi rel=\"noopener\", dans la même balise."
  exit 1
fi
echo "La fiche a ses titres, ses deux listes et ses trois liens, et le lien interne trouve son titre."
```

## 04.3 - Une image dans un sous-dossier

On range les images dans un dossier à part : créez le dossier `images` dans `BASICS` (survolez `BASICS`, icône **New Folder… (Nouveau dossier…)**), puis, dans ce dossier, un fichier `ville.svg`. Collez-y ce dessin, un fichier image écrit en texte au format SVG :

```xml
<svg xmlns="http://www.w3.org/2000/svg" width="320" height="160" viewBox="0 0 320 160">
  <rect width="320" height="160" fill="rgb(224, 242, 254)"/>
  <rect x="30" y="70" width="60" height="90" fill="rgb(236, 72, 153)"/>
  <rect x="110" y="40" width="50" height="120" fill="rgb(37, 99, 235)"/>
  <rect x="180" y="90" width="110" height="70" fill="rgb(250, 204, 21)"/>
  <circle cx="270" cy="35" r="18" fill="rgb(250, 204, 21)"/>
</svg>
```

Enregistrez. Dans `ville.html`, sous le paragraphe de présentation, ajoutez une image `<img>` qui affiche ce fichier, avec un texte alternatif qui décrit ce qu'elle montre. Le chemin part du dossier de la page : `ville.html` est dans `basics`, l'image dans `basics/images`.

Enregistrez, rechargez : un petit dessin de ville s'affiche. Faites ensuite deux essais, en remettant le bon chemin après chacun :

1. Écrivez `photo.svg` à la place de `ville.svg` : l'image disparaît, et votre texte alternatif s'affiche à sa place. C'est ce que voit un visiteur dont la connexion a échoué.
2. Écrivez `Images/ville.svg`, avec une majuscule. Sous macOS et Windows, l'image s'affiche quand même : le disque ignore la casse par défaut. Sous Linux, elle disparaît. La vérification ci-dessous se comporte comme un serveur Linux : avec ce chemin, elle échoue.

```verify
D=~/byte-layers/web/basics
if [ ! -f "$D/images/ville.svg" ]; then
  echo "Le fichier $D/images/ville.svg n'existe pas. Créez le dossier images, puis ville.svg dedans, en minuscules."
  exit 1
fi
T=$(grep -v '<!--' "$D/ville.html" 2>/dev/null | tr '\n\r' '  ')
IMG=$(echo "$T" | grep -o '<img [^>]*>' | grep 'ville.svg')
if [ -z "$IMG" ]; then
  echo "ville.html n'affiche pas encore l'image : ajoutez <img src=\"…\" alt=\"…\">, puis enregistrez."
  exit 1
fi
if ! echo "$IMG" | grep -qE 'src="(\./)?images/ville\.svg"'; then
  echo "Le chemin de l'image ne correspond pas exactement au fichier : un serveur Linux ne la trouverait pas. Le chemin part du dossier de la page, et la casse compte."
  exit 1
fi
if ! echo "$IMG" | grep -qE 'alt="[^"]{3,}"'; then
  echo "L'image doit avoir un texte alternatif qui décrit ce qu'elle montre : alt=\"…\"."
  exit 1
fi
echo "L'image s'affiche avec un chemin exact et un texte alternatif."
```

````solution
```html
<img src="images/ville.svg" alt="Un dessin de ville : trois immeubles colorés sous un soleil jaune">
```

Le chemin `images/ville.svg` part du dossier de `ville.html` : on descend dans le dossier `images`, puis on nomme le fichier, en minuscules comme sur le disque.
````

> 📖 [Créer des liens (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Structuring_content/Creating_links) · [Les images en HTML (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Structuring_content/HTML_images) · [Les listes (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Structuring_content/Lists)
