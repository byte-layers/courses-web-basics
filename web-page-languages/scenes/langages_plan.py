"""Scènes 2D (kit plan) du bit « Une page web : HTML, CSS et JavaScript » (courses-web-basics/web-page-languages).

Une étape :
- trois : chaque langage apporte une seule chose à la page ; retirer le CSS ou le JS laisse le contenu ;

Dessin : les fichiers à gauche (un fichier = une boîte « file »), la page affichée à droite (un conteneur « layer » qui
porte ce que le visiteur voit). Dans « moteurs », le navigateur est un conteneur qui porte ses deux moteurs et la page.
Kit plan : x vers la droite, y vers le bas, en unités de 28 px ; un enfant (in) est relatif au centre du parent.
Couleurs : y HTML (le contenu), r CSS (l'apparence : le bouton rose est rose parce que le CSS l'a dit),
g JavaScript (le comportement : le titre changé par le script devient vert), n apparence par défaut du navigateur.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools" / "scenes"))
from paths import outputs
from scene_kit import L, scene, send, wait, write


def ent(id, kind, at, size=None, tone=None, parent=None, **kw):
    d = {"id": id, "kind": kind, "at": list(at)}
    if tone: d["tone"] = tone
    if size: d["size"] = list(size) + [1]
    if parent: d["in"] = parent
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


X_FILE = -11
FILE = (6.4, 2.4)
ents = [
    ent("html", "file", (X_FILE, 0), FILE, "y", title="index.html", sub=None,
        detail="Le **HTML** dit ce que la page contient : un titre, un paragraphe, un bouton. C'est lui qui cite les deux autres fichiers."),
    ent("css", "file", (X_FILE, 5), FILE, "r", title="style.css",
        detail="Le **CSS** dit à quoi ressemble chaque élément : couleurs, tailles, polices, disposition."),
    ent("js", "file", (X_FILE, -5), FILE, "g", title="script.js",
        detail="Le **JavaScript** dit ce qui se passe quand on agit : un clic, une saisie, un défilement."),
    ent("page", "layer", (6, 0), (13, 12.5), "n", title="la page affichée"),
    ent("h1", "node", (0, -2.2), (9.5, 2.2), "y", parent="page", title="Bonjour !"),
    ent("btn", "node", (0, 2.6), (7, 2.2), "n", parent="page", title="Clique-moi"),
]

trois = {
    "id": "trois", "label": "Trois langages", "title": "Chaque langage apporte une chose",
    "body": ["Le HTML donne le contenu, le CSS l'apparence, le JavaScript le comportement. Chacun peut manquer sans emporter les autres."],
    "show": ["html", "page"],
    "links": [],
    "script": [
        wait(900),
        scene(show=["h1", "btn"], link=[L("html", "page")],
              say="Le HTML dit ce que la page contient : un titre et un bouton, avec l'apparence par défaut du navigateur."),
        wait(1300),
        scene(show=["css"], link=[L("css", "btn")]),
        send(["css", "btn"], tone="r", label="rose"),
        scene(set=[{"id": "btn", "tone": "r"}],
              say="La feuille de style dit à quoi il ressemble : le bouton devient rose."),
        wait(1300),
        scene(show=["js"], link=[L("js", "h1")],
              say="Le script attend un clic sur le bouton."),
        wait(900),
        {"do": "pulse", "at": "btn"},
        send(["js", "h1"], tone="g", label="au clic"),
        scene(set=[{"id": "h1", "title": "Merci !", "tone": "g"}],
              say="Au clic, il remplace le texte du titre."),
        wait(1600),
        scene(hide=["css"], set=[{"id": "btn", "tone": "n"}],
              say="Sans la feuille de style, tout le contenu reste ; seule l'apparence par défaut revient."),
        wait(1600),
        scene(hide=["js"], set=[{"id": "h1", "title": "Bonjour !", "tone": "y"}, {"id": "btn", "label": "le clic ne fait rien"}],
              say="Sans le script, la page s'affiche normalement, mais le clic ne fait plus rien."),
        wait(2600),
    ],
}

lesson = {
    "format": "bl-scenes/0.3", "id": "web-page-languages-plan", "title": "HTML, CSS et JavaScript (2D)",
    "lang": "fr", "kit": "plan",
    "legend": [{"tone": "y", "label": "HTML, contenu"}, {"tone": "r", "label": "CSS, apparence"},
               {"tone": "g", "label": "JS, comportement"}],
    "entities": ents, "steps": [trois],
}
write(lesson, *outputs(HERE, "langages.scene.json", "web-langages"))
