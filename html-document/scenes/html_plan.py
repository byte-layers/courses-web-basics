"""Scènes 2D (kit plan) du bit « Le squelette d'une page HTML » (courses-web-basics/html-document).

Trois étapes, une idée chacune :
- emboiter : les éléments s'emboîtent comme des boîtes ; le dernier ouvert se ferme en premier ;
- squelette : où va chaque partie du squelette (title dans l'onglet, h1 et p dans la page, meta nulle part) ;
- chemin : un chemin relatif se lit dossier par dossier à partir de la page ; une majuscule de trop et rien n'est trouvé.

Kit plan : x vers la droite, y vers le bas, en unités de 28 px ; un enfant (in) est relatif au centre du parent.
Une règle par sorte : un élément HTML est une boîte (layer s'il en contient d'autres, node sinon) ; un dossier est
un node, un fichier un file.
Couleurs (html.scene.json) : r élément ouvert, pas encore fermé (en cours) ; g élément fermé ; y le fichier HTML et
ce qu'il contient ; v le navigateur et ce qu'il affiche.
Couleurs (chemin.scene.json) : n dossier, y fichier, g trouvé, r introuvable.
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
    if size: d["size"] = list(size) + [1]
    if parent: d["in"] = parent
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


def line(n):
    return {"do": "line", "n": n}


# ---------- 1. des boîtes emboîtées
ents = [
    ent("e-body", "layer", (0, 0), (16, 11), "r", title="body"),
    ent("e-p", "layer", (0, 0.9), (13, 7), "r", parent="e-body", title="p", sub="Bonjour, je m'appelle"),
    ent("e-strong", "node", (0, 1.2), (7, 2.2), "r", parent="e-p", title="strong", sub="Ada"),
]
CODE = ["<body>", "  <p>Bonjour, je m'appelle", "    <strong>Ada</strong>.", "  </p>", "</body>"]
emboiter = {
    "id": "emboiter", "label": "S'emboîter", "title": "Des éléments emboîtés",
    "body": ["Chaque balise ouvrante ouvre une boîte dans la boîte en cours. On ferme toujours la dernière ouverte en premier."],
    "show": ["e-body"],
    "links": [],
    "widgets": [{"kind": "editor", "title": "index.html", "lang": "text", "lines": CODE}],
    "script": [
        line(1), wait(900),
        scene(say="`<body>` ouvre une boîte : tout ce qui suit sera dedans, jusqu'à `</body>`.",
              set=[{"id": "e-body", "label": "ouverte"}]),
        wait(900), line(2),
        scene(show=["e-p"], say="`<p>` ouvre un paragraphe, à l'intérieur du body."),
        wait(900), line(3),
        scene(show=["e-strong"], say="`<strong>` ouvre une boîte dans le paragraphe… et se ferme sur la même ligne."),
        wait(600),
        scene(set=[{"id": "e-strong", "tone": "g", "label": "fermée"}], ms=500),
        wait(900), line(4),
        scene(set=[{"id": "e-p", "tone": "g", "label": "fermée"}],
              say="`</p>` ferme le paragraphe : c'était la dernière boîte encore ouverte."),
        wait(900), line(5),
        scene(set=[{"id": "e-body", "tone": "g", "label": "fermée"}],
              say="`</body>` ferme la première ouverte : le dernier ouvert se ferme toujours en premier."),
        wait(2600),
    ],
}

# ---------- 2. le squelette : où va chaque partie
XF, XB = -8.5, 8.5
ents += [
    ent("f", "layer", (XF, 0), (13, 18), "y", title="index.html"),
    ent("f-head", "layer", (0, -3.6), (11, 6.6), "y", parent="f", title="head"),
    ent("f-meta", "node", (0, -0.6), (9, 1.7), "y", parent="f-head", title='meta charset="utf-8"'),
    ent("f-title", "node", (0, 1.6), (9, 1.7), "y", parent="f-head", title="title", sub="Mon premier site"),
    ent("f-body", "layer", (0, 4.6), (11, 6.6), "y", parent="f", title="body"),
    ent("f-h1", "node", (0, -0.6), (9, 1.7), "y", parent="f-body", title="h1", sub="Ma première page"),
    ent("f-p", "node", (0, 1.6), (9, 1.7), "y", parent="f-body", title="p", sub="Bonjour ! J'apprends…"),
    ent("win", "layer", (XB, 0), (13, 18), "v", title="navigateur"),
    ent("tab", "node", (-2.2, -6.6), (7.4, 1.8), "v", parent="win", title="onglet", sub="…"),
    ent("view", "layer", (0, 2.2), (11, 11.6), "n", parent="win", title="la page"),
    ent("v-h1", "node", (0, -2.2), (9, 2.4), "v", parent="view", title="Ma première page"),
    ent("v-p", "node", (0, 1.2), (9, 1.6), "v", parent="view", sub="Bonjour ! J'apprends à créer des pages…"),
]
squelette = {
    "id": "squelette", "label": "Le squelette", "title": "Où va chaque partie du squelette",
    "body": ["Le head parle au navigateur ; le body contient ce que voit le visiteur. Le title et le h1 ne s'affichent pas au même endroit."],
    "show": ["f", "f-head", "f-meta", "f-title", "f-body", "f-h1", "f-p", "win", "tab", "view"],
    "links": [],
    "script": [
        wait(1000),
        scene(link=[L("f-title", "tab")]),
        send(["f-title", "tab"], label="Mon premier site"),
        scene(set=[{"id": "tab", "sub": "Mon premier site"}],
              say="Le texte de `<title>` va dans l'onglet du navigateur, jamais dans la page."),
        wait(1300),
        scene(show=[{"id": "v-h1", "dim": True}], link=[L("f-h1", "v-h1")]),
        send(["f-h1", "v-h1"], label="grand titre"),
        scene(set=[{"id": "v-h1", "dim": None}], say="Le `<h1>` est le grand titre, en haut de la page."),
        wait(1100),
        scene(show=["v-p"], link=[L("f-p", "v-p")], say="Le paragraphe suit, dans la page : tout le body est pour le visiteur."),
        wait(1300),
        scene(set=[{"id": "f-meta", "label": "ne s'affiche pas"}],
              say="`<meta charset>` ne s'affiche nulle part : il dit au navigateur comment lire les caractères du fichier."),
        wait(1500),
        scene(set=[{"id": "f-head", "label": "pour le navigateur"}, {"id": "f-body", "label": "pour le visiteur"}],
              say="Le head renseigne le navigateur ; le body est la page que l'on voit."),
        wait(2600),
    ],
}

# ---------- 3. un chemin relatif, dossier par dossier (leçon à part : ses couleurs ont un autre sens)
ents2 = [
    ent("d-site", "node", (0, -6.5), (6, 2), "n", title="site/"),
    ent("d-pages", "node", (-7, -1), (6, 2), "n", title="pages/"),
    ent("d-images", "node", (7, -1), (6, 2), "n", title="images/"),
    ent("d-index", "file", (-7, 5), (7, 2), "y", title="index.html", sub=None),
    ent("d-svg", "file", (7, 5), (7, 2), "y", title="capitole.svg"),
    ent("d-ghost", "node", (0, -1), (5.4, 2), "r", title="Images/ ?", dim=True),
]
TREE = [L("d-site", "d-pages"), L("d-site", "d-images"), L("d-pages", "d-index"), L("d-images", "d-svg")]
chemin = {
    "id": "chemin", "label": "Un chemin", "title": "Un chemin relatif, dossier par dossier",
    "body": ["Le navigateur part du dossier de la page et suit le chemin morceau par morceau : `..` remonte d'un dossier."],
    "hud": [{"label": "dans la page", "value": "pages/index.html"}, {"label": "src", "value": "../images/capitole.svg"}],
    "show": ["d-site", "d-pages", "d-images", "d-index", "d-svg"],
    "links": TREE,
    "script": [
        wait(1000),
        scene(set=[{"id": "d-pages", "label": "on part d'ici"}],
              say="La page est dans `pages/` : c'est de ce dossier que part le chemin."),
        wait(900),
        send(["d-pages", "d-site", "d-images", "d-svg"], label="../images/capitole.svg",
             explain=["`..` remonte d'un dossier : on arrive dans `site/`.",
                      "`images/` descend dans le dossier des images.",
                      "`capitole.svg` : le fichier est là."]),
        scene(set=[{"id": "d-svg", "tone": "g", "label": "trouvé"}, {"id": "d-pages", "label": None}],
              say="Chaque morceau du chemin est un pas dans l'arbre des dossiers."),
        wait(1500),
        scene(set=[{"id": "d-svg", "tone": "y", "label": None}], show=["d-ghost"], link=[L("d-site", "d-ghost", dashed=True)],
              hud=[hud("src", "../Images/capitole.svg", "r")],
              say="Avec `Images/`, une majuscule de trop : sur la plupart des serveurs, ce dossier n'existe pas."),
        wait(1300),
        scene(set=[{"id": "d-ghost", "label": "404 : introuvable"}],
              say="L'image ne s'affiche pas en ligne, même si ton disque, lui, confondait les deux."),
        wait(2600),
    ],
}

lesson = {
    "format": "bl-scenes/0.3", "id": "html-document-plan", "title": "Le squelette d'une page HTML (2D)",
    "lang": "fr", "kit": "plan",
    "legend": [{"tone": "r", "label": "ouvert"}, {"tone": "g", "label": "fermé"},
               {"tone": "y", "label": "le fichier HTML"}, {"tone": "v", "label": "le navigateur"}],
    "entities": ents, "steps": [emboiter, squelette],
}
write(lesson, *outputs(HERE, "html.scene.json", "web-html"))

lesson2 = {
    "format": "bl-scenes/0.3", "id": "html-document-path", "title": "Un chemin relatif (2D)",
    "lang": "fr", "kit": "plan",
    "legend": [{"tone": "n", "label": "dossier"}, {"tone": "y", "label": "fichier"},
               {"tone": "g", "label": "trouvé"}, {"tone": "r", "label": "introuvable"}],
    "entities": ents2, "steps": [chemin],
}
write(lesson2, *outputs(HERE, "chemin.scene.json", "web-chemin"))
