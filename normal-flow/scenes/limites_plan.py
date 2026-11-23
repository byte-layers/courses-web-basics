"""Scène 2D (kit plan) du bit « Bloc, inline : le flux normal d'une page » (normal-flow), section « Ce que le flux
normal ne sait pas faire ».

Une étape (assets/limites.scene.json) :
  limites : l'entête d'un portfolio en flux normal (le logo bloc au-dessus, le menu bloc en dessous) à côté de ce
            qu'on veut (logo à gauche, menu à droite, sur une ligne, centrés) ; le flux normal ne sait pas passer
            de l'un à l'autre, il faut un autre mode de disposition.

Kit plan : x vers la droite, y vers le bas, en unités de 28 px ; un enfant (in) est relatif au centre du parent.
Mêmes règles de dessin que flow.py : un conteneur = layer, un bloc sans enfant = node, un inline = file.
Couleurs : v bloc, y inline (comme flow.py) ; g ce qu'on veut obtenir ; r ce que le flux normal ne fait pas.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools" / "scenes"))
from paths import outputs
from scene_kit import scene, wait, write, hud


def ent(id, kind, at, size=None, tone=None, parent=None, **kw):
    d = {"id": id, "kind": kind, "at": list(at)}
    if tone: d["tone"] = tone
    if size: d["size"] = list(size) + ([] if kind == "zone" else [1])
    if parent: d["in"] = parent
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


LINKS = ["Accueil", "Projets", "Contact"]
ents = [
    # à gauche : le flux normal
    ent("f-head", "layer", (-9, 0), (15, 9), "v", title="header, en flux normal"),
    ent("f-logo", "node", (0, -1.8), (13, 2), "v", parent="f-head", title=".logo : CM", sub="bloc : toute la largeur"),
    ent("f-nav", "layer", (0, 2.1), (13, 3), "v", parent="f-head", title="nav"),
]
ents += [ent(f"f-a{i}", "file", (-4 + 4 * i, 0.4), (3.4, 1.4), "y", parent="f-nav", title=t)
         for i, t in enumerate(LINKS)]
ents += [
    # à droite : ce qu'on veut
    ent("g-head", "layer", (9, 0), (15, 9), "g", title="ce qu'on veut"),
    ent("g-logo", "node", (-5, 0.6), (3, 3), "g", parent="g-head", title="CM"),
    ent("g-nav", "layer", (2, 0.6), (9.6, 3), "g", parent="g-head", title="nav"),
]
ents += [ent(f"g-a{i}", "file", (-3 + 3 * i, 0.4), (2.6, 1.4), "g", parent="g-nav", title=t)
         for i, t in enumerate(LINKS)]

limites = {
    "id": "limites", "label": "Les limites", "title": "Une ligne que le flux normal ne fait pas",
    "body": ["À gauche, l'entête en flux normal ; à droite, ce qu'on veut obtenir."],
    "hud": [{"label": "logo et menu", "value": "—"}],
    "show": ["f-head", "f-logo", "f-nav", "f-a0", "f-a1", "f-a2"],
    "links": [],
    "script": [
        wait(900),
        scene(hud=[hud("logo et menu", "deux lignes", "r")],
              say="En flux normal, `.logo` et `nav` sont **deux blocs** : deux lignes, chacun sur toute la largeur."),
        wait(1600),
        scene(show=["g-head", "g-logo", "g-nav", "g-a0", "g-a1", "g-a2"],
              say="Ce qu'on veut : le logo **à gauche**, le menu **à droite**, sur la même ligne, centrés en hauteur."),
        wait(1600),
        scene(set=[{"id": "g-head", "label": "pas en flux normal"}],
              say="`inline-block` les mettrait côte à côte, mais ne pousse pas le menu à droite et ne centre pas en hauteur."),
        wait(1700),
        scene(hud=[hud("logo et menu", "une ligne : Flexbox", "g")],
              say="Il faut un **autre mode de disposition** : c'est le rôle de Flexbox."),
        wait(2600),
    ],
}

write({
    "format": "bl-scenes/0.3", "id": "normal-flow-limits", "title": "Les limites du flux normal (2D)",
    "lang": "fr", "kit": "plan",
    "legend": [{"tone": "v", "label": "bloc"}, {"tone": "y", "label": "inline"}, {"tone": "g", "label": "ce qu'on veut"}],
    "entities": ents, "steps": [limites],
}, *outputs(HERE, "limites.scene.json", "normal-flow-limits"))
