---
title: "Mon portfolio, version 1"
description: "Une page à vous, sans guide : votre portfolio statique en HTML et CSS, avec un squelette valide, des zones sémantiques, un plan de titres, une liste, une image décrite, des liens, une feuille de style externe, vos propres classes, deux couleurs, une police et des espacements maîtrisés. Onze points vérifiés dans vos fichiers."
tags:
  - challenge
  - web
  - html
  - css
difficulty: beginner
duration: 90
introTitle: "Le défi"
requires: "0.4.0"
options:
  allowManualProgress: false
  autoCompleteOnNext: unverifiable
---

Ce challenge prouve que vous savez construire une page web complète, seul, à partir d'une page vide : la vôtre. Le sujet est un **portfolio**, une page qui vous présente : votre parcours, ce que vous savez faire, ce que vous avez réalisé, ou une passion si vous n'avez encore rien à montrer. Vous décidez du contenu, des couleurs, de la disposition. Il n'y a ni fichier à compléter ni corrigé : il n'existe pas une bonne réponse.

Ce portfolio vous suit dans les cours suivants : le cours sur le HTML et le CSS avancés le rendra adaptatif et accessible et lui ajoutera un formulaire, le cours de JavaScript le fera réagir. Cette première version est **statique** : du HTML et du CSS.

Chaque tâche donne des critères, et un bouton vérifie vos fichiers pour chacun. Si vous êtes bloqué, les **indices** se dévoilent un par un et renvoient au contenu qui enseigne le point. Les utiliser ne coûte rien : seule la vérification compte.

## Avant de commencer

- **Ce qu'il faut savoir** : ce qu'enseignent les bits du cours, du [squelette d'une page](https://byte-layers.com/fr/bits/html-document) au [modèle de boîte](https://byte-layers.com/fr/bits/box-model), et le lab [Les bases HTML et CSS, sur votre machine](https://byte-layers.com/fr/labs/html-css-basics-lab).
- **Ce qu'il faut avoir** : VS Code, un navigateur, et un terminal pour créer le dossier (Git Bash sous Windows).
- **Vos fichiers** : tout vit dans `~/byte-layers/web/portfolio`, avec `index.html`, `style.css` et un dossier `images/`. La première tâche crée le dossier. Il reste sur votre poste à la fin : c'est votre portfolio, que les cours suivants reprennent.

- **Un conseil de méthode** : écrivez d'abord tout le contenu en HTML, sans aucun style. Vous verrez mieux la structure, et le CSS ira ensuite plus vite. Le fond, puis la forme.
- **Des images** : prenez les vôtres, ou des images libres de droits, sur Unsplash, Pexels ou unDraw ; la plupart des images trouvées sur le web sont protégées par le droit d'auteur. Réduisez une photo à moins de 1 500 pixels de large avant de l'utiliser : une photo de 5 000 pixels ralentit la page pour rien.

Les vérifications lisent vos fichiers sur le disque. Elles contrôlent ce qui se contrôle dans un fichier : la présence d'une balise, d'un attribut, d'une règle. Elles ne jugent pas si votre texte alternatif décrit vraiment l'image, ni si vos couleurs vont bien ensemble : ça, c'est à vous de le regarder, dans le navigateur.

Le formulaire de contact ou le tableau de données de la checklist d'origine viendront avec la version 2, quand le cours suivant les aura enseignés.

# Tâche 1 : une page valide, découpée en zones

## Le squelette et les zones

Créez le dossier du portfolio, avec son sous-dossier `images` : `mkdir -p` crée les dossiers qui manquent sur le chemin.

```exec "Créer le dossier du portfolio"
mkdir -p ~/byte-layers/web/portfolio/images
```

Ouvrez le dossier `~/byte-layers/web/portfolio` dans VS Code, créez-y `index.html`, et posez la structure de la page.

**Critères :**

1. Un squelette valide : le doctype en première ligne, la langue sur `<html>`, l'encodage UTF-8, la ligne `meta viewport` et un `<title>` qui vous nomme.
2. Les zones de la page dans leurs balises sémantiques : un `<header>` avec un `<nav>`, un seul `<main>`, un `<footer>`, et dans le `<main>` au moins une `<section>` ou un `<article>`, selon ce que vous présentez.

```hint
Le squelette complet, ligne par ligne, est dans le bit [Le squelette d'une page HTML](https://byte-layers.com/fr/bits/html-document), section « Le squelette ».
```

```hint
Pour choisir entre `<section>` et `<article>`, faites le test de la publication du bit [Le HTML sémantique](https://byte-layers.com/fr/bits/semantic-html) : un projet présenté seul garde-t-il son sens ?
```

```verify
F=~/byte-layers/web/portfolio/index.html
[ -f "$F" ] || { echo "Le fichier $F n'existe pas. Créez index.html dans le dossier portfolio, puis enregistrez."; exit 1; }
head -n 1 "$F" | tr -d '\r' | grep -qi '^[[:space:]]*<!doctype html>[[:space:]]*$' || { echo "Critère 1 : la première ligne doit être le doctype, <!DOCTYPE html>, et rien d'autre."; exit 1; }
T=$(perl -0pe 's/<!--.*?-->//gs; s/[\r\n]/ /g' "$F")
echo "$T" | grep -qiE '<html[^>]*lang="[a-z]{2}' || { echo "Critère 1 : la balise <html> doit déclarer la langue, par exemple lang=\"fr\"."; exit 1; }
echo "$T" | grep -qiE '<meta[^>]*charset="?utf-8' || { echo "Critère 1 : il manque l'encodage, <meta charset=\"utf-8\">."; exit 1; }
echo "$T" | grep -qiE '<meta[^>]*name="viewport"[^>]*width=device-width|<meta[^>]*width=device-width[^>]*name="viewport"' || { echo "Critère 1 : il manque la ligne <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">."; exit 1; }
echo "$T" | grep -qiE '<title>[[:space:]]*[^<[:space:]][^<]*</title>' || { echo "Critère 1 : il manque un <title> avec un texte."; exit 1; }
echo "Critère 1 : le squelette est valide."
```

```verify
F=~/byte-layers/web/portfolio/index.html
[ -f "$F" ] || { echo "Le fichier $F n'existe pas."; exit 1; }
T=$(perl -0pe 's/<!--.*?-->//gs; s/[\r\n]/ /g' "$F")
n() { echo "$T" | grep -oiE "$1" | wc -l | tr -d ' '; }
[ "$(n '<header[ >]')" -ge 1 ] || { echo "Critère 2 : il manque un <header>, l'en-tête de la page."; exit 1; }
echo "$T" | grep -qiE '<header[^>]*>.*<nav[ >].*</nav>.*</header>' || { echo "Critère 2 : le menu doit être un <nav>, à l'intérieur du <header>."; exit 1; }
[ "$(n '<main[ >]')" = 1 ] || { echo "Critère 2 : il faut exactement un <main> ; il y en a $(n '<main[ >]')."; exit 1; }
[ "$(n '<footer[ >]')" -ge 1 ] || { echo "Critère 2 : il manque un <footer>, le pied de page."; exit 1; }
echo "$T" | grep -qiE '<main[^>]*>.*<(section|article)[ >].*</main>' || { echo "Critère 2 : le <main> doit contenir au moins une <section> ou un <article>."; exit 1; }
echo "Critère 2 : la page est découpée en zones sémantiques."
```

# Tâche 2 : le contenu

## Titres, liste, image et liens

Remplissez la page : qui vous êtes, ce que vous faites, ce que vous avez réalisé.

**Critères :**

3. Une hiérarchie de titres cohérente : un seul `<h1>`, au moins deux `<h2>`, et aucun niveau sauté (pas de `<h3>` sans `<h2>` avant lui, pas de `<h4>` sans `<h3>`).
4. Au moins une liste, à puces ou numérotée.
5. Au moins une image, rangée dans `images/`, avec un texte alternatif qui la décrit vraiment ; chaque image a son attribut `alt`, et chaque chemin correspond exactement au fichier, majuscules comprises.
6. Au moins trois liens, dont un vers un autre site, qui s'ouvre dans un nouvel onglet avec `rel="noopener"`.

```hint
Écrivez vos titres comme une table des matières : le `<h1>`, c'est vous ; les `<h2>`, les grandes parties de la page ; les `<h3>`, les éléments d'une partie, comme chaque projet.
```

```hint
Un chemin d'image part du dossier de `index.html` : `images/mon-image.jpg`. Nommez vos fichiers en minuscules, sans espace ni accent, et le piège de la casse disparaît.
```

```hint
Le menu du `<nav>` peut fournir deux liens internes, vers les `id` de vos sections : `href="#projets"` et `id="projets"`. Les liens sont dans le bit [Le squelette d'une page HTML](https://byte-layers.com/fr/bits/html-document).
```

```verify
F=~/byte-layers/web/portfolio/index.html
[ -f "$F" ] || { echo "Le fichier $F n'existe pas."; exit 1; }
T=$(perl -0pe 's/<!--.*?-->//gs; s/[\r\n]/ /g' "$F")
L=$(echo "$T" | grep -oiE '<h[1-6][ >]' | sed 's/[^1-6]//g')
[ "$(echo "$L" | grep -c '^1$')" = 1 ] || { echo "Critère 3 : il faut exactement un <h1> ; il y en a $(echo "$L" | grep -c '^1$')."; exit 1; }
[ "$(echo "$L" | grep -c '^2$')" -ge 2 ] || { echo "Critère 3 : il faut au moins deux <h2>, les grandes parties de la page."; exit 1; }
prev=0
for l in $L; do
  [ "$prev" -gt 0 ] || [ "$l" = 1 ] || { echo "Critère 3 : la page commence par un <h$l> ; le premier titre doit être le <h1>."; exit 1; }
  [ "$l" -le $((prev + 1)) ] || { echo "Critère 3 : un niveau est sauté, un <h$l> suit un <h$prev>. Les titres forment un plan, sans trou."; exit 1; }
  prev=$l
done
echo "Critère 3 : les titres forment un plan cohérent."
```

```verify
F=~/byte-layers/web/portfolio/index.html
[ -f "$F" ] || { echo "Le fichier $F n'existe pas."; exit 1; }
T=$(perl -0pe 's/<!--.*?-->//gs; s/[\r\n]/ /g' "$F")
echo "$T" | grep -qiE '<(ul|ol)[ >].*<li[ >]' || { echo "Critère 4 : il faut au moins une liste, <ul> ou <ol>, avec ses éléments <li>."; exit 1; }
echo "Critère 4 : la page a au moins une liste."
```

```verify
D=~/byte-layers/web/portfolio
F=$D/index.html
[ -f "$F" ] || { echo "Le fichier $F n'existe pas."; exit 1; }
T=$(perl -0pe 's/<!--.*?-->//gs; s/[\r\n]/ /g' "$F")
IMGS=$(echo "$T" | grep -oiE '<img [^>]*>')
[ -n "$IMGS" ] || { echo "Critère 5 : il faut au moins une image, <img src=\"images/…\" alt=\"…\">."; exit 1; }
[ "$(echo "$IMGS" | grep -vc 'alt="')" = 0 ] || { echo "Critère 5 : chaque image doit avoir un attribut alt."; exit 1; }
echo "$IMGS" | grep -qE 'alt="[^"]{5,}"' || { echo "Critère 5 : au moins une image doit avoir un texte alternatif qui la décrit, en quelques mots."; exit 1; }
echo "$IMGS" | grep -qE 'src="(\./)?images/' || { echo "Critère 5 : rangez au moins une image dans le dossier images/."; exit 1; }
for src in $(echo "$IMGS" | sed -n 's/.*src="\([^"]*\)".*/\1/p'); do
  case "$src" in http://*|https://*|data:*) continue ;; esac
  cur=$D
  for part in $(echo "${src#./}" | tr '/' ' '); do
    ls -1a "$cur" 2>/dev/null | grep -Fxq "$part" || { echo "Critère 5 : le chemin $src ne correspond à aucun fichier, majuscules comprises (« $part » introuvable dans $cur). Un serveur ne trouverait pas l'image."; exit 1; }
    cur=$cur/$part
  done
done
echo "Critère 5 : les images ont leur texte alternatif et des chemins exacts."
```

```verify
F=~/byte-layers/web/portfolio/index.html
[ -f "$F" ] || { echo "Le fichier $F n'existe pas."; exit 1; }
T=$(perl -0pe 's/<!--.*?-->//gs; s/[\r\n]/ /g' "$F")
A=$(echo "$T" | grep -oiE '<a [^>]*href="[^"]+"[^>]*>')
[ "$(echo "$A" | grep -c .)" -ge 3 ] || { echo "Critère 6 : il faut au moins trois liens <a href=\"…\">."; exit 1; }
EXT=$(echo "$A" | grep -E 'href="https?://' | grep 'target="_blank"')
[ -n "$EXT" ] || { echo "Critère 6 : il faut un lien vers un autre site (href=\"https://…\") qui s'ouvre dans un nouvel onglet, avec target=\"_blank\"."; exit 1; }
echo "$EXT" | grep -q 'rel="[^"]*noopener' || { echo "Critère 6 : le lien qui s'ouvre dans un nouvel onglet doit porter rel=\"noopener\", dans la même balise."; exit 1; }
echo "Critère 6 : la page a ses liens, dont un externe dans un nouvel onglet."
```

# Tâche 3 : la mise en forme

## Une feuille de style à vous

Habillez la page avec une feuille de style externe. Prenez le temps de choisir vos couleurs : une couleur **dominante**, celle qu'on retient de la page, et une couleur d'**accent**, pour ce qui doit attirer l'œil.

**Critères :**

7. Une feuille de style externe, `style.css` ou un autre nom, reliée par `<link>`, et le fichier existe sous ce nom exact.
8. Vos propres classes, au moins deux, posées dans le HTML et visées dans le CSS, nommées par leur **rôle** et non par leur apparence (`banniere`, `projet`, pas `bleu` ni `gros-titre`).
9. Une couleur dominante et une couleur d'accent : au moins deux couleurs différentes, écrites en hexadécimal (`#14457b`), en `rgb(…)` ou en `hsl(…)`. Les gris, les noirs et les blancs ne comptent pas.
10. Une police lisible avec sa liste de repli, finie par une famille générique, et un interligne (`line-height`).
11. Des espacements maîtrisés : du `padding` à l'intérieur et des `margin` à l'extérieur.

```hint
La balise `<link>`, la liste de repli d'une police et le nommage des classes sont dans le bit [CSS : règles, sélecteurs et cascade](https://byte-layers.com/fr/bits/css-rules-cascade).
```

```hint
Une couleur est grise quand ses trois composantes, rouge, vert et bleu, sont égales : `#333`, `rgb(200, 200, 200)`. Pour une dominante et un accent, prenez deux vraies teintes, un bleu et un rose par exemple.
```

```hint
Padding dedans, marge dehors : le test du fond est dans le bit [Le modèle de boîte](https://byte-layers.com/fr/bits/box-model). N'oubliez pas `* { box-sizing: border-box; }` en tête de la feuille.
```

```verify
D=~/byte-layers/web/portfolio
F=$D/index.html
[ -f "$F" ] || { echo "Le fichier $F n'existe pas."; exit 1; }
T=$(perl -0pe 's/<!--.*?-->//gs; s/[\r\n]/ /g' "$F")
LINK=$(echo "$T" | grep -oiE '<link [^>]*rel="stylesheet"[^>]*>' | head -1)
[ -n "$LINK" ] || { echo "Critère 7 : il manque la balise <link rel=\"stylesheet\" href=\"style.css\"> dans le <head>."; exit 1; }
CSS=$(echo "$LINK" | sed -n 's/.*href="\([^"]*\)".*/\1/p')
case "$CSS" in http://*|https://*|"") echo "Critère 7 : la balise <link> doit citer votre propre fichier CSS, dans le dossier portfolio."; exit 1 ;; esac
cur=$D
for part in $(echo "${CSS#./}" | tr '/' ' '); do
  ls -1a "$cur" 2>/dev/null | grep -Fxq "$part" || { echo "Critère 7 : la balise <link> cite $CSS, mais aucun fichier ne porte ce nom exact, majuscules comprises."; exit 1; }
  cur=$cur/$part
done
echo "Critère 7 : la feuille de style $CSS est reliée et existe."
```

```verify
D=~/byte-layers/web/portfolio
F=$D/index.html
[ -f "$F" ] || { echo "Le fichier $F n'existe pas."; exit 1; }
T=$(perl -0pe 's/<!--.*?-->//gs; s/[\r\n]/ /g' "$F")
CSS=$(echo "$T" | grep -oiE '<link [^>]*rel="stylesheet"[^>]*>' | head -1 | sed -n 's/.*href="\([^"]*\)".*/\1/p')
C=$D/${CSS#./}
[ -n "$CSS" ] && [ -f "$C" ] || { echo "Critère 8 : reliez d'abord une feuille de style (critère 7)."; exit 1; }
S=$(perl -0pe 's{/\*.*?\*/}{}gs; s/[\r\n]/ /g' "$C")
CLASSES=$(echo "$T" | grep -oE 'class="[^"]*"' | sed 's/class="//; s/"$//' | tr ' ' '\n' | grep -v '^$' | sort -u)
used=0
for c in $CLASSES; do
  for w in $(echo "$c" | tr '_-' '  '); do
    case "$w" in
      rouge|bleu|bleue|vert|verte|jaune|noir|noire|blanc|blanche|gris|grise|rose|orange|violet|violette|red|blue|green|yellow|black|white|gray|grey|pink|purple|gras|gros|grosse|petit|petite|grand|grande|big|small|bold|italique|souligne)
        echo "Critère 8 : la classe « $c » décrit une apparence. Nommez-la par son rôle (banniere, projet, contact…), puis renommez-la des deux côtés."; exit 1 ;;
    esac
  done
  echo "$S" | grep -qE "\.$c([^a-zA-Z0-9_-]|$)" && used=$((used + 1))
done
[ "$used" -ge 2 ] || { echo "Critère 8 : il faut au moins deux classes posées dans le HTML (class=\"…\") et visées dans le CSS (.nom { … }) ; il y en a $used."; exit 1; }
echo "Critère 8 : $used classes à vous, posées dans le HTML et visées dans le CSS."
```

```verify
D=~/byte-layers/web/portfolio
F=$D/index.html
[ -f "$F" ] || { echo "Le fichier $F n'existe pas."; exit 1; }
CSS=$(perl -0pe 's/<!--.*?-->//gs; s/[\r\n]/ /g' "$F" | grep -oiE '<link [^>]*rel="stylesheet"[^>]*>' | head -1 | sed -n 's/.*href="\([^"]*\)".*/\1/p')
C=$D/${CSS#./}
[ -n "$CSS" ] && [ -f "$C" ] || { echo "Critère 9 : reliez d'abord une feuille de style (critère 7)."; exit 1; }
V=$(perl -0pe 's{/\*.*?\*/}{}gs; s/[\r\n]/ /g' "$C" | grep -oE ':[^;{}]+')
found=""
for h in $(echo "$V" | grep -oE '#[0-9a-fA-F]{3,8}' | tr 'A-F' 'a-f'); do
  x=${h#\#}
  case ${#x} in
    3|4) r=${x:0:1}${x:0:1}; g=${x:1:1}${x:1:1}; b=${x:2:1}${x:2:1} ;;
    6|8) r=${x:0:2}; g=${x:2:2}; b=${x:4:2} ;;
    *) continue ;;
  esac
  [ "$r" = "$g" ] && [ "$g" = "$b" ] && continue
  found="$found $r$g$b"
done
for c in $(echo "$V" | grep -oE 'rgba?\([^)]*\)' | tr -d ' '); do
  set -- $(echo "$c" | sed 's/^rgba\{0,1\}(//; s/)$//' | tr ',/' '  ')
  [ $# -ge 3 ] || continue
  r=${1%.*}; g=${2%.*}; b=${3%.*}
  case "$r$g$b" in *[!0-9]*) continue ;; esac
  [ "$r" = "$g" ] && [ "$g" = "$b" ] && continue
  found="$found $(printf '%02x%02x%02x' "$r" "$g" "$b")"
done
for c in $(echo "$V" | grep -oE 'hsla?\([^)]*\)' | tr -d ' '); do
  set -- $(echo "$c" | sed 's/^hsla\{0,1\}(//; s/)$//; s/deg//; s/%//g' | tr ',/' '  ')
  [ $# -ge 3 ] || continue
  s=${2%.*}; l=${3%.*}
  case "$s$l" in *[!0-9]*) continue ;; esac
  [ "$s" -gt 0 ] && [ "$l" -gt 0 ] && [ "$l" -lt 100 ] && found="$found hsl$1-$s-$l"
done
N=$(echo $found | tr ' ' '\n' | grep -v '^$' | sort -u | wc -l | tr -d ' ')
[ "$N" -ge 2 ] || { echo "Critère 9 : il faut au moins deux couleurs différentes qui ne soient ni grises, ni noires, ni blanches, en #hexa, rgb(…) ou hsl(…) ; la feuille en a $N."; exit 1; }
echo "Critère 9 : la feuille utilise $N couleurs, hors gris, noir et blanc."
```

```verify
D=~/byte-layers/web/portfolio
F=$D/index.html
[ -f "$F" ] || { echo "Le fichier $F n'existe pas."; exit 1; }
CSS=$(perl -0pe 's/<!--.*?-->//gs; s/[\r\n]/ /g' "$F" | grep -oiE '<link [^>]*rel="stylesheet"[^>]*>' | head -1 | sed -n 's/.*href="\([^"]*\)".*/\1/p')
C=$D/${CSS#./}
[ -n "$CSS" ] && [ -f "$C" ] || { echo "Critère 10 : reliez d'abord une feuille de style (critère 7)."; exit 1; }
S=$(perl -0pe 's{/\*.*?\*/}{}gs; s/[\r\n]/ /g' "$C")
echo "$S" | grep -qE 'font-family:[^;}]*,[^;}]*(sans-serif|serif|monospace|cursive|system-ui)[[:space:]]*(;|\}|!)' || { echo "Critère 10 : la police doit avoir une liste de repli, finie par une famille générique : font-family: system-ui, \"Segoe UI\", sans-serif;"; exit 1; }
echo "$S" | grep -qE 'line-height:[[:space:]]*[0-9.]' || { echo "Critère 10 : il manque un interligne, par exemple line-height: 1.6; sur body."; exit 1; }
echo "Critère 10 : une police avec sa liste de repli, et un interligne."
```

```verify
D=~/byte-layers/web/portfolio
F=$D/index.html
[ -f "$F" ] || { echo "Le fichier $F n'existe pas."; exit 1; }
CSS=$(perl -0pe 's/<!--.*?-->//gs; s/[\r\n]/ /g' "$F" | grep -oiE '<link [^>]*rel="stylesheet"[^>]*>' | head -1 | sed -n 's/.*href="\([^"]*\)".*/\1/p')
C=$D/${CSS#./}
[ -n "$CSS" ] && [ -f "$C" ] || { echo "Critère 11 : reliez d'abord une feuille de style (critère 7)."; exit 1; }
S=$(perl -0pe 's{/\*.*?\*/}{}gs; s/[\r\n]/ /g' "$C")
echo "$S" | grep -qE 'padding(-[a-z]+)?:[^;}]*[1-9]' || { echo "Critère 11 : il faut au moins un padding non nul, l'espace intérieur d'un bloc."; exit 1; }
echo "$S" | grep -qE 'margin(-[a-z]+)?:[^;}]*([1-9]|auto)' || { echo "Critère 11 : il faut au moins une marge non nulle, l'espace entre deux blocs."; exit 1; }
echo "Critère 11 : padding dedans, marges dehors. Votre portfolio, version 1, est prêt : ouvrez-le dans le navigateur et regardez-le comme un visiteur."
```

Une dernière vérification, que les boutons ne font pas : déposez `index.html` sur le [validateur HTML du W3C](https://validator.w3.org/#validate_by_upload) et `style.css` sur le [validateur CSS](https://jigsaw.w3.org/css-validator/#validate_by_upload). Ils repèrent ce que le navigateur répare en silence : une balise mal fermée, un point-virgule oublié.

Votre portfolio a ses fondations. Le cours suivant commence par comprendre comment les boîtes se rangent toutes seules dans la page, avant de les disposer vous-même : [Le flux normal](https://byte-layers.com/fr/bits/normal-flow).
