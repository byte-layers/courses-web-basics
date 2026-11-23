"""Scènes 2D (kit plan) du bit « Une page web : HTML, CSS et JavaScript », la page construite pas à pas
(courses-web-basics/web-page-languages).

Quatre étapes, une idée chacune :
- structure : une page est une enveloppe <html> qui porte un en-tête <head> et un corps <body> (boîtes emboîtées,
  code à côté dans l'éditeur) ;
- base : la structure de base ligne par ligne, et ce que disent ses attributs (accolades et notes à droite) ;
- css : le <head> cite la feuille de style par <link> ; elle est chargée avant le corps, le premier affichage est stylé ;
- js : le <body> finit par <script src> ; le titre et le bouton existent déjà, le script les trouve et réagit au clic.

Kit plan : x vers la droite, y vers le bas, en unités de 28 px ; un enfant (in) est relatif au centre du parent.
Une règle par sorte : une partie de la page HTML est une boîte (layer si elle en contient d'autres, node sinon) ;
un fichier à part est un « file » ; la page affichée est un layer « n » qui porte ce que le visiteur voit.
Couleurs (structure, base) : r le doctype, g l'enveloppe <html>, b l'en-tête <head>, y le corps <body>.
Couleurs (css, js) : celles de l'étape « trois » : y HTML, r CSS, g JavaScript, n l'affichage par défaut.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools" / "scenes"))
from paths import outputs
from scene_kit import L, scene, send, wait, write, hud


def ent(id, kind, at, size=None, tone=None, parent=None, **kw):
    d = {"id": id, "kind": kind, "at": list(at)}
    if tone: d["tone"] = tone
    if size: d["size"] = list(size) + ([] if kind == "zone" else [1])
    if parent: d["in"] = parent
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


def line(n):
    return {"do": "line", "n": n}


# ---------- 1. structure : des boîtes emboîtées
S = [
    ent("s-doc", "node", (0, -9), (16, 2.2), "r", title="<!DOCTYPE html>", sub="déclaration"),
    ent("s-html", "layer", (0, 2.2), (16, 17.5), "g", title="<html>", sub="l'enveloppe"),
    ent("s-head", "layer", (0, -3.6), (13.5, 6), "b", parent="s-html", title="<head>", sub="l'en-tête"),
    ent("s-head-i", "node", (0, 0.9), (11, 1.8), "b", parent="s-head", title="infos pour le navigateur"),
    ent("s-body", "layer", (0, 4.2), (13.5, 6), "y", parent="s-html", title="<body>", sub="le corps"),
    ent("s-body-i", "node", (0, 0.9), (11, 1.8), "y", parent="s-body", title="ce qui s'affiche"),
]
CODE_S = ["<!DOCTYPE html>", "<html lang=\"fr\">", "<head>", "  <!-- les infos d'en-tête -->", "</head>",
          "<body>", "  <!-- le corps : titre, contenu -->", "</body>", "</html>"]
structure = {
    "id": "structure", "label": "La structure", "title": "Une enveloppe, un en-tête, un corps",
    "body": ["Une page HTML est un bloc `<html>` qui porte deux parties : l'en-tête `<head>`, pour le navigateur, puis le corps `<body>`, pour ce qui s'affiche."],
    "show": ["s-doc"],
    "links": [],
    "widgets": [{"kind": "editor", "title": "index.html", "lang": "text", "lines": CODE_S}],
    "script": [
        line(1), wait(1000),
        scene(set=[{"id": "s-doc", "label": "la page est en HTML d'aujourd'hui"}],
              say="`<!DOCTYPE html>` annonce une page en HTML d'aujourd'hui. C'est une déclaration, pas une balise."),
        wait(1200), line(2),
        scene(show=["s-html"], say="`<html>` est l'**enveloppe** : tout le reste est dedans, jusqu'à `</html>`."),
        wait(1200), line(3),
        scene(show=["s-head", "s-head-i"],
              say="`<head>`, l'**en-tête** : des informations pour le navigateur, qui ne s'affichent pas dans la page."),
        wait(1300), line(6),
        scene(show=["s-body", "s-body-i"],
              say="`<body>`, le **corps** : tout ce qui s'affiche, nos titres, nos textes, nos boutons."),
        wait(1300), line(9),
        scene(set=[{"id": "s-html", "label": "fermée"}],
              say="`</html>` ferme l'enveloppe : une page, c'est toujours un en-tête puis un corps."),
        wait(2600),
    ],
}

# ---------- 2. base : la structure de base, ligne par ligne
XC, XN = -6, 9.5            # colonne du code, colonne des notes
DY = 2.1
CODE_B = [
    ("b1", 0, "<!DOCTYPE html>", "r"),
    ("b2", 0, "<html lang=\"fr\">", "g"),
    ("b3", 1, "<head>", "b"),
    ("b4", 2, "<meta charset=\"utf-8\">", "b"),
    ("b5", 2, "<title>Titre de la page</title>", "b"),
    ("b6", 1, "</head>", "b"),
    ("b7", 1, "<body>", "y"),
    ("b8", 2, "<p>Ceci est un paragraphe</p>", "y"),
    ("b9", 1, "</body>", "y"),
    ("b10", 0, "</html>", "g"),
]
Y0 = -(len(CODE_B) - 1) * DY / 2
B = []
for i, (id, ind, txt, tone) in enumerate(CODE_B):
    B.append(ent(id, "node", (XC + ind * 0.9, Y0 + i * DY), (12.5 - ind * 1.8, 1.6), tone, title=txt))


def yl(i):
    return Y0 + (i - 1) * DY


B += [
    ent("z-html", "zone", (XC + 0.2, (yl(2) + yl(10)) / 2 - 0.5), (15.4, yl(10) - yl(2) + 3.6), "g", label="enveloppe"),
    ent("z-head", "zone", (XC + 1.1, (yl(3) + yl(6)) / 2), (13.4, yl(6) - yl(3) + 2.2), "b", label="en-tête"),
    ent("z-body", "zone", (XC + 1.1, (yl(7) + yl(9)) / 2), (13.4, yl(9) - yl(7) + 2.2), "y", label="corps"),
    ent("n-doc", "node", (XN, yl(1)), (12, 1.9), "r", title="la page est en HTML actuel"),
    ent("n-lang", "node", (XN, yl(2)), (12, 1.9), "g", title="attribut lang : la langue", sub="le contenu est en français"),
    ent("n-meta", "node", (XN, yl(4)), (12, 1.9), "b", title="attribut charset : l'encodage", sub="les accents s'affichent bien"),
    ent("n-title", "node", (XN, yl(5) + 0.4), (12, 1.9), "b", title="le nom de l'onglet"),
    ent("n-p", "node", (XN, yl(8)), (12, 1.9), "y", title="ce qui s'affiche dans la page"),
]
base = {
    "id": "base", "label": "Ligne par ligne", "title": "La structure de base, ligne par ligne",
    "body": ["Chaque ligne a un rôle. Les **attributs** précisent une balise : `nom=\"valeur\"`, dans la balise ouvrante."],
    "labels": "left",
    "show": [c[0] for c in CODE_B],
    "links": [],
    "script": [
        wait(1000),
        scene(show=["n-doc"], link=[L("b1", "n-doc")],
              say="La première ligne annonce le HTML d'aujourd'hui."),
        wait(1200),
        scene(show=["z-html", "n-lang"], link=[L("b2", "n-lang")],
              say="`lang=\"fr\"` est un **attribut** : il précise la balise `<html>`. Il dit la langue du contenu, utile aux lecteurs d'écran et aux traducteurs."),
        wait(1500),
        scene(show=["z-head", "n-meta"], link=[L("b4", "n-meta")],
              say="Dans l'en-tête, `charset=\"utf-8\"` dit comment les caractères sont codés : sans lui, les accents peuvent s'afficher en signes bizarres."),
        wait(1500),
        scene(show=["n-title"], link=[L("b5", "n-title")],
              say="`<title>` donne le texte de l'**onglet**, pas un titre dans la page."),
        wait(1300),
        scene(show=["z-body", "n-p"], link=[L("b8", "n-p")],
              say="Dans le corps, nos balises : ici un paragraphe, `<p>`, ouvert puis **fermé** par `</p>`."),
        wait(2800),
    ],
}

# ---------- 3. css : <link> dans le head
XF, XP = -9, 9
C = [
    ent("c-html", "layer", (XF, -1), (13, 12.5), "y", title="index.html"),
    ent("c-head", "layer", (0, -2.6), (11, 4.6), "y", parent="c-html", title="<head>"),
    ent("c-link", "node", (0, 0.7), (10, 1.7), "r", parent="c-head", title="<link rel=\"stylesheet\" href=\"style.css\">"),
    ent("c-body", "layer", (0, 3.2), (11, 4.6), "y", parent="c-html", title="<body>"),
    ent("c-body-i", "node", (0, 0.7), (10, 1.7), "y", parent="c-body", title="<h1> et <button>"),
    ent("c-css", "file", (0.5, -9.5), (7, 2.4), "r", title="style.css"),
    ent("c-page", "layer", (XP, -1), (11, 10), "n", title="la page affichée"),
    ent("c-h1", "node", (0, -1.8), (8, 2), "y", parent="c-page", title="Bonjour !"),
    ent("c-btn", "node", (0, 2), (6, 2), "n", parent="c-page", title="Clique-moi"),
]
css = {
    "id": "css", "label": "Le CSS", "title": "Le <head> cite la feuille de style",
    "body": ["`<link>` relie une feuille de style. Placée dans l'en-tête, elle est lue avant le corps : la page s'affiche stylée dès le début."],
    "hud": [{"label": "feuille de style", "value": "—"}],
    "labels": "left",
    "show": ["c-html", "c-head", "c-link", "c-body", "c-body-i"],
    "links": [],
    "script": [
        wait(1000),
        scene(set=[{"id": "c-link", "label": "lu en premier"}],
              say="Le navigateur lit la page de haut en bas. Dans l'en-tête, il trouve la balise `<link>`."),
        wait(1200),
        scene(show=["c-css"], link=[L("c-link", "c-css")], set=[{"id": "c-link", "label": None}],
              say="`href=\"style.css\"` est un chemin **relatif** : le fichier est à côté de la page, sur le même serveur."),
        send(["c-link", "c-css"], tone="r", label="GET style.css", reply="200"),
        scene(hud=[hud("feuille de style", "chargée", "r")], ms=300),
        scene(show=["c-page", "c-h1", "c-btn"], link=[L("c-body", "c-page")],
              say="Puis il affiche le corps : les règles sont déjà là."),
        wait(600),
        scene(set=[{"id": "c-btn", "tone": "r", "label": "rose dès le premier affichage"}],
              say="Le bouton est rose **dès le premier affichage** : c'est pour cela que le CSS se relie dans le `<head>`."),
        wait(2600),
    ],
}

# ---------- 4. js : <script> à la fin du body
J = [
    ent("j-html", "layer", (XF, -1), (13, 12.5), "y", title="index.html"),
    ent("j-head", "layer", (0, -3.6), (11, 2.8), "y", parent="j-html", title="<head>"),
    ent("j-body", "layer", (0, 2.2), (11, 7.4), "y", parent="j-html", title="<body>"),
    ent("j-h1", "node", (0, -1.4), (10, 1.6), "y", parent="j-body", title="<h1 id=\"titre\">"),
    ent("j-btn", "node", (0, 0.5), (10, 1.6), "y", parent="j-body", title="<button id=\"bouton\">"),
    ent("j-script", "node", (0, 2.4), (10, 1.6), "g", parent="j-body", title="<script src=\"script.js\"></script>"),
    ent("j-js", "file", (XF, 8.5), (8, 2.4), "g", title="script.js"),
    ent("j-page", "layer", (XP, -1), (11, 10), "n", title="la page affichée"),
    ent("j-ph1", "node", (0, -1.8), (8, 2), "y", parent="j-page", title="Bonjour !"),
    ent("j-pbtn", "node", (0, 2), (6, 2), "r", parent="j-page", title="Clique-moi"),
]
js = {
    "id": "js", "label": "Le JavaScript", "title": "Le <body> finit par le script",
    "body": ["`<script src>` relie un script. Placé juste avant `</body>`, il s'exécute quand le titre et le bouton existent déjà."],
    "hud": [{"label": "script", "value": "—"}],
    "labels": "left",
    "show": ["j-html", "j-head", "j-body", "j-h1", "j-btn", "j-script", "j-page", "j-ph1", "j-pbtn"],
    "links": [L("j-body", "j-page")],
    "script": [
        wait(1000),
        scene(set=[{"id": "j-script", "label": "en dernier"}],
              say="Le navigateur a lu le titre et le bouton : ils sont affichés. La dernière ligne du corps relie le script."),
        wait(1200),
        scene(show=["j-js"], link=[L("j-script", "j-js")], set=[{"id": "j-script", "label": None}]),
        send(["j-script", "j-js"], tone="g", label="GET script.js", reply="200"),
        scene(hud=[hud("script", "exécuté", "g")], link=[L("j-js", "j-pbtn")],
              say="Le script s'exécute : il trouve le bouton, qui existe déjà, et attend un clic."),
        wait(1300),
        scene(set=[{"id": "j-pbtn", "label": "clic"}], say="Un clic sur le bouton…", ms=400),
        wait(500),
        scene(set=[{"id": "j-ph1", "title": "Merci !", "tone": "g"}, {"id": "j-pbtn", "label": None}],
              say="… et le script remplace le texte du titre. Le HTML n'a pas changé : c'est la page affichée qui change."),
        wait(2600),
    ],
}

lesson = {
    "format": "bl-scenes/0.3", "id": "web-page-languages-page", "title": "Une page construite pas à pas (2D)",
    "lang": "fr", "kit": "plan",
    "legend": [{"tone": "r", "label": "doctype, CSS"}, {"tone": "g", "label": "<html>, JavaScript"},
               {"tone": "b", "label": "<head>"}, {"tone": "y", "label": "<body>, HTML"}],
    "entities": S + B + C + J, "steps": [structure, base, css, js],
}
write(lesson, *outputs(HERE, "page.scene.json", "web-page"))
