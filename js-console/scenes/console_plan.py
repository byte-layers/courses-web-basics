"""Scènes 2D (kit plan) du bit « La console JavaScript » (courses-web-basics/js-console) : code annoté.

Deux étapes (console-plan.scene.json), une idée chacune :
- calcul : des instructions tapées dans la console, une par ligne, et leur réponse à côté : les opérateurs, le `+`
  qui assemble deux textes, trois fonctions de `Math`, puis une réponse de la console contre une ligne écrite par
  `console.log`. Exemples volontairement différents de l'exercice qui suit (pas de solution donnée) ;
- variables : un nom qui reçoit une valeur ; `let` accepte la nouvelle, `const` la refuse (TypeError). Exemple
  différent de l'exercice (score, jours par semaine).

Kit plan : x vers la droite, y vers le bas, en unités de 28 px ; un enfant (in) est relatif au centre du parent.
Une règle par sorte : une ligne tapée est un node encre (i), à gauche ; ce que la console répond est un node à droite,
relié à sa ligne ; un nom (variable ou constante) est un layer qui porte sa valeur, un node bleu (b, un nombre, comme
dans console.py).
Couleurs : i ce que tu tapes ; g une réponse, une valeur acceptée ; n une ligne écrite par console.log ; r une erreur.
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


# ---------- 1. calcul : une ligne tapée, sa réponse
XC, XN, DY = -8, 8, 2.6
CODE = [
    ("c1", "12 * 4", "← 48", "multiplier : *", "g"),
    ("c2", "10 % 3", "← 1", "% : le reste de 10 divisé par 3", "g"),
    ("c3", "\"Ada\" + \" Lovelace\"", "← \"Ada Lovelace\"", "deux textes : + les assemble", "g"),
    ("c4", "Math.round(249.67)", "← 250", "arrondit à l'entier le plus proche", "g"),
    ("c5", "Math.max(4, 9, 2)", "← 9", "rend le plus grand", "g"),
    ("c6", "Math.random()", "← 0.7302…", "tire au hasard entre 0 et 1", "g"),
    ("c7", "console.log(12 * 4)", "48", "sans marque : une ligne écrite", "n"),
]
Y0 = -(len(CODE) - 1) * DY / 2
C = []
for i, (cid, code, rep, sub, tone) in enumerate(CODE):
    y = Y0 + i * DY
    C.append(ent(cid, "node", (XC, y), (12, 1.8), "i", title=code))
    C.append(ent("r" + cid, "node", (XN, y), (13, 2), tone, title=rep, sub=sub))
C[-1]["detail"] = ("Une **réponse** de la console est précédée d'une marque. Une ligne écrite par **`console.log`** "
                   "n'en a pas : c'est la seule sorte qu'un programme écrit, quand personne ne tape dans la console.")


def ans(i, say):
    cid = CODE[i][0]
    return scene(show=["r" + cid], link=[L(cid, "r" + cid)], say=say)


calcul = {
    "id": "calcul", "label": "Calculer", "title": "Une ligne tapée, une réponse",
    "body": ["À gauche, ce que tu tapes dans la console ; à droite, ce qu'elle répond."],
    "hud": [{"label": "+ entre textes", "value": "—"}],
    "show": [c[0] for c in CODE[:6]],
    "links": [],
    "script": [
        wait(900),
        ans(0, "Les opérateurs de la calculatrice : `*` multiplie, `/` divise. Le séparateur décimal est le **point**."),
        ans(1, "`%` rend le **reste** d'une division : 10 divisé par 3 fait 3, reste 1."),
        wait(900),
        ans(2, "Entre deux textes, le `+` ne calcule pas : il **assemble**. L'espace fait partie du second texte."),
        scene(hud=[hud("+ entre textes", "assemble", "g")]),
        wait(1100),
        scene(show=["rc4", "rc5", "rc6"], link=[L("c4", "rc4"), L("c5", "rc5"), L("c6", "rc6")],
              say="L'objet **`Math`** range des fonctions toutes faites : arrondir, prendre le plus grand, tirer au hasard."),
        wait(1500),
        scene(show=["c7"], say="Un programme, lui, n'a personne pour lire les réponses : il écrit avec `console.log(…)`."),
        ans(6, "La ligne écrite n'a **pas de marque** : elle vient du programme, pas d'une réponse de la console."),
        wait(2600),
    ],
}

# ---------- 2. variables : let accepte, const refuse
XV = 9
V_CODE = [
    ("v1", "let score = 10;"),
    ("v2", "score = score + 5;"),
    ("v3", "const JOURS_PAR_SEMAINE = 7;"),
    ("v4", "JOURS_PAR_SEMAINE = 8;"),
]
VY = [-6, -2.6, 2.6, 6]
V = [ent(vid, "node", (-9, VY[i]), (14, 1.8), "i", title=t) for i, (vid, t) in enumerate(V_CODE)]
V += [
    ent("n-score", "layer", (XV, -4.3), (11, 6), "v", title="score", sub="let : peut changer",
        detail="`let` crée une **variable** : un nom dont la valeur peut changer, sans réécrire `let`."),
    ent("n-score-v", "node", (0, 0.8), (4, 2.2), "b", parent="n-score", title="10"),
    ent("n-jours", "layer", (XV, 4.3), (11, 6), "v", title="JOURS_PAR_SEMAINE", sub="const : ne change pas",
        detail="`const` crée une **constante** : toute nouvelle valeur est refusée. Le bon réflexe : `const` par "
               "défaut, `let` seulement quand la valeur doit changer."),
    ent("n-jours-v", "node", (0, 0.8), (4, 2.2), "b", parent="n-jours", title="7"),
]
variables = {
    "id": "variables", "label": "let et const", "title": "Un nom qui reçoit une valeur",
    "body": ["Le `=` range la valeur de droite dans le nom de gauche."],
    "hud": [{"label": "let score", "value": "—"}, {"label": "const JOURS", "value": "—"}],
    "show": ["v1", "v2", "v3", "v4"],
    "links": [],
    "script": [
        wait(900),
        scene(show=["n-score", "n-score-v"], link=[L("v1", "n-score")], hud=[hud("let score", "10", "b")],
              say="`let score = 10` crée un nom, `score`, et y **range** 10. Le `=` range, il ne compare pas."),
        wait(1300),
        scene(link=[L("v2", "n-score")],
              set=[{"id": "n-score-v", "title": "15", "tone": "g"}, {"id": "n-score", "label": "nouvelle valeur"}],
              hud=[hud("let score", "15", "g")],
              say="`score = score + 5` lit la valeur actuelle, 10, ajoute 5, et range 15 à la place. `let` l'accepte."),
        wait(1500),
        scene(show=["n-jours", "n-jours-v"], link=[L("v3", "n-jours")], hud=[hud("const JOURS", "7", "b")],
              say="`const JOURS_PAR_SEMAINE = 7` crée une **constante** : sa valeur ne changera pas."),
        wait(1300),
        scene(link=[L("v4", "n-jours", dashed=True)],
              set=[{"id": "v4", "tone": "r", "label": "TypeError"}, {"id": "n-jours", "label": "refuse"}],
              hud=[hud("const JOURS", "7, refuse 8", "r")],
              say="`JOURS_PAR_SEMAINE = 8` est **refusé** : la console répond en rouge `TypeError: Assignment to constant variable.`"),
        wait(2800),
    ],
}

write({
    "format": "bl-scenes/0.3", "id": "js-console-plan", "title": "La console, ligne par ligne (2D)",
    "lang": "fr", "kit": "plan",
    "legend": [{"tone": "i", "label": "ce que tu tapes"}, {"tone": "g", "label": "réponse, acceptée"},
               {"tone": "n", "label": "ligne de console.log"}, {"tone": "b", "label": "un nombre rangé"},
               {"tone": "r", "label": "une erreur"}],
    "entities": C + V, "steps": [calcul, variables],
}, *outputs(HERE, "console-plan.scene.json", "js-console-plan"))
