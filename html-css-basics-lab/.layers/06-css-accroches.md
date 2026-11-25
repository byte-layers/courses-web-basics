---
title: "06 - Habiller une page en CSS, puis poser ses propres accroches"
description: "Écrire une feuille de style externe pour la page d'une médiathèque (police et repli, couleurs, classe, id, liens), lire les règles dans l'inspecteur, puis ajouter soi-même une classe dans le HTML et la règle qui la vise"
---

Le bit [CSS : règles, sélecteurs et cascade](https://byte-layers.com/fr/bits/css-rules-cascade) a fait écrire des règles dans une page dont le HTML était figé. Ici, vous habillez d'abord une page fournie, puis vous faites ce que fait tout développeur quand le HTML n'offre pas la prise dont il a besoin : vous la créez.

![Live coding : habiller la médiathèque en CSS, lire les règles dans l'inspecteur, puis créer la classe banniere](https://media.byte-layers.com/v/4108f6e6727ea227e868531db3b181070b9218a402314d57b8f64a50500aea4d.mp4)

## 06.1 - Créer la page et sa feuille de style

Cette section est un support. Créez `mediatheque.html` dans `BASICS` et collez-y la page d'une médiathèque :

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Médiathèque des Trois Rivières</title>
  <link rel="stylesheet" href="mediatheque.css">
</head>
<body>
  <header>
    <h1>Médiathèque des Trois Rivières</h1>
    <p>Lire, écouter, emprunter, depuis 1994</p>
  </header>
  <nav>
    <ul>
      <li><a href="#presentation">Bienvenue</a></li>
      <li><a href="#nouveautes">Nouveautés</a></li>
    </ul>
  </nav>
  <main>
    <section id="presentation">
      <h2>Bienvenue</h2>
      <p class="intro">Plus de 40 000 ouvrages et une salle de lecture ouverte à tous.</p>
      <p>L'inscription est gratuite pour les moins de dix-huit ans.</p>
    </section>
    <section id="nouveautes">
      <h2>Nos nouveautés</h2>
      <p class="intro">Une sélection renouvelée chaque mois par l'équipe.</p>
      <ul>
        <li>Le Mur invisible, de Marlen Haushofer</li>
        <li>La Horde du Contrevent, d'Alain Damasio</li>
      </ul>
    </section>
  </main>
  <footer>
    <p>12 rue des Peupliers, Toulouse</p>
  </footer>
</body>
</html>
```

Créez ensuite, à côté, un fichier vide `mediatheque.css` : c'est le nom que cite la balise `<link>`. Ouvrez `mediatheque.html` dans le navigateur : il s'affiche avec l'apparence par défaut, en police à empattements.

## 06.2 - Écrire les règles

Écrivez dans `mediatheque.css` une règle par ligne du tableau. Après chacune, enregistrez et rechargez la page.

| Sélecteur | Ce que la règle doit faire |
|---|---|
| `body` | une police sans empattements avec au moins un repli, finie par `sans-serif` ; un interligne de `1.6` ; un texte `#333` sur un fond `#f7f7f5` |
| `h1` | la couleur `#14457b` |
| `h2` | la couleur `#0b6bcb`, texte centré |
| la classe `intro` | le texte en gras |
| l'id `presentation` | un fond blanc |
| `a` | sans soulignement (`text-decoration: none`), couleur `#0b6bcb` |
| `footer` | texte centré, taille `14px` |

Les deux paragraphes `intro` passent en gras, mais seule la section « Bienvenue » prend un fond blanc : une classe vise tous les éléments qui la portent, un id un seul.

Puis ouvrez l'inspecteur : clic droit sur un paragraphe en gras, **Inspecter**. Le panneau **Styles** liste toutes les règles qui s'appliquent à cet élément, avec le nom du fichier et le numéro de ligne : votre `.intro`, et plus bas votre `body`, sous « Hérité de » (*Inherited from*), pour la police. Ajoutez maintenant une faute exprès dans une règle, `colr` au lieu de `color` dans `h1`, enregistrez, rechargez, inspectez le titre : la déclaration est barrée, avec un triangle d'avertissement. Corrigez la faute avant de continuer.

```verify
C=~/byte-layers/web/basics/mediatheque.css
if [ ! -f "$C" ]; then
  echo "Le fichier $C n'existe pas. Créez mediatheque.css à côté de mediatheque.html, puis enregistrez."
  exit 1
fi
rule() { perl -0pe 's{/\*.*?\*/}{}gs; s/[\r\n]/ /g' "$C" | grep -oE '[^{}]+\{[^}]*\}' | grep -E "(^|[ ,])$1[ ,]*\{"; }
if ! rule body | grep -qE 'font-family:[^;}]*,[^;}]*sans-serif'; then
  echo "La règle body doit donner une police avec au moins un repli, finie par sans-serif : font-family: system-ui, \"Segoe UI\", sans-serif;"
  exit 1
fi
if ! rule body | grep -q 'line-height'; then
  echo "La règle body doit donner un interligne : line-height: 1.6;"
  exit 1
fi
if ! rule h2 | grep -qE 'text-align:[[:space:]]*center'; then
  echo "La règle h2 doit centrer le texte : text-align: center;"
  exit 1
fi
if ! rule '\.intro' | grep -qE 'font-weight:[[:space:]]*(bold|[6-9]00)'; then
  echo "La règle de la classe intro, écrite avec un point (.intro), doit mettre le texte en gras : font-weight: bold;"
  exit 1
fi
if ! rule '#presentation' | grep -qE 'background(-color)?:'; then
  echo "La règle de l'id presentation, écrite avec un dièse (#presentation), doit donner un fond blanc."
  exit 1
fi
if ! rule a | grep -qE 'text-decoration:[[:space:]]*none'; then
  echo "La règle a doit retirer le soulignement : text-decoration: none;"
  exit 1
fi
if grep -qE '(^|[^-])colr|colour' "$C"; then
  echo "Une faute de frappe reste dans la feuille : la propriété s'écrit color."
  exit 1
fi
echo "La feuille de style habille la page : police et repli, titres, classe, id et liens."
```

```hint
Une règle qui ne fait rien a presque toujours l'une de ces trois causes : le fichier CSS n'est pas enregistré, le sélecteur ne vise rien (un point oublié devant `intro`, un dièse devant `presentation`), ou un point-virgule manque entre deux déclarations.
```

## 06.3 - Poser sa propre accroche : une classe dans le HTML

On veut un bandeau bleu foncé pour l'en-tête de cette page, et de celles qu'on ajoutera au site. Il n'existe aucune classe sur le `<header>` pour le viser, et `header` comme sélecteur viserait aussi les en-têtes d'articles le jour où il y en aura. Créez donc l'accroche :

1. dans `mediatheque.html`, ajoutez `class="banniere"` dans la balise ouvrante du `<header>` ;
2. dans `mediatheque.css`, écrivez la règle `.banniere` : un fond `#14457b`, un texte blanc, `30px` d'espace intérieur (`padding: 30px`), texte centré ;
3. enregistrez **les deux fichiers**, puis rechargez.

Le titre, lui, reste bleu foncé, donc invisible sur le fond bleu foncé : la règle `h1` l'emporte sur la couleur héritée de `.banniere`, parce qu'une règle qui vise l'élément passe devant l'héritage. Ajoutez `color: white;` dans une règle `.banniere h1`, qui vise les `h1` à l'intérieur de la bannière.

Dernier essai, celui de la panne la plus fréquente : dans le HTML, écrivez `class="baniere"`, avec un seul `n`, enregistrez, rechargez. Le bandeau disparaît, sans aucun message, ni dans le HTML ni dans le CSS : les deux fichiers sont valides, ils ne se parlent simplement plus. Inspectez l'en-tête : la règle `.banniere` n'apparaît plus dans le panneau Styles. Remettez le bon nom.

```verify
D=~/byte-layers/web/basics
T=$(grep -v '<!--' "$D/mediatheque.html" 2>/dev/null | tr '\n\r' '  ')
if ! echo "$T" | grep -qE '<header[^>]*class="([^"]* )?banniere( [^"]*)?"'; then
  echo "La balise <header> de mediatheque.html doit porter class=\"banniere\", orthographié exactement ainsi. Le fichier est-il enregistré ?"
  exit 1
fi
C=$D/mediatheque.css
rule() { perl -0pe 's{/\*.*?\*/}{}gs; s/[\r\n]/ /g' "$C" | grep -oE '[^{}]+\{[^}]*\}' | grep -E "(^|[ ,])$1[ ,]*\{"; }
if ! rule '\.banniere' | grep -qE 'background(-color)?:'; then
  echo "La règle .banniere de mediatheque.css doit donner un fond bleu foncé : background-color: #14457b;"
  exit 1
fi
if ! rule '\.banniere' | grep -q 'padding'; then
  echo "La règle .banniere doit donner un espace intérieur : padding: 30px;"
  exit 1
fi
echo "L'accroche existe des deux côtés : class=\"banniere\" dans le HTML, .banniere dans le CSS."
```

````solution
```css
.banniere {
  background-color: #14457b;
  color: white;
  padding: 30px;
  text-align: center;
}

.banniere h1 {
  color: white;
}
```

Dans le HTML, la balise devient `<header class="banniere">`. On nomme la classe par son rôle, `banniere`, et non par son apparence, `bandeau-bleu` : le jour où la couleur change, le nom reste juste.
````

> 📖 [Les sélecteurs CSS (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Core/Styling_basics/Basic_selectors) · [Examiner et modifier le CSS dans Chrome (en anglais)](https://developer.chrome.com/docs/devtools/css) · [Le validateur CSS du W3C](https://jigsaw.w3.org/css-validator/)
