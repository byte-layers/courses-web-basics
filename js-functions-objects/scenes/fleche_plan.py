"""Scène 2D (kit plan) du bit « Fonctions et objets » (courses-web-basics/js-functions-objects) : la fonction sans
nom, puis la forme fléchée.

Une étape (fleche.scene.json) :
- fleche : la même fonction `double` écrite quatre fois, une rangée par écriture (code annoté) : avec un nom, sans
  nom rangée dans une variable, en flèche, en flèche courte ; à droite, une note par rangée ; en bas, l'appel
  `double(5)`, qui vaut 10 à chaque écriture.

Kit plan : x vers la droite, y vers le bas, en unités de 28 px.
Une règle par sorte : un morceau de code est un node ; une note est un node neutre (n) ; l'appel est un node encre (i).
Couleurs : v le code déjà vu ; y le morceau qui change à cette rangée ; n les notes ; b le nombre rendu.
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


# trois colonnes de code (le nom rangé, l'en-tête, le corps), puis les notes
X1, X2, X3, XN = -12, -5, 2.5, 12.5
W1, W2, W3, WN = 6.5, 6.5, 7.5, 10
Y = [-4.5, -1.5, 1.5, 4.5]
YC = 8.5
H = 2

E = [
    # 1. avec un nom
    ent("a-tete", "node", ((X1 + X2) / 2, Y[0]), (W1 + W2 + 1, H), "v", title="function double(n)"),
    ent("a-corps", "node", (X3, Y[0]), (W3, H), "v", title="{ return n * 2; }"),
    ent("a-note", "node", (XN, Y[0]), (WN, H), "n", title="un nom, un bloc",
        sub="déjà connue"),
    # 2. sans nom, rangée dans une variable
    ent("b-var", "node", (X1, Y[1]), (W1, H), "v", title="const double ="),
    ent("b-tete", "node", (X2, Y[1]), (W2, H), "v", title="function (n)"),
    ent("b-corps", "node", (X3, Y[1]), (W3, H), "v", title="{ return n * 2; }"),
    ent("b-note", "node", (XN, Y[1]), (WN, H), "n", title="pas de nom",
        sub="une valeur",
        detail="Une fonction **sans nom** (on dit aussi *anonyme*) est une valeur, comme un nombre ou un texte : "
               "on la range dans une variable, ou on la donne à une autre fonction."),
    # 3. en flèche
    ent("c-var", "node", (X1, Y[2]), (W1, H), "v", title="const double ="),
    ent("c-tete", "node", (X2, Y[2]), (W2, H), "v", title="(n) =>"),
    ent("c-corps", "node", (X3, Y[2]), (W3, H), "v", title="{ return n * 2; }"),
    ent("c-note", "node", (XN, Y[2]), (WN, H), "n", title="=> remplace function",
        detail="La **forme fléchée** (*arrow function*) : on retire le mot `function`, et une flèche `=>` "
               "suit les paramètres."),
    # 4. en flèche courte
    ent("d-var", "node", (X1, Y[3]), (W1, H), "v", title="const double ="),
    ent("d-tete", "node", (X2, Y[3]), (W2, H), "v", title="(n) =>"),
    ent("d-corps", "node", (X3, Y[3]), (W3, H), "v", title="n * 2"),
    ent("d-note", "node", (XN, Y[3]), (WN, H), "n", title="ni { } ni return",
        sub="un seul calcul"),
    # l'appel
    ent("appel", "node", (X1, YC), (W1, H), "i", title="double(5)",
        detail="L'**appel** s'écrit de la même façon, quelle que soit l'écriture de la fonction."),
]

V = "double(5) vaut"


def essai(row, prev, say):
    """L'appel pointe la rangée du moment, puis rend 10."""
    return [
        scene(link=[L("appel", f"{row}-var" if row != "a" else "a-tete", dashed=True)],
              unlink=[L("appel", prev)] if prev else [], set=[{"id": "appel", "label": None}], hud=[hud(V, "…", None)],
              ms=400),
        wait(500),
        scene(set=[{"id": "appel", "label": "10"}], hud=[hud(V, 10, "b")], say=say),
    ]


step = {
    "id": "fleche", "label": "Sans nom, en flèche", "title": "Une fonction sans nom, puis en flèche",
    "body": ["La même fonction, écrite quatre fois : seule l'écriture change, l'appel rend toujours 10."],
    "hud": [{"label": V, "value": "—"}],
    "labels": "left",
    "show": ["a-tete", "a-corps", "a-note", "appel"],
    "links": [],
    "script": [
        wait(900),
        *essai("a", None, "La fonction que tu connais : un **nom**, ses paramètres, son bloc. `double(5)` rend 10."),
        wait(1400),
        scene(show=["b-var", "b-tete", "b-corps"], ms=600),
        scene(show=["b-note"], link=[L("b-tete", "b-note")], set=[{"id": "b-tete", "tone": "y"}],
              say="Sans nom : `function (n) { … }` est une **valeur**, rangée dans `double` comme un nombre."),
        wait(1300),
        *essai("b", "a-tete", "On l'appelle par le nom de la variable : `double(5)` rend toujours 10."),
        wait(1400),
        scene(show=["c-var", "c-tete", "c-corps"], set=[{"id": "b-tete", "tone": "v"}], ms=600),
        scene(show=["c-note"], link=[L("c-tete", "c-note")], set=[{"id": "c-tete", "tone": "y"}],
              say="La **forme fléchée** : le mot `function` disparaît, une flèche `=>` suit les paramètres."),
        wait(1300),
        *essai("c", "b-var", "Même geste, plus court à écrire : 10."),
        wait(1400),
        scene(show=["d-var", "d-tete", "d-corps"], set=[{"id": "c-tete", "tone": "v"}], ms=600),
        scene(show=["d-note"], link=[L("d-corps", "d-note")], set=[{"id": "d-corps", "tone": "y"}],
              say="Un seul calcul à rendre : on retire les accolades **et** `return`, le résultat est rendu quand même."),
        wait(1300),
        *essai("d", "c-var", "Quatre écritures, une même fonction : `double(5)` vaut 10 à chaque fois."),
        wait(2600),
    ],
}

write({
    "format": "bl-scenes/0.3", "id": "js-arrow-functions", "title": "Fonction sans nom et forme fléchée (2D)",
    "lang": "fr", "kit": "plan",
    "legend": [{"tone": "v", "label": "code"}, {"tone": "y", "label": "ce qui change"},
               {"tone": "i", "label": "l'appel"}, {"tone": "b", "label": "valeur rendue"}],
    "entities": E, "steps": [step],
}, *outputs(HERE, "fleche.scene.json", "js-arrow-functions"))
