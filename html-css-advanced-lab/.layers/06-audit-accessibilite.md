---
title: "06 - Auditer sa page : Lighthouse et une grille RGAA allégée"
description: "Ajouter une section d'avis qui contient des erreurs, mesurer la page avec Lighthouse, la passer à une grille de neuf critères RGAA, corriger, puis mesurer de nouveau"
---

Une page accessible, ça se vérifie. Vous ajoutez une section qui contient des erreurs fréquentes, puis vous auditez toute la page de deux façons : avec **Lighthouse**, un outil automatique, et avec une **grille RGAA allégée**, à la main. Vous corrigez, et vous mesurez de nouveau.

## 06.1 - Ajouter la section des avis

Cette sous-étape est un **support** : elle ajoute à la page des erreurs à trouver. Collez cette section dans `index.html`, dans `main`, après les projets :

```html
<section class="avis">
  <h4>Ils ont travaillé avec moi</h4>
  <img src="images/sommet.svg">
  <p class="citation">« Un site clair, livré à temps. » Le club de rando</p>
</section>
```

Puis ces deux règles à la fin de `style.css`, **avant** la media query :

```css
.citation {
  color: #aaa;
}

a:focus {
  outline: none;
}
```

## 06.2 - Mesurer la page avec Lighthouse

**Lighthouse** est intégré aux outils de développement de Chrome et d'Edge. Il refuse les pages ouvertes depuis un fichier (`file://`) : il lui faut une adresse en `http://`. L'extension Live Preview de VS Code en fournit une : ouvrez la palette de commandes (Ctrl+Maj+P, ou Cmd+Maj+P sous macOS), tapez `Live Preview: Show Preview (External Browser)`, puis Entrée. La page s'ouvre dans le navigateur, à une adresse comme `http://127.0.0.1:3000/index.html`.

1. Ouvrez les outils de développement (F12), onglet **Lighthouse** (il peut être caché derrière le chevron `»`).
2. Cochez seulement la catégorie **Accessibility**, choisissez **Desktop**, puis cliquez sur **Analyze page load**.
3. Notez le **score** sur 100, et lisez la liste des défauts : chacun a un lien vers son explication et montre l'élément en cause.

Dans votre dossier, créez un fichier `audit.md` et collez-y cette grille. Notez le score après « avant » ; la ligne « après » attendra les corrections.

```markdown
# Audit d'accessibilité de index.html

Score Lighthouse avant :
Score Lighthouse après :

| Critère | Question | Résultat |
|---|---|---|
| 1.1 | Chaque image porteuse d'information a-t-elle une alternative textuelle ? | |
| 1.2 | Chaque image de décoration est-elle ignorée par les lecteurs d'écran (alt vide) ? | |
| 3.2 | Le contraste entre le texte et son fond est-il suffisant (4,5:1) ? | |
| 8.3 | La langue de la page est-elle déclarée ? | |
| 8.5 | La page a-t-elle un titre (balise title) ? | |
| 9.1 | Les titres sont-ils hiérarchisés, sans niveau sauté ? | |
| 10.7 | Le focus est-il visible sur chaque élément qu'on atteint au clavier ? | |
| 11.1 | Chaque champ de formulaire a-t-il une étiquette ? | |
| 12.8 | L'ordre de passage avec la touche Tab est-il cohérent ? | |
```

## 06.3 - Passer la grille, critère par critère

Ces neuf critères viennent du **RGAA 4.1**, le référentiel français, qui en compte 106. Pour chacun, la dernière colonne reçoit l'un de trois résultats :

| Résultat | Veut dire |
|---|---|
| `C` | conforme : le critère est respecté partout sur la page |
| `NC` | non conforme : au moins un élément ne le respecte pas |
| `NA` | non applicable : la page n'a rien de concerné (pas d'image décorative, par exemple) |

Certains critères se lisent dans le rapport de Lighthouse (1.1, 3.2, 8.3, 8.5, 11.1) ; les autres demandent un geste à la main :

- pour **9.1**, relisez les balises `h1` à `h6` de `index.html` dans l'ordre ;
- pour **10.7** et **12.8**, cliquez dans la page, puis appuyez sur Tab, encore et encore : chaque lien et chaque champ doit montrer un contour, dans l'ordre de lecture ;
- pour **1.2**, demandez-vous si chaque image apporte une information, ou si elle n'est qu'une décoration.

Remplissez la grille telle que vous trouvez la page, **avant** de corriger.

## 06.4 - Corriger, puis mesurer de nouveau

Corrigez chaque critère `NC` dans `index.html` et `style.css`, avec les corrections du bit sur l'accessibilité. Puis relancez Lighthouse, notez le nouveau score après « après », et mettez à jour la colonne des résultats : il ne doit plus rester de `NC`.

> 💡 **Remarque.** Le score de Lighthouse ne dit pas tout : l'outil a vu l'image sans `alt`, mais il ne sait pas si votre nouvel `alt` décrit vraiment l'image, ni si l'ordre de vos titres a du sens. C'est le rôle de la grille et de vos tests au clavier.

```verify
D=~/byte-layers/web/advanced
A="$D/audit.md"
[ -f "$A" ] || { echo "Il n'y a pas de audit.md dans $D."; exit 1; }
grep -Eq '^Score Lighthouse avant :[[:space:]]*[0-9]+' "$A" || { echo "Notez le score de Lighthouse avant corrections, un nombre, après « Score Lighthouse avant : »."; exit 1; }
grep -Eq '^Score Lighthouse après :[[:space:]]*[0-9]+' "$A" || { echo "Relancez Lighthouse après vos corrections, et notez le score après « Score Lighthouse après : »."; exit 1; }
N=$(grep -cE '^\|[[:space:]]*[0-9]+\.[0-9]+[[:space:]]*\|' "$A")
F=$(grep -cE '^\|[[:space:]]*[0-9]+\.[0-9]+[[:space:]]*\|.*\|[[:space:]]*(C|NC|NA)[[:space:]]*\|[[:space:]]*$' "$A")
[ "$N" -ge 9 ] || { echo "La grille de audit.md doit garder ses neuf critères."; exit 1; }
[ "$F" -eq "$N" ] || { echo "Chaque critère de la grille attend un résultat dans la dernière colonne : C, NC ou NA."; exit 1; }
if grep -Eq '\|[[:space:]]*NC[[:space:]]*\|[[:space:]]*$' "$A"; then echo "La grille contient encore un critère NC : corrigez-le dans la page, puis mettez la grille à jour."; exit 1; fi
H=$(tr -d '\n' < "$D/index.html")
echo "$H" | grep -Eq '<h4' && { echo "La section des avis a encore un h4 : après des h2, le niveau suivant est h3, ou h2 pour une nouvelle section."; exit 1; }
[ "$(grep -o '<img' "$D/index.html" | wc -l)" -eq "$(grep -oE '<img[^>]*alt=' "$D/index.html" | wc -l)" ] || { echo "Une image de index.html n'a pas d'attribut alt."; exit 1; }
C=$(tr -d '\n' < "$D/style.css")
echo "$C" | grep -Eiq '\.citation[[:space:]]*\{[^}]*color:[[:space:]]*(#aaa|#aaaaaa)' && { echo "Le texte de .citation est encore #aaa, contraste 2,3:1 sur blanc : foncez-le."; exit 1; }
echo "$C" | grep -Eq 'outline:[[:space:]]*(none|0)' && { echo "style.css supprime encore le contour du focus (outline: none)."; exit 1; }
echo "La grille est remplie, sans NC, et les erreurs de la section des avis sont corrigées."
```

```hint
Les quatre erreurs de la section des avis : un `h4` après des `h2` (9.1), une image sans `alt` (1.1), un gris `#aaa` sur blanc (3.2), et `outline: none` (10.7). Pour le gris, `#555` donne 7,5:1 sur blanc.
```

````solution
Dans `index.html` :

```html
<section class="avis">
  <h2>Ils ont travaillé avec moi</h2>
  <img src="images/sommet.svg" alt="Le logo du club de rando : une montagne sur fond bleu">
  <p class="citation">« Un site clair, livré à temps. » Le club de rando</p>
</section>
```

Dans `style.css`, la règle `a:focus` est supprimée, ou remplacée par un contour visible :

```css
.citation {
  color: #555;
}

a:focus-visible {
  outline: 3px solid rgb(219, 39, 119);
  outline-offset: 2px;
}
```

Dans `audit.md`, la grille d'une page corrigée ressemble à ceci, les scores dépendant de votre page :

```markdown
Score Lighthouse avant : 82
Score Lighthouse après : 100

| Critère | Question | Résultat |
|---|---|---|
| 1.1 | Chaque image porteuse d'information a-t-elle une alternative textuelle ? | C |
| 1.2 | Chaque image de décoration est-elle ignorée par les lecteurs d'écran (alt vide) ? | NA |
| 3.2 | Le contraste entre le texte et son fond est-il suffisant (4,5:1) ? | C |
| 8.3 | La langue de la page est-elle déclarée ? | C |
| 8.5 | La page a-t-elle un titre (balise title) ? | C |
| 9.1 | Les titres sont-ils hiérarchisés, sans niveau sauté ? | C |
| 10.7 | Le focus est-il visible sur chaque élément qu'on atteint au clavier ? | C |
| 11.1 | Chaque champ de formulaire a-t-il une étiquette ? | C |
| 12.8 | L'ordre de passage avec la touche Tab est-il cohérent ? | C |
```
````

> 📖 [Le RGAA 4.1, critères et tests (DINUM)](https://accessibilite.numerique.gouv.fr/methode/criteres-et-tests/) · [Lighthouse, vue d'ensemble (Chrome, en anglais)](https://developer.chrome.com/docs/lighthouse/overview) · [Live Preview pour VS Code (Visual Studio Marketplace, en anglais)](https://marketplace.visualstudio.com/items?itemName=ms-vscode.live-server)
