"""Scène 2D (kit plan) du bit « Données JSON et fetch » (courses-web-basics/json-fetch), le format JSON.

Une étape (json.scene.json) :
- json : un objet JavaScript à gauche, le même en JSON au milieu, ligne par ligne (code annoté) ; à droite, une
  note par règle du JSON : clés entre guillemets doubles, textes entre guillemets doubles, pas de virgule après le
  dernier élément, seulement des données (la fonction ne passe pas).

Kit plan : x vers la droite, y vers le bas, en unités de 28 px.
Une règle par sorte : une ligne de code est un node ; une note est un node neutre (n).
Couleurs : v le code JavaScript ; y le texte JSON ; n les notes ; g ce que le JSON accepte ; r ce qu'il refuse.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools" / "scenes"))
from paths import outputs
from scene_kit import L, scene, wait, write, hud


def ent(id, kind, at, size=None, tone=None, parent=None, **kw):
    d = {"id": id, "kind": kind, "at": list(at)}
    if tone: d["tone"] = tone
    if size: d["size"] = list(size) + ([] if kind == "zone" else [1])
    if parent: d["in"] = parent
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


XJS, XJSON, XN = -14, 0, 14
DY = 2.6
ROWS = 5
Y = [(i - (ROWS - 1) / 2) * DY for i in range(ROWS)]
JS = [
    ("j1", 0, "{"),
    ("j2", 1, "titre: 'Dune',"),
    ("j3", 1, "pages: 900,"),
    ("j4", 1, "resumer() { … },"),
    ("j5", 0, "}"),
]
JSON_ = [
    ("s1", 0, "{"),
    ("s2", 1, "\"titre\": \"Dune\","),
    ("s3", 1, "\"pages\": 900"),
    ("s5", 0, "}"),
]
E = [ent(id, "node", (XJS + ind * 0.9, Y[i]), (11 - ind * 1.8, 1.8), "v", title=t) for i, (id, ind, t) in enumerate(JS)]
E += [ent(id, "node", (XJSON + ind * 0.9, Y[i if i < 3 else 4]), (11 - ind * 1.8, 1.8), "y", title=t)
      for i, (id, ind, t) in enumerate(JSON_)]
E += [
    ent("h-js", "node", (XJS, Y[0] - 3), (11, 1.6), "n", title="un objet JavaScript", sub="dans le code"),
    ent("h-json", "node", (XJSON, Y[0] - 3), (11, 1.6), "n", title="le même, en JSON", sub="un texte"),
    ent("n-cle", "node", (XN, Y[1] - 1.3), (12, 2), "n", title="clés entre guillemets doubles", sub="\"titre\", jamais titre"),
    ent("n-txt", "node", (XN, Y[1] + 1.3), (12, 2), "n", title="textes entre guillemets doubles",
        sub="\"Dune\", jamais 'Dune'"),
    ent("n-virg", "node", (XN, Y[2] + 1.2), (12, 2), "n", title="pas de virgule après le dernier",
        sub="[1, 2, 3,] est refusé"),
    ent("n-data", "node", (XN, Y[3] + 1.0), (12, 2), "n", title="seulement des données",
        sub="textes, nombres, true, false, null…",
        detail="Le JSON accepte des textes, des nombres, `true`, `false`, `null`, des objets et des tableaux. "
               "**Pas de fonction** : une méthode ne passe pas."),
]

json_step = {
    "id": "json", "label": "Le format JSON", "title": "Un objet, et le même écrit en JSON",
    "body": ["Presque la même syntaxe que JavaScript, avec quatre règles plus strictes."],
    "hud": [{"label": "règles", "value": "0 / 4"}],
    "labels": "left",
    "show": ["h-js"] + [r[0] for r in JS],
    "links": [],
    "script": [
        wait(900),
        scene(show=["h-json", "s1", "s2"],
              say="Un objet JavaScript à gauche. Écrivons-le en **JSON**, une ligne après l'autre."),
        wait(1100),
        scene(show=["n-cle"], link=[L("s2", "n-cle")], set=[{"id": "s2", "tone": "g"}], hud=[hud("règles", "1 / 4", "g")],
              say="Première règle : la clé `titre` s'écrit entre **guillemets doubles**, `\"titre\"`."),
        wait(1500),
        scene(show=["n-txt"], link=[L("s2", "n-txt")], set=[{"id": "j2", "label": "'Dune' : refusé en JSON"}],
              hud=[hud("règles", "2 / 4", "g")],
              say="Les textes aussi : `'Dune'`, entre guillemets simples, devient `\"Dune\"`."),
        wait(1500),
        scene(show=["s3"], ms=500),
        scene(show=["n-virg"], link=[L("s3", "n-virg")], set=[{"id": "s3", "tone": "g"}],
              hud=[hud("règles", "3 / 4", "g")],
              say="`\"pages\": 900` est le dernier élément : **pas de virgule** après lui."),
        wait(1500),
        scene(show=["n-data"], link=[L("j4", "n-data", dashed=True)],
              set=[{"id": "j4", "tone": "r", "label": "absente du JSON"}], hud=[hud("règles", "4 / 4", "g")],
              say="La méthode `resumer` ne passe pas : le JSON ne porte **que des données**, jamais de fonction."),
        wait(1300),
        scene(show=["s5"],
              say="Le résultat est un **texte** : il voyage tel quel du serveur à la page."),
        wait(2600),
    ],
}

write({
    "format": "bl-scenes/0.3", "id": "js-json-format", "title": "Le format JSON (2D)",
    "lang": "fr", "kit": "plan",
    "legend": [{"tone": "v", "label": "code JavaScript"}, {"tone": "y", "label": "texte JSON"},
               {"tone": "g", "label": "accepté"}, {"tone": "r", "label": "refusé"}],
    "entities": E, "steps": [json_step],
}, *outputs(HERE, "json.scene.json", "js-json-format"))
