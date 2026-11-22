---
title: "Mon portfolio v2 : adaptatif, accessible, avec un formulaire"
description: "Reprendre son portfolio et le rendre prêt à être montré : les 17 points de la checklist (structure, mise en forme, adaptation), un formulaire de contact relié, des couleurs en variables, puis un audit d'accessibilité avec Lighthouse et une grille RGAA. Sans corrigé : chaque point est vérifié dans vos fichiers."
tags:
  - challenge
  - html
  - css
difficulty: beginner
duration: 150
introTitle: "Le défi"
requires: "0.4.0"
options:
  allowManualProgress: false
  autoCompleteOnNext: unverifiable
---

Ce challenge prouve que vous savez faire une page **adaptative**, **accessible** et dotée d'un **formulaire de contact**, sans guide pas à pas. Vous reprenez votre portfolio, celui du challenge [Mon portfolio v1](https://byte-layers.com/fr/challenges/portfolio-v1-challenge), et vous le menez jusqu'aux 17 points de la checklist, puis vous l'auditez.

Il n'y a **pas de corrigé** : c'est votre page, votre sujet, vos couleurs, et il n'existe pas une bonne réponse. Chaque point a un bouton qui vérifie ce qui se vérifie dans vos fichiers, et des **indices** qui se dévoilent un par un. Les utiliser ne coûte rien.

## Avant de commencer

- **Ce qu'il faut savoir** : ce qu'enseignent les bits du cours, du [flux normal](https://byte-layers.com/fr/bits/normal-flow) à [Tailwind](https://byte-layers.com/fr/bits/css-build-tools), et le lab [HTML et CSS avancé, sur votre machine](https://byte-layers.com/fr/labs/html-css-advanced-lab), qui en a pratiqué chaque notion. Le lab est votre meilleur modèle : rouvrez `~/byte-layers/web/advanced` quand un point vous échappe.
- **Ce qu'il faut avoir** : VS Code, un navigateur récent, et l'extension Live Preview pour l'audit Lighthouse de la tâche 4.
- **Le dossier** : `~/byte-layers/web/portfolio`, le même que pour la v1. Si vous n'avez pas fait la v1, un point de départ y est créé à l'ouverture : `index.html`, un squelette minimal, et `style.css`, vide. Un dossier existant n'est jamais modifié. Vos fichiers restent sur votre poste à la fin.
- **La méthode** : écrivez d'abord tout le contenu en HTML, sans style, puis le CSS. Vous verrez mieux la structure, et le CSS ira plus vite.

Les vérifications lisent `index.html` et toutes les feuilles `.css` du dossier. Elles contrôlent ce qui se lit dans un fichier ; ce qui demande un jugement (un `alt` qui décrit vraiment l'image, des classes nommées par leur rôle) ou un geste (la page à 360 px) est dit comme tel, et reste à votre charge.

# Tâche 1 : la structure et le sens

## 1. Un squelette valide

```setup
D=~/byte-layers/web/portfolio
if [ ! -f "$D/index.html" ]; then
  mkdir -p "$D"
  cat > "$D/index.html" <<'EOF'
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <!-- Votre portfolio : tout est à écrire. -->
</body>
</html>
EOF
  [ -f "$D/style.css" ] || : > "$D/style.css"
fi
```

**Critère :** la page a un doctype, une langue déclarée sur `html`, un encodage, un titre non vide et la balise `meta viewport`.

```hint
Le squelette tient en six lignes avant `body` : `<!DOCTYPE html>`, `<html lang="fr">`, `<meta charset="utf-8">`, `<meta name="viewport" content="width=device-width, initial-scale=1">`, `<title>…</title>`.
```

```verify
D=~/byte-layers/web/portfolio; F="$D/index.html"
[ -f "$F" ] || { echo "Il n'y a pas de index.html dans $D."; exit 1; }
H=$(tr -d '\n' < "$F")
head -c 200 "$F" | grep -iq '<!DOCTYPE html>' || { echo "Le fichier ne commence pas par <!DOCTYPE html>."; exit 1; }
echo "$H" | grep -Eq '<html[^>]*lang="[a-z]{2}' || { echo "La langue n'est pas déclarée : <html lang=\"fr\">."; exit 1; }
echo "$H" | grep -Eiq '<meta[^>]*charset=' || { echo "Il manque <meta charset=\"utf-8\">."; exit 1; }
echo "$H" | grep -Eq '<title>[^<]*[^<[:space:]][^<]*</title>' || { echo "La page n'a pas de titre, ou un titre vide : <title>…</title>."; exit 1; }
echo "$H" | grep -Eiq '<meta[^>]+name="viewport"[^>]*width=device-width' || { echo "Il manque la balise meta viewport."; exit 1; }
echo "Le squelette est complet."
```

## 2. Les balises sémantiques

**Critère :** la page a un `header`, un `nav`, un `main` et un `footer`, et au moins une `section` ou un `article`.

```hint
Le menu va dans `nav`, lui-même souvent dans `header` ; le contenu principal dans `main`, découpé en `section` ; le nom et l'année dans `footer`.
```

```verify
H=$(tr -d '\n' < ~/byte-layers/web/portfolio/index.html 2>/dev/null)
for t in header nav main footer; do
  echo "$H" | grep -Eq "<$t[ >]" || { echo "Il manque la balise <$t>."; exit 1; }
done
echo "$H" | grep -Eq '<(section|article)[ >]' || { echo "Le contenu n'est découpé ni en section ni en article."; exit 1; }
echo "Les régions sémantiques sont en place."
```

## 3. Une hiérarchie de titres cohérente

**Critère :** un seul `h1`, au moins un `h2`, et aucun niveau sauté (pas de `h3` sans `h2`, pas de `h4` sans `h3`…).

```hint
Le `h1` est le titre de la page, votre nom par exemple. Chaque section commence par un `h2` ; un sous-titre dans une section est un `h3`.
```

```verify
F=~/byte-layers/web/portfolio/index.html
n() { grep -oiE "<h$1[ >]" "$F" | wc -l | tr -d ' '; }
[ "$(n 1)" -eq 1 ] || { echo "La page doit avoir exactement un h1 (elle en a $(n 1))."; exit 1; }
[ "$(n 2)" -ge 1 ] || { echo "La page n'a aucun h2 : chaque section commence par un h2."; exit 1; }
for k in 3 4 5 6; do
  p=$((k-1))
  if [ "$(n $k)" -gt 0 ] && [ "$(n $p)" -eq 0 ]; then echo "Un niveau est sauté : un h$k sans aucun h$p."; exit 1; fi
done
echo "Un h1, des h2, aucun niveau sauté."
```

## 4. Au moins une liste

**Critère :** la page contient une liste `ul` ou `ol`, avec ses `li`.

```hint
Le menu est déjà une liste, si vous l'écrivez comme dans le lab ; une liste de compétences en est une autre.
```

```verify
H=$(tr -d '\n' < ~/byte-layers/web/portfolio/index.html 2>/dev/null)
echo "$H" | grep -Eq '<(ul|ol)[ >].*<li[ >]' || { echo "La page n'a aucune liste ul ou ol avec des li."; exit 1; }
echo "La page a au moins une liste."
```

## 5. Des images avec un texte alternatif

**Critère :** au moins une image, et chaque image a un attribut `alt` ; au moins une a un `alt` non vide. Que ce texte décrive vraiment l'image ne se vérifie pas ici : relisez-le en vous demandant ce qu'entendrait quelqu'un qui ne la voit pas.

```hint
Une image qui informe : `alt="Le site du club, page d'accueil"`. Une image décorative : `alt=""`, vide, pour que le lecteur d'écran l'ignore. Prenez vos images dans une banque libre de droits (Unsplash, Pexels, unDraw), ou dessinez un SVG comme dans le lab.
```

```verify
F=~/byte-layers/web/portfolio/index.html
I=$(grep -oiE '<img[^>]*>' "$F" | wc -l | tr -d ' ')
[ "$I" -ge 1 ] || { echo "La page n'a aucune image."; exit 1; }
A=$(grep -oiE '<img[^>]*>' "$F" | grep -ciE 'alt=')
[ "$A" -eq "$I" ] || { echo "$((I-A)) image(s) sur $I n'ont pas d'attribut alt."; exit 1; }
grep -oiE '<img[^>]*>' "$F" | grep -qiE 'alt="[^"]*[^"[:space:]][^"]*"' || { echo "Aucune image n'a de texte alternatif non vide."; exit 1; }
echo "Les $I image(s) ont un alt."
```

## 6. Au moins trois liens, dont un externe dans un nouvel onglet

**Critère :** au moins trois liens `a href`, dont un vers une adresse en `http` ou `https` qui s'ouvre dans un nouvel onglet (`target="_blank"`).

```hint
Les liens du menu comptent. Pour le lien externe : `<a href="https://github.com/…" target="_blank">mon GitHub</a>`.
```

```verify
F=~/byte-layers/web/portfolio/index.html
[ "$(grep -oiE '<a[^>]*href=' "$F" | wc -l | tr -d ' ')" -ge 3 ] || { echo "La page a moins de trois liens."; exit 1; }
grep -oiE '<a[^>]*>' "$F" | grep -iE 'href="https?://' | grep -qi 'target="_blank"' || { echo "Aucun lien vers une adresse http(s) ne s'ouvre dans un nouvel onglet : target=\"_blank\"."; exit 1; }
echo "Au moins trois liens, dont un externe dans un nouvel onglet."
```

## 7. Un formulaire de contact, chaque champ relié et nommé

**Critère :** un `form` ; chaque champ (`input`, `select`, `textarea`, hors boutons) a un `id`, un `name`, et une étiquette `label` dont le `for` reprend son `id` ; au moins un champ `type="email"` et au moins un champ `required`.

```hint
Le modèle d'un champ : `<label for="email">Votre e-mail</label>` puis `<input type="email" id="email" name="email" required>`. Testez en cliquant sur chaque étiquette : le curseur doit aller dans le champ.
```

```hint
Sans `action`, et avec `method="get"`, le formulaire s'envoie à la page elle-même : la barre d'adresse montre alors chaque `name=valeur` envoyé, comme à l'étape 4 du lab.
```

```verify
F=~/byte-layers/web/portfolio/index.html
H=$(tr -d '\n' < "$F")
echo "$H" | grep -Eiq '<form[ >]' || { echo "La page n'a pas de formulaire."; exit 1; }
FIELDS=$(echo "$H" | grep -oiE '<(input|select|textarea)[^>]*>' | grep -viE 'type="(submit|button|reset|hidden)"')
[ -n "$FIELDS" ] || { echo "Le formulaire n'a aucun champ."; exit 1; }
while IFS= read -r f; do
  id=$(echo "$f" | sed -nE 's/.*[[:space:]]id="([^"]+)".*/\1/p')
  [ -n "$id" ] || { echo "Un champ n'a pas d'id : $f"; exit 1; }
  echo "$f" | grep -Eq '[[:space:]]name="[^"]+"' || { echo "Le champ $id n'a pas de name : sa valeur ne serait pas envoyée."; exit 1; }
  echo "$H" | grep -Eq "<label[^>]*for=\"$id\"" || { echo "Aucune étiquette n'est reliée au champ $id : <label for=\"$id\">."; exit 1; }
done <<< "$FIELDS"
echo "$FIELDS" | grep -qi 'type="email"' || { echo "Aucun champ de type email."; exit 1; }
echo "$FIELDS" | grep -qiE '[[:space:]]required([[:space:]>=/]|$)' || { echo "Aucun champ n'est obligatoire : required."; exit 1; }
echo "Chaque champ du formulaire est relié à son étiquette et nommé."
```

# Tâche 2 : la mise en forme

## 8. Une feuille de style externe

**Critère :** la page charge une feuille de style par `<link rel="stylesheet">`, et le fichier visé existe dans le dossier.

```hint
`<link rel="stylesheet" href="style.css">` dans le `head`. Le nom dans `href` et le nom du fichier doivent être identiques, majuscules comprises.
```

```verify
D=~/byte-layers/web/portfolio
L=$(tr -d '\n' < "$D/index.html" | grep -oiE '<link[^>]*rel="stylesheet"[^>]*>' | head -1)
[ -n "$L" ] || { echo "La page ne charge aucune feuille de style : <link rel=\"stylesheet\" href=\"style.css\">."; exit 1; }
HREF=$(echo "$L" | sed -nE 's/.*href="([^"]+)".*/\1/p')
case "$HREF" in http*) echo "La feuille liée est en ligne ($HREF) : il faut aussi votre propre feuille, dans le dossier."; exit 1 ;; esac
[ -f "$D/$HREF" ] || { echo "La page charge $HREF, mais ce fichier n'existe pas dans $D."; exit 1; }
echo "La page charge $HREF, qui existe."
```

## 9. Vos propres classes

**Critère :** au moins trois classes différentes, utilisées dans le HTML et visées dans le CSS. Qu'elles soient nommées par leur **rôle** (`.projets`, `.bouton-contact`) et non par leur apparence (`.rouge`, `.gauche`) ne se vérifie pas ici : relisez-les.

```hint
Une classe sert dans les deux fichiers : `class="projets"` dans le HTML, `.projets { … }` dans le CSS.
```

```verify
D=~/byte-layers/web/portfolio
C=$(cat "$D"/*.css 2>/dev/null)
N=0
for c in $(grep -oE 'class="[^"]+"' "$D/index.html" | sed -E 's/class="([^"]+)"/\1/' | tr ' ' '\n' | sort -u); do
  printf '%s' "$C" | grep -Eq "\.$c([^a-zA-Z0-9_-]|$)" && N=$((N+1))
done
[ "$N" -ge 3 ] || { echo "Seulement $N classe(s) sont à la fois dans le HTML et dans le CSS : il en faut au moins trois."; exit 1; }
echo "$N classes servent dans le HTML et dans le CSS."
```

## 10. Une couleur dominante et une couleur d'accent, en variables

**Critère :** au moins deux variables CSS déclarées sur `:root`, et utilisées au moins deux fois avec `var()`. Les gris, les blancs et les fonds ne comptent pas comme couleurs du thème : que vos deux variables soient de vraies couleurs, c'est à vous de le juger.

```hint
`:root { --dominante: rgb(30, 64, 175); --accent: rgb(219, 39, 119); }`, puis `color: var(--dominante);` dans les titres, `background-color: var(--accent);` sur le bouton.
```

```verify
C=$(cat ~/byte-layers/web/portfolio/*.css 2>/dev/null | tr -d '\n')
R=$(echo "$C" | grep -oE ':root[[:space:]]*\{[^}]*\}' | grep -oE -- '--[a-zA-Z0-9-]+[[:space:]]*:' | wc -l | tr -d ' ')
[ "$R" -ge 2 ] || { echo "La règle :root doit déclarer au moins deux variables (elle en déclare $R)."; exit 1; }
U=$(echo "$C" | grep -oE 'var\([[:space:]]*--' | wc -l | tr -d ' ')
[ "$U" -ge 2 ] || { echo "Les variables ne servent que $U fois : utilisez-les avec var(--…)."; exit 1; }
echo "$R variables sur :root, utilisées $U fois."
```

## 11. Une police lisible, avec sa liste de repli, et un interligne confortable

**Critère :** un `font-family` qui donne une liste de polices (au moins une virgule), et un `line-height`.

```hint
`body { font-family: system-ui, "Segoe UI", sans-serif; line-height: 1.6; }` : si la première police manque, le navigateur prend la suivante.
```

```verify
C=$(cat ~/byte-layers/web/portfolio/*.css 2>/dev/null | tr -d '\n')
echo "$C" | grep -Eq 'font-family:[^;}]*,' || { echo "Aucun font-family ne donne de police de repli (une liste séparée par des virgules)."; exit 1; }
echo "$C" | grep -Eq 'line-height:' || { echo "Aucun line-height : l'interligne reste celui du navigateur."; exit 1; }
echo "La police a sa liste de repli, et l'interligne est réglé."
```

## 12. Des espacements maîtrisés

**Critère :** la feuille de style règle des `padding` (l'espace à l'intérieur des boîtes) et des `margin` (l'espace entre elles). Qu'ils soient bien choisis se juge à l'œil : rien ne doit coller au bord de l'écran ni à son voisin.

```hint
Un bouton a du `padding` ; deux sections sont séparées par une `margin` ; `gap` espace les enfants d'un conteneur flex ou grid.
```

```verify
C=$(cat ~/byte-layers/web/portfolio/*.css 2>/dev/null | tr -d '\n')
echo "$C" | grep -Eq 'padding(-[a-z]+)?:' || { echo "Aucun padding dans la feuille de style."; exit 1; }
echo "$C" | grep -Eq 'margin(-[a-z]+)?:' || { echo "Aucune margin dans la feuille de style."; exit 1; }
echo "La feuille règle des padding et des margin."
```

## 13. Au moins une zone disposée avec Flexbox ou Grid

**Critère :** au moins un `display: flex` ou `display: grid`.

```hint
Un entête avec le nom à gauche et le menu à droite (Flexbox), ou une grille de projets (Grid), comme aux étapes 2 et 3 du lab.
```

```verify
C=$(cat ~/byte-layers/web/portfolio/*.css 2>/dev/null | tr -d '\n')
echo "$C" | grep -Eq 'display:[[:space:]]*(flex|grid|inline-flex|inline-grid)' || { echo "Aucune zone n'est disposée avec Flexbox ou Grid."; exit 1; }
echo "Au moins une zone est disposée avec Flexbox ou Grid."
```

# Tâche 3 : l'adaptation

## 14. Les fondations : box-sizing et images

**Critère :** la règle `box-sizing: border-box` sur tous les éléments, et `img { max-width: 100%; height: auto; }`.

```hint
Deux règles, en haut de la feuille : `* { box-sizing: border-box; }` et `img { max-width: 100%; height: auto; }`.
```

```verify
C=$(cat ~/byte-layers/web/portfolio/*.css 2>/dev/null | tr -d '\n')
echo "$C" | grep -Eq 'box-sizing:[[:space:]]*border-box' || { echo "Il manque box-sizing: border-box."; exit 1; }
echo "$C" | grep -Eq '(^|[},[:space:]])img[[:space:]]*\{[^}]*max-width:[[:space:]]*100%' || { echo "Il manque img { max-width: 100%; height: auto; }."; exit 1; }
echo "Les fondations sont posées."
```

## 15 et 16. Des largeurs maximales, et aucun défilement horizontal de 360 à 1600 px

**Critères :** aucune largeur fixe de `400px` ou plus (des `max-width` à la place) ; et le **test décisif** : en mode appareil, **Responsive**, de `360px` à `1600px`, la page n'a jamais de barre de défilement horizontale.

La vérification ne contrôle que le premier critère : le second demande un navigateur. Faites-le vous-même, lentement, en faisant glisser le bord de la page ; si une barre apparaît, survolez les éléments dans le panneau HTML pour trouver celui qui dépasse.

```hint
Cherchez `width:` dans vos feuilles (Ctrl+F, ou Cmd+F). Une boîte de contenu s'écrit `max-width: 960px; margin: 0 auto;`.
```

```verify
BIG=$(cat ~/byte-layers/web/portfolio/*.css 2>/dev/null | grep -oE '(^|[^-a-z])width:[[:space:]]*[0-9]+px' | grep -oE '[0-9]+' | awk '$1 >= 400' | head -1)
[ -z "$BIG" ] || { echo "Une feuille a encore une largeur fixe de ${BIG}px : remplacez width par max-width."; exit 1; }
cat ~/byte-layers/web/portfolio/*.css 2>/dev/null | grep -Eq 'max-width:' || { echo "Aucune largeur maximale : le contenu s'étale sur toute la largeur des grands écrans."; exit 1; }
echo "Aucune largeur fixe de 400 px ou plus. Le test de 360 à 1600 px reste à faire dans le navigateur."
```

## 17. Au moins une media query, en mobile-first

**Critère :** au moins une media query `min-width`, qui enrichit pour les grands écrans un style écrit d'abord pour le téléphone.

```hint
`@media (min-width: 700px) { … }`, écrite après les règles de base. `max-width` dans une media query, c'est l'approche inverse : le contrôle ne la compte pas.
```

```verify
cat ~/byte-layers/web/portfolio/*.css 2>/dev/null | tr -d '\n' | grep -Eq '@media[^{]*min-width' || { echo "Aucune media query min-width."; exit 1; }
echo "Au moins une media query mobile-first."
```

# Tâche 4 : l'audit d'accessibilité

## Le focus visible et le mouvement

**Critère :** aucune règle ne supprime le contour du focus (`outline: none` ou `outline: 0`) ; et si vos feuilles ont des transitions ou des animations, une media query `prefers-reduced-motion: reduce` les coupe.

```hint
Pour changer le contour sans le supprimer : `a:focus-visible { outline: 3px solid var(--accent); }`. Pour le mouvement : `@media (prefers-reduced-motion: reduce) { … { transition: none; animation: none; } }`.
```

```verify
C=$(cat ~/byte-layers/web/portfolio/*.css 2>/dev/null | tr -d '\n')
[ -n "$C" ] || { echo "Le dossier n'a encore aucune feuille de style."; exit 1; }
echo "$C" | grep -Eq 'outline:[[:space:]]*(none|0)([[:space:]]*[;}]|[[:space:]]*!)' && { echo "Une règle supprime le contour du focus (outline: none ou 0)."; exit 1; }
if echo "$C" | grep -Eq '(transition|animation):[[:space:]]*[^n;}]'; then
  echo "$C" | grep -Eq 'prefers-reduced-motion:[[:space:]]*reduce' || { echo "Vos feuilles ont des transitions ou des animations, mais aucune media query prefers-reduced-motion: reduce."; exit 1; }
fi
grep -Eq ':focus-visible|:focus' ~/byte-layers/web/portfolio/*.css || { echo "Aucun style de focus : ajoutez un :focus-visible qui rend le focus bien visible, par exemple sur les liens et le bouton."; exit 1; }
echo "Le focus reste visible, et le mouvement se coupe sur demande."
```

## Lighthouse et la grille RGAA

**Critères :** un fichier `audit.md` dans le dossier du portfolio, avec le score de Lighthouse en accessibilité, d'**au moins 90**, et la grille des neuf critères de l'étape 6 du lab, chacun noté `C` ou `NA`, sans aucun `NC`.

Lancez Lighthouse sur votre page servie par Live Preview (palette de commandes, `Live Preview: Show Preview (External Browser)`), catégorie **Accessibility**. Puis passez la grille, en reprenant le tableau de l'étape 6 du lab, avec cette ligne de score en tête :

```markdown
Score Lighthouse : 
```

```hint
Si le score est sous 90, chaque défaut de la liste de Lighthouse a un lien vers son explication et montre l'élément en cause. Les plus fréquents : un contraste trop faible, une image sans `alt`, un lien dont le texte est vide.
```

```hint
Pour les critères 10.7 et 12.8, cliquez dans la page puis appuyez sur Tab, encore et encore : chaque lien et chaque champ doit montrer un contour, dans l'ordre de lecture.
```

```verify
A=~/byte-layers/web/portfolio/audit.md
[ -f "$A" ] || { echo "Il n'y a pas de audit.md dans ~/byte-layers/web/portfolio."; exit 1; }
S=$(sed -nE 's/^Score Lighthouse[^:]*:[[:space:]]*([0-9]+).*/\1/p' "$A" | tail -1)
[ -n "$S" ] || { echo "Notez le score de Lighthouse en accessibilité, un nombre, après « Score Lighthouse : »."; exit 1; }
[ "$S" -ge 90 ] || { echo "Le score de Lighthouse est $S : corrigez les défauts qu'il signale, jusqu'à 90 au moins, puis notez le nouveau score."; exit 1; }
N=$(grep -cE '^\|[[:space:]]*[0-9]+\.[0-9]+[[:space:]]*\|' "$A")
[ "$N" -ge 9 ] || { echo "La grille doit avoir les neuf critères de l'étape 6 du lab (elle en a $N)."; exit 1; }
F=$(grep -cE '^\|[[:space:]]*[0-9]+\.[0-9]+[[:space:]]*\|.*\|[[:space:]]*(C|NA)[[:space:]]*\|[[:space:]]*$' "$A")
[ "$F" -eq "$N" ] || { echo "Chaque critère doit être noté C ou NA dans la dernière colonne ; un NC se corrige dans la page avant d'être noté C."; exit 1; }
echo "Score $S, et les $N critères de la grille sont C ou NA. Challenge terminé."
```

## La suite

Votre portfolio est prêt à être montré : il se lit sur un téléphone comme sur un grand écran, au clavier comme à la souris, et son formulaire envoie ce qu'il doit. Il ne réagit encore à rien, et ses projets sont écrits à la main. Le cours suivant lui apprend à réagir, avec JavaScript, en commençant par le bit [La console, premier contact](https://byte-layers.com/fr/bits/js-console).
