"""Scène 2D (kit plan) du bit « Variables CSS : un choix écrit une fois » (css-variables).

Une étape dans assets/variables.scene.json :
  variables   (section « Les variables CSS ») : une valeur déclarée une fois sur :root, lue par trois règles ;
              on la change, les trois suivent. Le rose devient bleu, pas violet : l'exercice qui suit demande le
              violet, la scène ne donne pas sa solution.

Kit plan : x vers la droite, y vers le bas, en unités de 28 px ; entités au premier niveau.
Dessin : une règle CSS = node. Couleurs : r la couleur d'accent rose, b la couleur d'accent bleue, n une règle pas
encore colorée.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools" / "scenes"))
from paths import outputs
from scene_kit import L, scene, send, wait, write


def r(v):
    return round(v, 3)


def ent(id, kind, cx, cy, w=None, h=None, tone=None, **kw):
    d = {"id": id, "kind": kind, "at": [r(cx), r(cy)]}
    if w is not None:
        d["size"] = [r(w), r(h)] + ([] if kind == "zone" else [1])
    if tone: d["tone"] = tone
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


# ── Étape 1 : une variable, trois lectures ────────────────────────────────────────────────────────────────────
ELS = [("e-h1", "h1"), ("e-btn", ".bouton"), ("e-a", "a")]
ents = [ent("root", "node", 0, -4.0, 11.0, 1.9, "r", title=":root", sub="--accent: rgb(219, 39, 119)",
            detail="`:root` vise l'élément `html` : une variable déclarée ici est disponible dans toute la page.")]
for i, (eid, t) in enumerate(ELS):
    ents.append(ent(eid, "node", -7.2 + i * 7.2, 1.6, 6.0, 1.9, "n", title=t, sub="color: var(--accent)",
                    detail="`var(--accent)` lit la valeur de la variable là où elle sert." if i == 0 else None))

variables = {
    "id": "variables", "label": "Une variable", "title": "Une valeur écrite une fois, lue partout",
    "body": ["Une couleur d'accent déclarée sur `:root`, et trois règles qui s'en servent."],
    "show": ["root"] + [e for e, _ in ELS],
    "script": [
        wait(1000),
        scene(say="Chaque règle lit la valeur avec var(--accent) : les trois éléments prennent la couleur rose.",
              link=[L("root", e) for e, _ in ELS], set=[{"id": e, "tone": "r"} for e, _ in ELS], ms=900),
        wait(1500),
        scene(say="On change la variable, une seule ligne : le bleu remplace le rose.",
              set=[{"id": "root", "tone": "b", "sub": "--accent: rgb(37, 99, 235)"}]),
        wait(600),
        send(["root", "e-h1"], tone="b"),
        send(["root", "e-btn"], tone="b"),
        send(["root", "e-a"], tone="b"),
        scene(say="Les trois éléments suivent, sans qu'on touche à leurs règles.",
              set=[{"id": e, "tone": "b"} for e, _ in ELS]),
        wait(2600),
    ],
}

lesson = {
    "format": "bl-scenes/0.3", "id": "css-variables",
    "title": "Variables CSS", "lang": "fr", "kit": "plan",
    "entities": ents, "steps": [variables],
}
write(lesson, *outputs(HERE, "variables.scene.json", "layout-css-variables"))
