---
title: "05 - Ranger une page en balises sémantiques, et voir son plan"
description: "Remplacer les div d'une page de blog par header, nav, main, article, aside et footer, en gardant un seul div, puis comparer l'arbre d'accessibilité avant et après dans les outils de développement"
---

Le bit [Le HTML sémantique](https://byte-layers.com/fr/bits/semantic-html) annonçait que les balises sémantiques ne changent rien à l'écran, et changent ce qu'entend un lecteur d'écran. Dans un aperçu en ligne, on ne pouvait que le croire. Ici, les outils de développement vous montrent le plan que le navigateur construit, avant et après.

![Live coding : remplacer les div par des balises sémantiques, et voir l'arbre d'accessibilité changer](https://media.byte-layers.com/v/a9a067ddfeb086d405a1a38266ef82297b8ac9b63d1c6d1c0883e95d5521937a.mp4)

## 05.1 - Créer la page faite de div

Cette section est un support : elle vous donne la page à transformer. Créez `club.html` dans `BASICS` et collez-y le blog d'un club de randonnée, construit entièrement en `<div>` :

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Les Marcheurs du Dimanche</title>
</head>
<body>
  <div>
    <h1>Les Marcheurs du Dimanche</h1>
    <p>Le blog d'un club de randonnée</p>
    <div>
      <ul>
        <li><a href="#">Accueil</a></li>
        <li><a href="#">Nos sorties</a></li>
        <li><a href="#">Nous rejoindre</a></li>
      </ul>
    </div>
  </div>

  <div>
    <h2>Nos derniers récits</h2>
    <div>
      <div>
        <h3>Le pic du Midi par la face nord</h3>
        <p>Départ à 6 h du parking. La montée est raide, mais le panorama récompense l'effort.</p>
      </div>
      <div>
        <h3>Boucle des trois lacs</h3>
        <p>Une sortie familiale de 12 km, accessible aux enfants à partir de huit ans.</p>
      </div>
    </div>

    <div>
      <h3>Le saviez-vous ?</h3>
      <p>Le club organise une sortie chaque dimanche depuis 1987.</p>
    </div>
  </div>

  <div>
    <p>© 2026 Les Marcheurs du Dimanche</p>
  </div>
</body>
</html>
```

Enregistrez et ouvrez la page dans le navigateur. Avant de la modifier, regardez le plan qu'en tire le navigateur :

| Navigateur | Où voir l'arbre d'accessibilité |
|---|---|
| Chrome, Edge | clic droit sur la page, **Inspecter** ; onglet **Éléments**, puis, dans le volet de droite, l'onglet **Accessibilité** (*Accessibility*), parfois caché derrière `»` ; cochez **Activer l'arborescence d'accessibilité complète** (*Enable full-page accessibility tree*) si elle est proposée, puis rouvrez les outils |
| Firefox | clic droit sur la page, **Inspecter l'accessibilité** : l'onglet **Accessibilité** s'ouvre |

L'arbre liste des titres (*heading*), des listes, des liens et des paragraphes, mais aucune zone : les huit `<div>` n'y produisent rien.

## 05.2 - Remplacer les div

Remplacez chaque `<div>`, et sa balise fermante `</div>`, par la balise qui dit ce qu'est la zone. Une seule doit rester un `<div>` : celle qui groupe les deux récits, pour la mise en page.

| Zone | Balise |
|---|---|
| le bloc du nom du club, avec le menu | `<header>` |
| le bloc de la liste de liens | `<nav>` |
| le bloc qui contient « Nos derniers récits », les récits et l'encadré | `<main>` |
| chacun des deux récits | `<article>` |
| l'encadré « Le saviez-vous ? » | `<aside>` |
| le bloc du copyright | `<footer>` |

Le plus sûr est de procéder zone par zone : remplacez la balise ouvrante, descendez jusqu'à sa balise fermante, que l'indentation vous aide à trouver, remplacez-la aussi, enregistrez, rechargez. L'apparence ne doit pas bouger d'un pixel ; si quelque chose se déplace, une balise ouvrante et sa fermante ne se correspondent plus.

Rouvrez ensuite l'arbre d'accessibilité : de nouvelles zones y apparaissent, *banner*, *navigation*, *main*, deux *article*, *complementary* et *contentinfo*. C'est le plan qu'un lecteur d'écran propose pour sauter directement au menu ou au contenu principal.

```verify
F=~/byte-layers/web/basics/club.html
if [ ! -f "$F" ]; then
  echo "Le fichier $F n'existe pas : refaites la section 05.1."
  exit 1
fi
T=$(grep -v '<!--' "$F" | tr '\n\r' '  ')
n() { echo "$T" | grep -o "$1" | wc -l | tr -d ' '; }
for pair in "header:1" "nav:1" "main:1" "article:2" "aside:1" "footer:1"; do
  tag=${pair%%:*}; want=${pair##*:}
  if [ "$(n "<$tag[ >]")" != "$want" ] || [ "$(n "</$tag>")" != "$want" ]; then
    echo "Il faut $want élément(s) <$tag>, avec autant de balises fermantes </$tag> : il y en a $(n "<$tag[ >]") ouvrant(s) et $(n "</$tag>") fermant(s)."
    exit 1
  fi
done
if [ "$(n '<div[ >]')" != 1 ] || [ "$(n '</div>')" != 1 ]; then
  echo "Il doit rester exactement un <div> et un </div>, ceux qui groupent les deux récits."
  exit 1
fi
if ! echo "$T" | grep -q '<header[^>]*>.*<nav[^>]*>.*</nav>.*</header>'; then
  echo "Le <nav> doit être à l'intérieur du <header>, comme le bloc du menu était dans le bloc du nom du club."
  exit 1
fi
echo "La page nomme ses zones : header, nav, main, deux article, aside, footer, et un seul div."
```

```hint
Si le compte d'une balise est faux, cherchez-la avec Cmd+F ou Ctrl+F dans VS Code : le nombre de résultats s'affiche dans la barre de recherche. Une balise fermante oubliée reste souvent un `</div>`.
```

> 📖 [Structurer un document HTML (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Structuring_content/Structuring_documents) · [L'arbre d'accessibilité dans Chrome (en anglais)](https://developer.chrome.com/docs/devtools/accessibility/reference) · [L'inspecteur d'accessibilité de Firefox (en anglais)](https://firefox-source-docs.mozilla.org/devtools-user/accessibility_inspector/)
