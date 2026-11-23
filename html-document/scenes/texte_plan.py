"""Scènes 2D (kit plan) du bit « Le squelette d'une page HTML » (courses-web-basics/html-document), suite.

Trois étapes, une idée chacune (texte.scene.json) :
- encodage : un fichier est une suite d'octets ; le é en prend deux en UTF-8 ; lu avec une autre table, il devient
  deux caractères ; avec <meta charset="utf-8">, le navigateur lit avec la bonne table ;
- texte : le code à gauche, ce que le navigateur affiche à droite : titre, paragraphe, liste à puces, liste
  numérotée ; chaque balise donne sa forme au texte ;
- liens : trois liens d'une même page, trois destinations ; le lien vers #horaires ne mène nulle part tant
  qu'aucun élément ne porte id="horaires".

Kit plan : x vers la droite, y vers le bas, en unités de 28 px ; un enfant (in) est relatif au centre du parent.
Une règle par sorte : un fichier est un file ; une ligne de code est un node ; ce que le navigateur affiche est
posé dans un layer « la page affichée ».
Couleurs : y le fichier et le code HTML ; v le navigateur et ce qu'il affiche ; g ce qui s'affiche bien ou mène
quelque part ; r ce qui casse ou ne mène nulle part ; n les octets, un autre site.
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


# ---------- 1. encodage
E = [
    ent("e-file", "file", (-11.5, 0), (6.4, 2.6), "y", title="index.html : créé",
        detail="Dans l'éditeur, tu vois le mot **créé**. Sur le disque, le fichier ne contient que des nombres : des **octets**."),
    ent("e-bytes", "layer", (-2, 0), (7, 12), "n", title="les octets, en UTF-8"),
    ent("e-b1", "node", (0, -3.6), (5.4, 2), "n", parent="e-bytes", title="63", sub="c"),
    ent("e-b2", "node", (0, -1.2), (5.4, 2), "n", parent="e-bytes", title="72", sub="r"),
    ent("e-b3", "node", (0, 1.2), (5.4, 2), "n", parent="e-bytes", title="C3 A9", sub="é : deux octets"),
    ent("e-b4", "node", (0, 3.6), (5.4, 2), "n", parent="e-bytes", title="C3 A9", sub="é : deux octets"),
    ent("e-nav", "layer", (8.5, 0), (10.5, 12), "v", title="le navigateur"),
    ent("e-meta", "node", (0, -3), (9, 2.2), "g", parent="e-nav", title="<meta charset=\"utf-8\">",
        detail="Placée au début du `<head>`, elle dit au navigateur **quelle table** utiliser pour lire les octets."),
    ent("e-view", "node", (0, 2), (9, 3), "v", parent="e-nav", title="…"),
]
encodage = {
    "id": "encodage", "label": "L'encodage", "title": "Des octets, et une table pour les lire",
    "body": ["Un fichier est une suite d'octets. L'encodage est la table qui dit quel octet donne quel caractère."],
    "hud": [{"label": "table de lecture", "value": "—"}],
    "show": ["e-file", "e-nav", "e-view"],
    "links": [],
    "script": [
        wait(900),
        scene(show=["e-bytes", "e-b1", "e-b2", "e-b3", "e-b4"], link=[L("e-file", "e-bytes")],
              say="Ton éditeur enregistre le mot en **UTF-8** : une suite d'octets. Le **é** en prend deux, C3 et A9."),
        wait(1500),
        scene(link=[L("e-bytes", "e-nav")]),
        send(["e-bytes", "e-nav"], label="octets"),
        scene(set=[{"id": "e-view", "title": "crÃ©Ã©", "tone": "r"}],
              hud=[hud("table de lecture", "devinée : Windows-1252", "r")],
              say="Sans `charset`, le navigateur **devine** la table. Ici il se trompe : chaque octet du é devient un caractère."),
        wait(1800),
        scene(show=["e-meta"], set=[{"id": "e-view", "title": "créé", "tone": "g"}],
              hud=[hud("table de lecture", "UTF-8, déclarée", "g")],
              say="Avec `<meta charset=\"utf-8\">`, il lit avec la bonne table : deux octets, un seul é."),
        wait(2600),
    ],
}

# ---------- 2. texte : le code et son rendu
XC, XR = -8, 10
DY = 2.0
CODE = [
    ("c1", 0, "<h1>Ma recette</h1>", "y"),
    ("c2", 0, "<p>Une <strong>bonne</strong> crêpe.</p>", "y"),
    ("c3", 0, "<ul>", "y"),
    ("c4", 1, "<li>farine de sarrasin</li>", "y"),
    ("c5", 1, "<li>œufs</li>", "y"),
    ("c6", 0, "</ul>", "y"),
    ("c7", 0, "<ol>", "y"),
    ("c8", 1, "<li>mélanger</li>", "y"),
    ("c9", 1, "<li>cuire</li>", "y"),
    ("c10", 0, "</ol>", "y"),
]
Y0 = -(len(CODE) - 1) * DY / 2
T = []
for i, (id, ind, txt, tone) in enumerate(CODE):
    T.append(ent(id, "node", (XC + ind * 0.9, Y0 + i * DY), (15 - ind * 1.8, 1.6), tone, title=txt))
T += [
    ent("t-page", "layer", (XR, 0), (13, 21), "v", title="la page affichée"),
    ent("t-h1", "node", (0, -7.2), (11, 2.8), "v", parent="t-page", title="Ma recette", sub="titre de niveau 1",
        detail="`<h1>` : le titre principal, un seul par page. `<h2>` à `<h6>` pour les sous-titres."),
    ent("t-p", "node", (0, -3.6), (11, 2.2), "v", parent="t-page", title="Une bonne crêpe.", sub="« bonne » en gras",
        detail="`<p>` fait un paragraphe ; `<strong>` marque un passage important, affiché en gras."),
    ent("t-ul", "node", (0, 0.6), (11, 3.4), "v", parent="t-page", title="• farine de sarrasin   • œufs", sub="liste à puces",
        detail="`<ul>` (*unordered list*) : une liste à puces, un `<li>` par élément."),
    ent("t-ol", "node", (0, 5.4), (11, 3.4), "v", parent="t-page", title="1. mélanger   2. cuire", sub="liste numérotée",
        detail="`<ol>` (*ordered list*) : le navigateur calcule les numéros."),
]
texte = {
    "id": "texte", "label": "Le texte", "title": "Chaque balise donne sa forme au texte",
    "body": ["Le code à gauche, ce que le navigateur affiche à droite."],
    "show": ["c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "t-page"],
    "links": [],
    "labels": "left",
    "script": [
        wait(900),
        scene(show=["t-h1"], link=[L("c1", "t-h1")],
              say="`<h1>` : le **titre** principal, en grand."),
        wait(1300),
        scene(show=["t-p"], link=[L("c2", "t-p")],
              say="`<p>` : un **paragraphe**. Dedans, `<strong>` met « bonne » en gras."),
        wait(1300),
        scene(show=["t-ul"], link=[L("c3", "t-ul")],
              say="`<ul>` et ses `<li>` : une **liste à puces**, une puce par élément."),
        wait(1300),
        scene(show=["t-ol"], link=[L("c7", "t-ol")],
              say="`<ol>` : une **liste numérotée**. Tu n'écris pas les numéros, le navigateur les calcule."),
        wait(2600),
    ],
}

# ---------- 3. liens
K = [
    ent("k-page", "layer", (-5, 0), (15, 17), "v", title="index.html, affichée"),
    ent("k-wiki", "node", (0, -5.6), (12, 2.2), "v", parent="k-page", title="la page Wikipédia", sub="href=\"https://fr.wikipedia.org/…\""),
    ent("k-contact", "node", (0, -2.6), (12, 2.2), "v", parent="k-page", title="nous écrire", sub="href=\"contact.html\""),
    ent("k-ancre", "node", (0, 0.4), (12, 2.2), "v", parent="k-page", title="les horaires", sub="href=\"#horaires\""),
    ent("k-h2", "node", (0, 5.6), (12, 2.2), "y", parent="k-page", title="<h2>Horaires</h2>", sub="plus bas dans la page"),
    ent("k-site", "node", (12, -6), (8, 2.6), "n", title="fr.wikipedia.org", sub="un autre site"),
    ent("k-file", "file", (12, 0), (8, 2.6), "y", title="contact.html",
        detail="Un **chemin relatif** : le navigateur cherche `contact.html` dans le même dossier que la page."),
]
liens = {
    "id": "liens", "label": "Les liens", "title": "Trois liens, trois destinations",
    "body": ["L'attribut href dit où mène le lien : un autre site, une autre page du site, un endroit de la page."],
    "hud": [{"label": "le clic", "value": "—"}],
    "show": ["k-page", "k-wiki", "k-contact", "k-ancre", "k-h2", "k-site", "k-file"],
    "links": [L("k-wiki", "k-site"), L("k-contact", "k-file")],
    "script": [
        wait(900),
        {"do": "pulse", "at": "k-wiki"},
        send(["k-wiki", "k-site"], tone="g", label="clic"),
        scene(hud=[hud("le clic", "un autre site", "g")],
              say="Une **adresse complète**, protocole compris : le clic quitte ton site."),
        wait(1300),
        {"do": "pulse", "at": "k-contact"},
        send(["k-contact", "k-file"], tone="g", label="clic"),
        scene(hud=[hud("le clic", "une autre page du site", "g")],
              say="Un **chemin relatif** : `contact.html`, cherché à côté de la page."),
        wait(1300),
        {"do": "pulse", "at": "k-ancre"},
        scene(set=[{"id": "k-ancre", "tone": "r"}], hud=[hud("le clic", "ne mène nulle part", "r")],
              say="`#horaires` vise l'élément qui porte `id=\"horaires\"`. Il n'y en a pas : le clic ne fait rien, sans message."),
        wait(1700),
        scene(set=[{"id": "k-h2", "title": "<h2 id=\"horaires\">Horaires</h2>", "tone": "g"},
                   {"id": "k-ancre", "tone": "v"}],
              link=[L("k-ancre", "k-h2")],
              say="Deuxième geste : on donne l'`id` au titre visé."),
        send(["k-ancre", "k-h2"], tone="g", label="clic"),
        scene(hud=[hud("le clic", "descend aux horaires", "g")],
              say="Maintenant, le clic fait **descendre** la page jusqu'aux horaires."),
        wait(2600),
    ],
}

write({
    "format": "bl-scenes/0.3", "id": "web-html-texte", "title": "Encodage, texte et liens (2D)",
    "lang": "fr", "kit": "plan",
    "legend": [{"tone": "y", "label": "code HTML"}, {"tone": "v", "label": "le navigateur"},
               {"tone": "g", "label": "ça marche"}, {"tone": "r", "label": "ça casse"}],
    "entities": E + T + K, "steps": [encodage, texte, liens],
}, *outputs(HERE, "texte.scene.json", "web-html-texte"))
