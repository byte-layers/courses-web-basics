"""Scènes 2D (kit plan) du bit « Transitions et animations CSS » (css-motion).

Trois étapes dans assets/motion.scene.json :
  transition  (section « Les transitions ») : posée dans :hover, la transition ne joue qu'à l'aller ; posée sur
              l'état normal, elle joue dans les deux sens.
  animation   (section « Les animations : @keyframes ») : la bannière va de from (invisible, plus bas) à to (visible,
              à sa place) pendant que le temps avance sur une ligne de 0 à 0,6 s.
  reduit      (section « Le piège : prefers-reduced-motion ») : la même bannière ; réglage système désactivé, elle
              monte ; activé, la page rechargée l'affiche directement à sa place.

Kit plan : x vers la droite, y vers le bas, en unités de 28 px ; entités au premier niveau.
Dessin : un élément = node ; la souris = actor ; la couleur de fond du bouton, du bleu au rose, est une piste (zone)
sur laquelle glisse un curseur : il glisse quand une transition joue, il saute quand il n'y en a pas.
Une bannière animée = node, sa place finale = zone en pointillés ; opacity 0 se dessine estompé (dim), et les
encarts donnent les valeurs exactes. Un changement brutal se joue en ms=1 (sinon 700 ms par défaut).
Couleurs : étape 1 : b fond normal (bleu), r fond au survol (rose) ; étapes 2 et 3 : y la bannière, v le réglage activé.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools" / "scenes"))
from paths import outputs
from scene_kit import L, hud, scene, wait, write


def r(v):
    return round(v, 3)


def ent(id, kind, cx, cy, w=None, h=None, tone=None, **kw):
    d = {"id": id, "kind": kind, "at": [r(cx), r(cy)]}
    if w is not None:
        d["size"] = [r(w), r(h)] + ([] if kind == "zone" else [1])
    if tone: d["tone"] = tone
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


# ── Étape 1 : la transition, sur l'état normal ────────────────────────────────────────────────────────────────
BX, BY = -4.0, -2.4          # centre du bouton
MOUSE_OFF, MOUSE_ON = (6.5, -2.2), (0.0, -2.2)
T0, T1 = -8.6, 0.6           # bouts de la piste : fond bleu, fond rose
ents = [
    ent("bouton", "node", BX, BY, 6.0, 1.7, "b", title="a.bouton",
        detail="Le bouton : `background-color` bleu à l'état normal, rose dans `.bouton:hover`."),
    ent("piste", "zone", (T0 + T1) / 2, 1.4, T1 - T0 + 2.0, 1.6, label="fond : bleu → rose"),
    ent("curseur", "node", T0, 1.5, 1.8, 1.0, "b", title="fond",
        detail="La couleur de fond du bouton, entre le bleu (à gauche) et le rose (à droite). Elle **glisse** quand une transition joue, elle **saute** sinon."),
    ent("souris", "actor", *MOUSE_OFF, tone="n", label="souris"),
]


def hover(on, smooth, say):
    return scene(say=say, hud=[hud("état", ":hover" if on else "normal")],
                 set=[{"id": "souris", "at": list(MOUSE_ON if on else MOUSE_OFF)},
                      {"id": "bouton", "tone": "r" if on else "b"},
                      {"id": "curseur", "at": [T1 if on else T0, 1.5], "tone": "r" if on else "b"}],
                 ms=1100 if smooth else 1)


transition = {
    "id": "transition", "label": "La transition", "title": "Une transition posée dans :hover ne joue qu'à l'aller",
    "body": ["Un bouton bleu qui devient rose au survol. Sa transition est écrite dans `.bouton:hover`."],
    "show": ["bouton", "piste", "curseur", "souris"],
    "hud": [{"label": "état", "value": "normal"}, {"label": "transition", "value": "dans :hover", "tone": "r"}],
    "script": [
        wait(1000),
        hover(True, True, "La souris survole : :hover s'applique, avec sa transition. Le fond passe au rose en douceur."),
        wait(1200),
        hover(False, False, "La souris part : l'état normal revient, et il n'a pas de transition. Retour sec."),
        wait(1500),
        scene(say="On déplace la transition dans .bouton, l'état normal : elle vaut maintenant dans les deux sens.",
              hud=[hud("transition", "dans .bouton", "g")]),
        wait(1100),
        hover(True, True, "Le survol : aller en douceur…"),
        wait(1000),
        hover(False, True, "…et retour en douceur."),
        wait(2400),
    ],
}

# ── Étape 2 : une animation @keyframes, de from à to ──────────────────────────────────────────────────────────
PX, PY = 0.0, -2.6           # la place de la bannière (to)
LOW = PY + 1.4               # from : 20 px plus bas (agrandi pour se voir)
A0, A1 = -6.0, 6.0           # ligne de temps : 0 s, 0,6 s
ents += [
    ent("place", "zone", PX, PY, 13.0, 2.8, label="sa place (to)"),
    ent("ban", "node", PX, LOW, 11.0, 2.0, "y", title="header.banniere", sub="Camille Martin",
        detail="La bannière de la page, avec `animation: apparition 0.6s ease-out`."),
    ent("ligne", "zone", (A0 + A1) / 2, 2.6, A1 - A0 + 2.4, 1.6, label="0 s → 0,6 s"),
    ent("temps", "node", A0, 2.7, 2.2, 1.0, "n", title="from",
        detail="Le temps de l'animation, de `from` (0 s) à `to` (0,6 s). Le navigateur calcule chaque image entre les deux."),
]
START = [{"label": "temps", "value": "0 s"}, {"label": "opacity", "value": "0"},
         {"label": "transform", "value": "translateY(20px)"}]

animation = {
    "id": "animation", "label": "@keyframes", "title": "Une animation : de from à to, toute seule",
    "body": ["Au chargement de la page, la bannière joue l'animation `apparition` : deux étapes, `from` et `to`."],
    "show": ["place", {"id": "ban", "dim": True}, "ligne", "temps"],
    "hud": START,
    "script": [
        wait(1000),
        scene(say="La page se charge : la bannière part de from, invisible et 20 px plus bas.",
              set=[{"id": "ban", "label": "from"}]),
        wait(1100),
        scene(say="En 0,6 s, le navigateur calcule chaque image entre from et to : elle monte et apparaît.",
              set=[{"id": "ban", "at": [PX, PY], "dim": None, "label": None},
                   {"id": "temps", "at": [A1, 2.7], "title": "to"}],
              hud=[hud("temps", "0,6 s"), hud("opacity", "1"), hud("transform", "translateY(0)")], ms=1400),
        wait(900),
        scene(say="Arrivée à to, l'animation s'arrête : la bannière garde son style, à sa place.",
              set=[{"id": "ban", "label": "to"}]),
        wait(2600),
    ],
}

# ── Étape 3 : prefers-reduced-motion ──────────────────────────────────────────────────────────────────────────
ents += [
    ent("reglage", "node", -12.0, PY, 7.0, 2.0, "n", title="réglage du système", sub="réduire les animations : non",
        detail="macOS, Windows, Android et iOS ont un réglage pour **réduire les animations**. La page le lit avec `prefers-reduced-motion`."),
]

reduit = {
    "id": "reduit", "label": "Moins de mouvement", "title": "La même bannière, quand le système demande moins de mouvement",
    "body": ["La bannière de l'étape précédente. À gauche, le réglage du système de la personne qui visite la page."],
    "show": ["reglage", "place", {"id": "ban", "dim": True}],
    "hud": [{"label": "réglage", "value": "no-preference"}, {"label": "animation", "value": "apparition"}],
    "script": [
        wait(1000),
        scene(say="Réglage désactivé : au chargement, la bannière monte et apparaît.",
              set=[{"id": "ban", "at": [PX, PY], "dim": None}], ms=1400),
        wait(1300),
        scene(say="La personne active « réduire les animations » dans son système : le mouvement lui donne des vertiges.",
              set=[{"id": "reglage", "tone": "v", "sub": "réduire les animations : oui"}],
              hud=[hud("réglage", "reduce", "v")]),
        wait(1200),
        scene(say="Elle recharge la page.", set=[{"id": "ban", "at": [PX, LOW], "dim": True}], ms=1),
        wait(800),
        scene(say="La media query s'applique, animation: none : la bannière s'affiche directement à sa place.",
              link=[L("reglage", "ban")], set=[{"id": "ban", "at": [PX, PY], "dim": None}],
              hud=[hud("animation", "none", "v")], ms=1),
        wait(2600),
    ],
}

lesson = {
    "format": "bl-scenes/0.3", "id": "css-motion",
    "title": "Transitions et animations CSS", "lang": "fr", "kit": "plan",
    "entities": ents, "steps": [transition, animation, reduit],
}
write(lesson, *outputs(HERE, "motion.scene.json", "layout-css-motion"))
