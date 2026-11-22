---
title: "01 - L'entête d'un site dans le flux normal"
description: "Créer le dossier du lab, écrire l'entête (logo, titre, menu), voir les blocs s'empiler dans l'inspecteur, mettre le menu sur une ligne et donner une vraie boîte au bouton"
---

Vous commencez la page par son entête : un logo, un menu, puis le titre et un bouton de contact. Sans aucune règle de disposition, le navigateur les range dans le **flux normal** ; vous allez le voir, puis le corriger là où il coince.

## 01.1 - Créer le dossier du lab et l'ouvrir dans VS Code

Cette sous-étape est un **support** : elle prépare le dossier, vous pouvez la jouer telle quelle. La commande `mkdir -p` crée le dossier, et avec `-p` les dossiers parents qui manquent (`byte-layers`, puis `web`) :

```exec "Créer le dossier du lab"
mkdir -p ~/byte-layers/web/advanced
```

Ouvrez ce dossier dans VS Code : menu **File > Open Folder…** (Fichier > Ouvrir le dossier…), puis choisissez `advanced` dans votre dossier personnel, sous `byte-layers/web`. Si la commande `code` est installée, celle-ci fait la même chose :

```exec "Ouvrir le dossier dans VS Code"
code ~/byte-layers/web/advanced
```

## 01.2 - Écrire l'entête : logo, menu, titre

Dans l'explorateur de VS Code, créez un fichier `index.html` (icône **New File…** à droite du nom du dossier), puis collez-y ce squelette. Il est complet, sauf l'entête : les deux commentaires `TODO` disent ce qu'il doit contenir.

🚧 **À compléter :**

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Camille Martin, développeuse web</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header class="entete">
    <!-- TODO : un paragraphe de classe "logo" qui contient CM -->
    <!-- TODO : un nav, et dedans une liste ul de classe "menu" avec trois liens :
         Projets vers #projets, Galerie vers #galerie, Contact vers #contact -->
  </header>
  <main>
    <h1>Camille Martin, développeuse web</h1>
    <p>Je cherche une alternance à partir de septembre.</p>
    <a class="bouton" href="#contact">Me contacter</a>
  </main>
</body>
</html>
```

Créez ensuite `style.css`, à côté, avec cette seule règle, puis enregistrez les deux fichiers :

```css
body {
  font-family: system-ui, sans-serif;
  margin: 0;
}
```

Ouvrez `index.html` dans le navigateur : double-clic sur le fichier dans votre gestionnaire de fichiers, ou clic droit dans l'explorateur de VS Code, **Show Preview** avec Live Preview. Le logo, le menu, le titre et le paragraphe s'empilent, chacun sur sa ligne ; les liens du menu ont une puce chacun.

> 📖 [Le flux normal (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/CSS_layout/Introduction#le_flux_normal)

```verify
F=~/byte-layers/web/advanced/index.html
[ -f "$F" ] || { echo "Il n'y a pas de index.html dans ~/byte-layers/web/advanced. Créez-le depuis l'explorateur de VS Code, puis enregistrez."; exit 1; }
H=$(tr -d '\n' < "$F")
echo "$H" | grep -Eq '<p[^>]*class="logo"[^>]*>[[:space:]]*CM' || { echo "L'entête n'a pas encore de paragraphe de classe logo qui contient CM."; exit 1; }
echo "$H" | grep -Eq '<nav[^>]*>.*<ul[^>]*class="menu"' || { echo "Il manque un nav qui contient une liste ul de classe menu."; exit 1; }
for a in '#projets' '#galerie' '#contact'; do
  echo "$H" | grep -q "href=\"$a\"" || { echo "Le menu n'a pas de lien vers $a."; exit 1; }
done
[ -f ~/byte-layers/web/advanced/style.css ] || { echo "Il n'y a pas encore de style.css à côté de index.html."; exit 1; }
echo "L'entête a son logo et son menu de trois liens."
```

```hint
Un lien de menu s'écrit `<li><a href="#projets">Projets</a></li>` ; les trois `li` vont dans `<ul class="menu">`, lui-même dans `<nav>`.
```

## 01.3 - Voir les blocs avec l'inspecteur

Avant de toucher au CSS, regardez comment le navigateur a rangé les boîtes. Clic droit sur le logo, **Inspecter** : le panneau des outils de développement s'ouvre sur la balise `<p class="logo">`.

> **🧪 Manip — la largeur d'un bloc**
>
> 1. Dans le panneau HTML, survolez `<p class="logo">` : le navigateur surligne sa boîte dans la page.
> 2. Survolez ensuite `<a class="bouton">`.
>
> *Observé : le paragraphe du logo, qui ne contient que deux lettres, est surligné sur toute la largeur de la page ; c'est un **bloc**. Le lien n'est surligné que sur la largeur de son texte ; c'est un **inline**.*

## 01.4 - Le menu sur une ligne, le bouton avec une vraie boîte

Deux choses coincent : les liens du menu sont empilés, et le bouton n'a pas encore de forme. Vous les réglez dans `style.css`, avec les deux valeurs de `display` du bit sur le flux normal.

| Propriété | Sur quoi | Rôle |
|---|---|---|
| `display: inline-block` | `.menu li` | met chaque élément de liste dans la ligne |
| `list-style: none` | `.menu` | retire les puces |
| `padding: 0` | `.menu` | retire le retrait à gauche de la liste |
| `display: inline-block` | `.bouton` | le lien reste dans la ligne, mais sa marge du haut et son padding comptent |

> **🧪 Manip — la marge ignorée**
>
> 1. Ajoutez d'abord cette règle, sans `display`, enregistrez et rechargez :
>    `.bouton { background-color: rgb(219, 39, 119); color: white; padding: 8px 16px; margin-top: 24px; text-decoration: none; }`
> 2. Regardez l'espace entre le paragraphe et le bouton.
>
> *Observé : la marge du haut ne fait rien, et le fond rose déborde sur le paragraphe. Le lien est inline : sa marge verticale ne repousse rien.*

🚧 **À compléter :** ajoutez à la règle `.bouton` la ligne qui manque, puis écrivez les deux règles du menu.

```css
.bouton {
  /* TODO : la valeur de display qui donne une vraie boîte au bouton */
  background-color: rgb(219, 39, 119);
  color: white;
  padding: 8px 16px;
  margin-top: 24px;
  text-decoration: none;
}

/* TODO : .menu, sans puces ni retrait */
/* TODO : .menu li, dans la ligne, avec margin-right: 16px */
```

Enregistrez et rechargez : les trois liens sont sur une ligne, et le bouton s'écarte du paragraphe. Le logo reste au-dessus du menu : `.logo` et `nav` sont deux blocs. L'étape suivante règle ce point.

```verify
C=$(tr -d '\n' < ~/byte-layers/web/advanced/style.css 2>/dev/null)
echo "$C" | grep -Eq '\.menu li[[:space:]]*\{[^}]*display:[[:space:]]*inline|\.menu[[:space:]]*\{[^}]*display:[[:space:]]*flex' || { echo "Les éléments du menu ne sont pas encore dans la ligne : écrivez display: inline-block dans une règle .menu li."; exit 1; }
echo "$C" | grep -Eq '\.menu[[:space:]]*\{[^}]*list-style(-type)?:[[:space:]]*none' || { echo "Le menu a encore ses puces : list-style: none dans la règle .menu."; exit 1; }
echo "$C" | grep -Eq '\.bouton[[:space:]]*\{[^}]*display:[[:space:]]*(inline-block|block)' || { echo "Le bouton est encore inline : ajoutez display: inline-block à la règle .bouton."; exit 1; }
echo "Le menu est sur une ligne et le bouton a une vraie boîte."
```

```hint
Si la vérification échoue alors que la page s'affiche bien, regardez le nom de la règle : `.menu li` avec un espace (les `li` à l'intérieur de `.menu`), et un point devant `menu` et `bouton`.
```

````solution
```css
body {
  font-family: system-ui, sans-serif;
  margin: 0;
}

.bouton {
  display: inline-block;
  background-color: rgb(219, 39, 119);
  color: white;
  padding: 8px 16px;
  margin-top: 24px;
  text-decoration: none;
}

.menu {
  list-style: none;
  padding: 0;
}

.menu li {
  display: inline-block;
  margin-right: 16px;
}
```
````

> 📖 [La propriété display (MDN)](https://developer.mozilla.org/fr/docs/Web/CSS/display) · [Les outils de développement, inspecter le HTML et le CSS (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Howto/Tools_and_setup/What_are_browser_developer_tools)
